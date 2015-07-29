INDEX="logstash-web-*"
SERVER=192.168.206.163

#curl -XGET "http://$SERVER:9200/$INDEX/_settings,_mappings"
#curl -i -XGET "http://$SERVER:9200/$INDEX/_stats/indexing?types=nginx-access"

#curl -i -XGET "http://$SERVER:9200/$INDEX/_mappings/agent"
#curl -i -XGET "http://$SERVER:9200/$INDEX/_mappings/"

#curl -XGET "http://$SERVER:9200/$INDEX/_mappings/nginx-access"
#curl -XGET "http://$SERVER:9200/$INDEX/nginx-access/_mapping/field/agent"
#curl -XGET "http://$SERVER:9200/$INDEX/_mapping/nginx-access/field/agent"

#curl -XGET "http://$SERVER:9200/$INDEX/_field_stats?fields=agent&level=indices"

curl -XGET "http://$SERVER:9200/_stats/fielddata/?fields=agent*&pretty"
