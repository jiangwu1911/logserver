# -*- coding: UTF-8 -*-

import logging
from time import *
from elasticsearch import Elasticsearch

def print_hits(results, facet_masks={}):
    " Simple utility function to print results of a search query. "
    print('=' * 80)
    print('Total %d found in %dms' % (results['hits']['total'], results['took']))
    print(results)
    print()


def _get_cpu_ids(es, host):
    result = es.search(body={
                        "query": { "query_string": { "query": "type:collectd AND host:%s AND plugin:cpu" % host }, },
                        "facets": { "cpu_id": { "terms": {"field": "plugin_instance" }} },
                        "size": 0
                    })
    cpu_ids = []
    for r in result['facets']['cpu_id']['terms']:
        cpu_ids.append(r['term'])
    return cpu_ids 
                            

def search_cpu_data(es, host, from_time="now-10m", to_time="now", interval="5m"):
    querys = []
    cpu_ids = _get_cpu_ids(es, host) 
    
    for cpu_id in cpu_ids:
        for data_type in ('idle', 'user', 'system'):
            q = build_es_search_body_for_cpu_data(host, cpu_id, data_type, from_time, to_time, interval)
            querys.append({})       # Append a empty header
            querys.append(q)
    return es.msearch(body=querys)


def get_current_time():
    return time() 


# 发现ES中,如果输入的时间没按interval对齐,查询出的数据不准确
# adjust_time将时间按interval对其
# 输入输出参数单位都是秒,注意在ES中,需要将其乘以1000使用
def adjust_time(t, interval):
    return int(t / interval) * interval
    

def build_es_search_body_for_cpu_data(host, cpu_id, data_type, from_time, to_time, interval):
    facet_name = "facet_%s_%s" % (cpu_id, data_type)
    query_string = "plugin:cpu AND plugin_instance:%s AND type_instance:%s" % (cpu_id, data_type)
    return {
        "facets": {
            facet_name: {
                "date_histogram": {
                    "key_field": "@timestamp",
                    "value_field": "value",
                    "interval": interval,
                },
                "global": "true",
                "facet_filter": {
                    "fquery": {
                        "query": {
                            "filtered": {
                                "query": {
                                    "query_string": {
                                        "query": query_string
                                    }
                                },
                                "filter": {
                                    "bool": {
                                        "must": [
                                            {
                                                "range": {
                                                    "@timestamp": {
                                                        "from": from_time,
                                                        "to": to_time
                                                    }
                                                }
                                            },
                                            {
                                                "fquery": {
                                                    "query": {
                                                        "query_string": {
                                                            "query": "type:collectd AND host:\"%s\"" % host
                                                        }
                                                    },
                                                    "_cache": "true"
                                                }
                                            }
                                        ]
                                    }
                                },
                            }
                        }
                    }
                }
            }
        },
        "size": 0
    }

def parse_cpu_search_result(results):
    graph_data = {}

    for r in results['responses']:
        for k in r['facets'].keys():
            graph = []
            for item in r['facets'][k]['entries']:
                graph.append({'date': item['time'], 
                              'value': item['mean']})
            # 排序
            graph.sort(lambda x,y : cmp(x['date'], y['date']))
 
            # 求差值
            new_graph = []    
            last_point = None
            for point in graph:
                if last_point != None:
                    p = {}
                    p['date'] = strftime("%Y-%m-%d %H:%M:%S", localtime(point['date']/1000))
                    p['value'] = (point['value'] - last_point['value']) * 1000 / \
                                 (point['date'] - last_point['date'])
                    new_graph.append(p)
                last_point = point
                    
            graph_data[k] = new_graph
    print graph_data        
    



#tracer = logging.getLogger('elasticsearch.trace')
#tracer.setLevel(logging.INFO)
#tracer.addHandler(logging.FileHandler('es_trace.log'))
#tracer.propagate = False

es = Elasticsearch(['http://192.168.145.152:9200'])
intval = 600
to_t = adjust_time(get_current_time(), intval)
from_t = adjust_time(get_current_time() - 6000, intval)

results = search_cpu_data(es, "logclient", from_time=from_t*1000, to_time=to_t*1000, interval=intval*1000)
parse_cpu_search_result(results)
