#!/bin/sh

# 获取索引信息
#curl -XGET 'http://192.168.102.140:9200/logstash-*/?pretty'

# 获取单个索引信息
#curl -XGET 'http://192.168.102.140:9200/logstash-web-2015.09.02/?pretty'

# 获取nginx-access的某一条数据
#curl -XGET 'http://192.168.102.140:9200/logstash-web-2015.09.02/nginx-access/AU-M741is-B314wX560B?pretty'

# 查看数据是否存在
#curl -XHEAD -i 'http://192.168.102.140:9200/logstash-web-2015.09.02/nginx-access/AU-M741is-B314wX560B?pretty'

# 获取数据的某一个字段
#curl -XGET 'http://192.168.102.140:9200/logstash-web-2015.09.02/nginx-access/AU-M741is-B314wX560B?fields=message,verb&pretty'

# 获取某条数据的source
#curl -XGET 'http://192.168.102.140:9200/logstash-web-2015.09.02/nginx-access/AU-M741is-B314wX560B?_source&pretty'

# 获取index的信息
#curl -XGET 'http://192.168.102.140:9200/logstash-web-2015.09.02/_settings,_mappings?pretty'

# 查询索引是否存在
#curl -XHEAD -i 'http://192.168.102.140:9200/logstash-web-2015.09.02?pretty'

# 查询某个type的mapping信息
#curl -XGET 'http://192.168.102.140:9200/logstash-web-2015.09.02/_mapping/nginx-access?pretty'

# 查询某个字段的mapping信息
#curl -XGET 'http://192.168.102.140:9200/logstash-web-2015.09.02/_mapping/nginx-access/field/message?pretty'

# 查询type是否存在
#curl -XHEAD -i 'http://192.168.102.140:9200/logstash-web-2015.09.02/nginx-access?pretty'

# 查看索引状态, 可以返回索引的大小(按字节)
#curl -XGET 'http://192.168.102.140:9200/logstash-web-2015.09.02/_status?pretty'

# 查看索引统计信息, 记录条数
#curl -XGET 'http://192.168.102.140:9200/logstash-web-2015.09.02/_stats?pretty'

# 查看索引segments
curl -XGET 'http://192.168.102.140:9200/logstash-web-2015.09.02/_segments?pretty'
