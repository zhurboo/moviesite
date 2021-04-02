# 分布式电影推荐系统

北京大学2019年秋《云计算与大数据平台》课程项目。

这是一个结合了 Hadoop、Hbase、Spark、MongoDB、Django 等开源框架的高可用分布式电影推荐系统，并以 Web 页面为用户提供了友好的访问方式。

## 系统功能

- 基本功能
  - 登录注册
  - 个人信息维护
  - 按类别电影展示
  - 电影搜索
  - 电影详情查看
  - 电影评分
  - 电影评论
- 后台管理
- 电影推荐
  - 协同过滤推荐
  - 兴趣推荐
  - 在线推荐

   
## 体系框架

![](https://i.postimg.cc/BnXbhqkT/tixi.png)

## 系统架构
本系统的系统架构如图2 所示，我们的数据基于MovieLens 20M6 数据集，并将
该数据集的rating.csv 存入HDFS 集群，并从IMDB7 爬取数据集中的电影基本信息
与电影图片，电影基本信息经过处理后存入MongoDB 集群，电影图片存入Hbaes8 集
群。计算模块运行于YARN 集群上，其中Spark 负责离线推荐计算，Spark Streaming
负责在线推荐计算，离线推荐计算的任务每天执行一次，在线推荐计算的任务来源于
Kafka9 消息队列，时间窗口和间隔均为一分钟，计算所得的推荐结果存入MongoDB
集群。使用Nginx10 处理负载均衡和静态文件(电影图片、css、js)，使用uWSGI11 启
动Django 服务，并将动静请求分离，Redis12 作为Django 的缓存。Zookeeper13 用来
保证Kafka、YARN、HDFS 和Hbase 的高可用性。接下来，我们将分别介绍本系统中
的各个组件。
![](https://i.postimg.cc/MG1W4XDQ/xitong.png)

## 配置与使用

1. [详细配置](详细配置.md)
2. [详细使用](详细使用.md)
3. [简单使用(需要在作者的环境下)](简单使用.md)


