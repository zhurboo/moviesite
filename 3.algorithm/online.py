import pymongo
import numpy as np
from pyspark.sql import SparkSession
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils


spark = SparkSession.builder\
    .config("spark.mongodb.input.uri", "mongodb://cloud3:8018,cloud4:8018,cloud5:8018/?replicaSet=cloud")\
    .config("spark.mongodb.output.uri", "mongodb://cloud3:8018,cloud4:8018,cloud5:8018/?replicaSet=cloud")\
    .getOrCreate()
sc = spark.sparkContext

# 电影-相似前5
near_top_5_rdd = spark.sparkContext.textFile('hdfs:///data/near_top_5')\
                    .map(lambda x:x[1:-1].split(','))\
                    .map(lambda x:(int(x[0]),[int(each) for each in x[1:]]))
near_top_5 = {each[0]:each[1] for each in near_top_5_rdd.collect()}

# 电影-特征向量
factors_rdd = spark.sparkContext.textFile('hdfs:///data/movie_factors')\
                .map(lambda x:x[1:-1].split(','))\
                .map(lambda x:(int(x[0]),[float(each) for each in x[1:]]))
factors = {each[0]:each[1] for each in factors_rdd.collect()}


def online_recommend(rdd):
    rdd = rdd.map(lambda x:x.split()).map(lambda x:(int(x[0]),int(x[1]),float(x[2])))
    good_rdd = rdd.filter(lambda x:x[2] > 3).groupBy(lambda x:x[0]).map(lambda x:(x[0],list(x[1])))
    bad_rdd = rdd.filter(lambda x:x[2] < 3).groupBy(lambda x:x[0]).map(lambda x:(x[0],list(x[1])))
    good = {each[0]:each[1] for each in good_rdd.collect()}
    bad = {each[0]:each[1] for each in bad_rdd.collect()}

    print('good:',good)
    print('bad:',bad)
    
    if len(good) == 0 and len(bad) == 0:
        return

    # 用户-推荐ID
    user_recommendation_id_df = spark.read.format("mongo")\
                                    .option("database", "django").option("collection", "user_user_recommendations").load()\
                                    .select('user_id','recommendation_id').selectExpr("recommendation_id as id","user_id")
    # 推荐ID-电影-权重
    movie_recommendation_df = spark.read.format("mongo")\
                                    .option("database", "django").option("collection", "movie_recommendation").load()\
                                    .select('id','movie_id','weight')

    # 推荐ID-用户-电影-权重
    user_movie_recommendation_df = user_recommendation_id_df.join(movie_recommendation_df, 'id')


    # 用户-(用户-推荐ID-电影-权重)
    user_movie_recommendation_rdd = user_movie_recommendation_df.rdd.map(lambda x:(x[1],x[0],x[2],x[3]))\
                                    .groupBy(lambda x:x[0]).map(lambda x:(x[0],list(x[1])))

    # 计算余弦距离
    def cal_cos(x,y):
        return np.sum(np.multiply(x,y))/np.linalg.norm(x)/np.linalg.norm(y)

    # 负操作
    def decay_weight(recommendations, decay_movies):
        for movie in decay_movies:
            cosdis = np.array([cal_cos(factors[movie[1]],factors[recommendation[2]]) for recommendation in recommendations])
            arg = np.argsort(-cosdis)[:5]
            for index in arg:
                recommendation = recommendations[index]
                recommendations[index] = (recommendation[0],recommendation[1],recommendation[2],recommendation[3]*(1-(3-movie[0])/6))
        return recommendations

    # 正操作
    def update_movies(recommendations, add_movies):
        user = recommendations[0][0]
        ids = [recommendation[1] for recommendation in recommendations]
        movies = [recommendation[2] for recommendation in recommendations]
        recommendations = [(recommendation[2],recommendation[3]) for recommendation in recommendations]
        for movie in add_movies:
            new_movies = near_top_5[movie[1]]
            weight = 13+(5-movie[2])
            for each in new_movies:
                if each in movies:
                    recommendations[movies.index(each)] = (recommendations[movies.index(each)][0], max(weight, recommendations[movies.index(each)][1]))
                else:
                    movies.append(each)
                    recommendations.append((each,weight))
        recommendations = sorted(recommendations, key=lambda x:-x[1])[:30]
        recommendations = [(user,ids[i],recommendation[0],recommendation[1]) for i,recommendation in enumerate(recommendations)]
        return recommendations

    # 推荐ID-电影-权重
    recommendations_rdd = user_movie_recommendation_rdd.map(lambda x:(x[0],decay_weight(x[1],bad.get(x[0],[]))))\
                            .map(lambda x:(x[0],update_movies(x[1],good.get(x[0],[]))))\
                            .map(lambda x:x[1]).flatMap(lambda x:[(v[1],v[2],v[3]) for v in x])\

    recommendations_df = spark.createDataFrame(recommendations_rdd, ['id','movie_id','weight'])
    recommendations_df.write.format("mongo").mode("overwrite")\
                        .option("database", "django").option("collection", "movie_recommendation").save()




ssc = StreamingContext(sc, 10)


# 接收操作
kafkaStreams = KafkaUtils.createStream(ssc, 'cloud1:6181,cloud2:6181,cloud3:6181', 'django_group', {'django': 1}).map(lambda x: x[1])
kafkaStreams.foreachRDD(online_recommend)


ssc.start()
ssc.awaitTermination()
