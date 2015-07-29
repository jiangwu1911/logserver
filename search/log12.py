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


def aggr01(es):
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
                                        "query": {
                                            "match": {
                                                "host": {
                                                    "query": "logclient",
                                                    "type": "phrase"
                                                }
                                            }
                                        }
                                    },
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
                },
                "aggs": {
                    "2": {
                        "date_histogram": {
                            "field": "@timestamp",
                            "interval": "10m",
                            "min_doc_count": 0,
                            "extended_bounds": {
                                "min": 1441123200000,
                                "max": 1441209599999
                            }
                        }
                    }
                },
            })

tracer = logging.getLogger('elasticsearch.trace')
tracer.setLevel(logging.INFO)
tracer.addHandler(logging.FileHandler('es_trace.log'))
tracer.propagate = False

es = Elasticsearch(['http://192.168.102.140:9200'])
info(es)
print_hits(aggr01(es))
