# -*- coding: UTF-8 -*-

# 按时间段查询所有web日志记录

#!/usr/bin/env python

import logging
from elasticsearch import Elasticsearch

def print_hits(results, facet_masks={}):
    " Simple utility function to print results of a search query. "
    print('=' * 80)
    print('Total %d found in %dms' % (results['hits']['total'], results['took']))
    print(results)
    print()


def info(es):
    print(es.info)


def query(es):
    return es.search(body={
                "size": 5,
                "query": {
                    "filtered": {
                        "query": {
                            "query_string": {
                                "analyze_wildcard": "true",
                                "query": "*"
                            }
                        },
                        "filter": {
                            "bool": {
                                "must": [
                                    {
                                        "range": {
                                            "@timestamp": {
                                                "gte": 1441123200000,
                                                "lte": 1441209599999
                                            }
                                        }
                                    }
                                ],
                                "must_not": []
                            }
                        }
                    }
                }
            })

tracer = logging.getLogger('elasticsearch.trace')
tracer.setLevel(logging.INFO)
tracer.addHandler(logging.FileHandler('es_trace.log'))
tracer.propagate = False

es = Elasticsearch(['http://192.168.102.140:9200/logstash-web-*'])
info(es)
print_hits(query(es))
