#!/bin/sh

# 获取alias
#curl -XGET 'http://192.168.102.140:9200/_cat/aliases?v'

# 获取磁盘空间使用情况
#curl -XGET 'http://192.168.102.140:9200/_cat/allocation?v'

# 获取索引中记录条数
#curl -XGET 'http://192.168.102.140:9200/_cat/indices?help'
#curl -XGET 'http://192.168.102.140:9200/_cat/indices?v'

# 获取在每个node上的数据量
#curl -XGET 'http://192.168.102.140:9200/_cat/fielddata?v'

# 获取索引的健康度
#curl -XGET 'http://192.168.102.140:9200/_cat/health?v'

# 获取索引
#curl -XGET 'http://192.168.102.140:9200/_cat/indices?v'

# 获取master信息
#curl -XGET 'http://192.168.102.140:9200/_cat/master?v'

# 获取节点信息
#curl -XGET 'http://192.168.102.140:9200/_cat/nodes?v'
#curl -XGET 'http://192.168.102.140:9200/_cat/nodes?v&h=id,ip,port,v,m'

# 查询挂起的任务
#curl -XGET 'http://192.168.102.140:9200/_cat/pending_tasks?v'

# 查询plugin
#curl -XGET 'http://192.168.102.140:9200/_cat/plugins?v'

# 查询recovery
#curl -XGET 'http://192.168.102.140:9200/_cat/recovery?v'

# 查询线程池
#curl -XGET 'http://192.168.102.140:9200/_cat/thread_pool?v'

# 查询shards
#curl -XGET 'http://192.168.102.140:9200/_cat/shards?v'

# 查询index pattern
#curl -XGET 'http://192.168.102.140:9200/_cat/shards/logstash-web-2015.09.02?v'

# 获取shards状态
curl -XGET 'http://192.168.102.140:9200/_cat/health?v'

