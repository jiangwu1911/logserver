#!/usr/bin/env python

import logging
from elasticsearch import Elasticsearch

def print_hits(results, facet_masks={}):
    " Simple utility function to print results of a search query. "
    print('=' * 80)
    print('Total %d found in %dms' % (results['hits']['total'], results['took']))
    print(results['aggregations'])
    print()


def info(es):
    print(es.info)


def basic_query(es):
    return es.search(body={
                        'query': {
                            'term': { 'type': 'syslog' }
                        }
                    })


def aggr_host(es):
    return es.search(body={
                        'aggs': {
                            'hosts': {
                                'terms': { 'field': 'logsource' }
                            }
                        }
                    })


def aggr_host_range(es):
    return es.search(body={
                        'aggs': {
                            'recent_logs': {
                                'filter': {
                                    'range': {
                                        '@timestamp': {
                                            'from':'2015-04-14T16:19:00+08',
                                            'to': '2015-04-15T17:19:00+08'
                                        }
                                    }
                                },
                                'aggs': {
                                    'hosts': {
                                        'terms': { 'field': 'logsource' }
                                    }
                                }
                            }
                        }
                    })


def aggr_host_range_logtype(es):
    return es.search(body={
                        'query': {
                            'match': { 'type': 'syslog' }
                        },
                        'aggs': {
                            'recent_logs': {
                                'filter': {
                                    'range': {
                                        '@timestamp': {
                                            'from':'2015-04-14T16:19:00+08',
                                            'to': '2015-04-15T17:19:00+08'
                                        }
                                    }
                                },
                                'aggs': {
                                    'hosts': {
                                        'terms': { 'field': 'logsource' }
                                    }
                                }
                            }
                        }
                    })


        

def highlight(es):
    return es.search(body={
                        'highlight': {
                            'fields': { 'host': {} }
                        },
                        'query': {
                            'term': { 'type': 'syslog' }
                        }
                    })

tracer = logging.getLogger('elasticsearch.trace')
tracer.setLevel(logging.INFO)
tracer.addHandler(logging.FileHandler('es_trace.log'))
tracer.propagate = False

es = Elasticsearch(['http://10.2.2.213:9200'])
#info(es)
#print_hits(basic_query(es))
print_hits(aggr_host(es))
#print_hits(aggr_host_range(es))
#print_hits(aggr_host_range_logtype(es))
