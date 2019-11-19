import pymongo
import numpy as np
from pyspark.sql import SparkSession
from pyspark.ml.recommendation import ALS

spark = SparkSession.builder\
    .config("spark.mongodb.input.uri", "mongodb://cloud3:8018,cloud4:8018,cloud5:8018/?replicaSet=cloud")\
    .config("spark.mongodb.output.uri", "mongodb://cloud3:8018,cloud4:8018,cloud5:8018/?replicaSet=cloud")\
    .getOrCreate()
sc = spark.sparkContext

# 真实评分
true_ratings_rdd = spark.read.format("mongo")\
                    .option("database", "django").option("collection", "rating_mrating").load()\
                    .rdd.map(lambda x:(x[4],x[2],x[3]))
true_ratings_df = spark.createDataFrame(true_ratings_rdd, ['user','item','rating'])

# 虚拟评分
virtual_ratings_rdd = spark.read.csv("hdfs:///data/ratings.csv", header=True)\
                        .rdd.map(lambda x:(int(x[0]),int(x[1]),float(x[2]))).cache()

# 所有评分
all_ratings_rdd = true_ratings_rdd.union(virtual_ratings_rdd)
all_ratings_df = spark.createDataFrame(all_ratings_rdd, ['user','item','rating'])

# 协同过滤模型
als  = ALS(maxIter=5, regParam=0.01)
model = als.fit(all_ratings_df)



# top推荐：用户-电影-权重
recommendations_top_rdd = model.recommendForUserSubset(true_ratings_df,30)\
                            .rdd.flatMap(lambda x: [(x[0],v[0],v[1]) for v in x[1]])

# 真实用户-类型
true_user_genres_rdd = spark.read.format("mongo")\
                        .option("database", "django").option("collection", "user_user_interests").load()\
                        .select('user_id','genre_id').rdd.groupByKey().map(lambda x:(x[0],list(x[1])))
true_user_genres_df = spark.createDataFrame(true_user_genres_rdd, ['user','user_genres'])

# 电影-类型
movie_genres_rdd = spark.read.format("mongo")\
                    .option("database", "django").option("collection", "movie_movie_genres").load()\
                    .select('movie_id','genre_id').rdd.groupByKey().map(lambda x:(x[0],list(x[1])))
movie_genres_df = spark.createDataFrame(movie_genres_rdd, ['item','item_genres'])

# genre推荐：用户-电影-权重
recommendations_genre_rdd = model.recommendForUserSubset(true_ratings_df,60)\
                            .rdd.flatMap(lambda x: [(x[0],v[0],v[1]) for v in x[1]])

# genre推荐：电影-用户-权重-用户类型-电影类型
recommendations_genre_df =  spark.createDataFrame(recommendations_genre_rdd, ['user','item','rating'])\
                            .join(true_user_genres_df, 'user').join(movie_genres_df, 'item')
recommendations_genre_rdd = recommendations_genre_df.rdd.map(lambda x:(x[0],x[1],x[2],x[3],x[4]))\
                            .filter(lambda x:len(set(x[3])&set(x[4])))

# genre推荐：用户-电影-权重     权重改变
recommendations_genre_rdd = recommendations_genre_rdd.map(lambda x:(x[1],x[0],x[2]*(1+0.2*len(set(x[3])&set(x[4])))))
recommendations_genre_pairs = set(recommendations_genre_rdd.map(lambda x:(x[0],x[1])).collect())

# top推荐：用户-电影-权重     去重
recommendations_top_rdd = recommendations_top_rdd.filter(lambda x:(x[0],x[1]) not in recommendations_genre_pairs)

# 综合推荐：用户-电影-权重
recommendations_rdd = recommendations_top_rdd.union(recommendations_genre_rdd)


def top30(x):
    x = sorted(x,key=lambda x:-x[2])
    return x[:30]

# 综合推荐：用户-电影-权重
recommendations_rdd = recommendations_rdd.groupBy(lambda x:x[0]).map(lambda x:(x[0],list(x[1])))\
                        .map(lambda x:top30(x[1])).flatMap(lambda x: [(v[0],v[1],v[2]) for v in x])

# 用户-推荐ID
user_recommendation_ids_rdd = spark.read.format("mongo")\
                                .option("database", "django").option("collection", "user_user_recommendations").load()\
                                .select('user_id','recommendation_id').rdd.groupByKey().map(lambda x:(x[0],list(x[1])))
user_recommendation_ids = {each[0]:each[1] for each in user_recommendation_ids_rdd.collect()}

# 综合推荐：推荐ID-电影-权重
def user_to_movie(user, x, ids):
    for i,id in enumerate(ids[user]):
        x[i] = (id,x[i][1],x[i][2])
    return x

recommendations_rdd = recommendations_rdd.groupBy(lambda x:x[0]).map(lambda x:(x[0],list(x[1])))\
                        .map(lambda x:user_to_movie(x[0], x[1], user_recommendation_ids))\
                        .flatMap(lambda x: [(v[0],v[1],v[2]) for v in x])
recommendations_df = spark.createDataFrame(recommendations_rdd, ['id','movie_id','weight'])

# 更新推荐
recommendations_df.write.format("mongo").mode("overwrite")\
                    .option("database", "django").option("collection", "movie_recommendation").save()



# 电影向量和相似前5的写入
factors_rdd = model.itemFactors.rdd.map(lambda x:[x[0]]+x[1])
factors = np.array(model.itemFactors.rdd.map(lambda x:x[1]).collect())
index = np.array(model.itemFactors.rdd.map(lambda x:x[0]).collect())
factors = np.array(model.itemFactors.rdd.map(lambda x:x[1]).collect())
norms = np.array([np.linalg.norm(each) for each in factors])
near_top_5 = np.zeros((len(norms),5),np.int32)
for i in range(len(norms)):
    cosdis = np.dot(factors,factors.T[:,i])/norms[i]/norms
    arg = np.argsort(-cosdis)
    near_top_5[i,:] = index[arg[:5]]

    
near_top_5_rdd = sc.parallelize([[index[i]]+each for i,each in enumerate(near_top_5.tolist())])

os.system('hdfs dfs -rm -r /data/near_top_5')
os.system('hdfs dfs -rm -r /data/movie_factors')
near_top_5_rdd.saveAsTextFile('hdfs:///data/near_top_5')
factors_rdd.saveAsTextFile('hdfs:///data/movie_factors')