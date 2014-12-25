#!/usr/bin/env python

import logging
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
                            

def search_cpu_data(es, host, from_time="now-2m", to_time="now", interval="1m"):
    querys = []
    cpu_ids = _get_cpu_ids(es, host) 
    
    for cpu_id in cpu_ids:
        for data_type in ('idle', 'user', 'system'):
            q = build_es_search_body_for_cpu_data(host, cpu_id, data_type, from_time, to_time, interval)
            querys.append({})       # Append a empty header
            querys.append(q)
    return es.msearch(body=querys)
    

def build_es_search_body_for_cpu_data(host, cpu_id, data_type, from_time, to_time, interval):
    facet_name = "facet_%s_%s" % (cpu_id, data_type)
    query_string = "plugin:cpu AND plugin_instance:%s AND type_instance:%s" % (cpu_id, data_type)
    return {
        "facets": {
            facet_name: {
                "date_histogram": {
                    "key_field": "@timestamp",
                    "value_field": "value",
                    "interval": interval
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
                                }
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
            graph_data[k] = graph

    # 1. 时间需要处理成字符串格式的吗?
    # 2. value需要减去前一点的
                
    print graph_data        
    



#tracer = logging.getLogger('elasticsearch.trace')
#tracer.setLevel(logging.INFO)
#tracer.addHandler(logging.FileHandler('es_trace.log'))
#tracer.propagate = False

es = Elasticsearch(['http://192.168.145.152:9200'])

results = search_cpu_data(es, "logclient")
parse_cpu_search_result(results)
