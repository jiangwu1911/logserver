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


def empty_search(es):
    return es.search()


def basic_query(es):
    return es.search(body={
                        'query': {
                            'term': { 'type': 'syslog' }
                        }
                    })

def basic_query_nginx(es):
    return es.search(body={
                        'query': {
                            "query_string": {
                                "query": "type:nginx-access",
                                "analyze_wildcard": "true"
                            }
                        }
                    })

def query_range(es):
    return es.search(body={
                        'query': {
                            'range': {
                                '@timestamp': {
                                    #'from': '2014-12-23',
                                    #'to': '2014-12-23'
                                    'from':'2014-12-23T16:19:00+08',
                                    'to': '2014-12-23T17:19:00+08'
                                }
                            },
                        },
                        'sort': [
                            {'@timestamp': {'order': 'desc'}}
                        ],
                        'size': 8
                    })


def query_with_from_and_size(es):
    return es.search(body={
                        'from': 0, 
                        'size': 5,
                        'query': {
                            'term': { 'type': 'syslog' }
                        }
                    })


def query_sort(es):
    return es.search(body={ 
                        'sort': [
                            {'@timestamp': {'order': 'asc'}},
                            {'host': {'order': 'asc'}}
                            
                        ],
                        'query': {
                            'term': { 'type': 'syslog' }
                        }
                    })


def query_field(es):
    return es.search(body={
                        'fields': ['@timestamp', 'host'],
                        'query': {
                            'term': { 'type': 'syslog' }
                        }
                    })


def query_script_field(es):
    return es.search(body={
                        'script_fields': {
                            'test1': {
                                'script': "doc['@version'].value * 10"
                            }
                        },
                        'query': {
                            'term': { 'type': 'syslog' }
                        }
                    })


# Don't understand how to use this...
def query_data_field(es):
    return es.search(body={
                        'fielddata_fields': ['test1', 'test2'],
                        'query': {
                            'term': { 'type': 'syslog' }
                        }
                    })


def post_filter(es):
    return es.search(body={
                        'query': {
                            "filtered": {
                                "filter": {
                                    "bool": {
                                        "must": [
                                            { "term": { "host": "192.168.145.129"   }},
                                            { "term": { "severity": "6" }}
                                        ]
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

def collectd_01(es):
    return es.search(body={
                        "fields": ["@timestamp", "type_instance", "value"],
                        "query": {
                            "filtered": {
                                "query": {
                                    "bool": {
                                        "should": [
                                            { "query_string": { "query": "collectd_type:(cpu) AND type_instance:(system)" } },
                                        ]
                                    }
                                },
                                "filter": {
                                    "bool": {
                                        "must": [
                                            { "range": {
                                                    "@timestamp": {
                                                        "from": "2014-12-20T17:29:00+08",
                                                        "to": "2014-12-24T17:34:00+08"
                                                    }
                                                }
                                            },
                                            { "terms": { "_type": [ "collectd" ] } },
                                            { "terms": { "host": [ "logclient" ] } }
                                        ]
                                    },
                                }
                            }
                        }, 
                        "size": 5,
                        "sort": [
                            {"@timestamp": {"order": "desc"}}
                        ],
                    })


def collectd_02(es):
    return es.search(body={
                        "facets": {
                            "17": {
                                "date_histogram": {
                                    "key_field": "@timestamp",
                                    "value_field": "value",
                                    "interval": "1h"
                                },
                                "global": "true",
                                "facet_filter": {
                                    "fquery": {
                                        "query": {
                                            "filtered": {
                                                "query": {
                                                    "query_string": {
                                                        "query": "plugin:\"cpu\" AND plugin_instance:\"0\" AND type_instance:\"idle\""
                                                    }
                                                },
                                                "filter": {
                                                    "bool": {
                                                        "must": [
                                                            {
                                                                "range": {
                                                                    "@timestamp": {
                                                                        "from": "2014-12-24T11:29:00+08",
                                                                        "to": "2014-12-24T17:34:00+08"
                                                                    }
                                                                }
                                                            },
                                                            {
                                                                "fquery": {
                                                                    "query": {
                                                                        "query_string": {
                                                                            "query": "type:collectd AND host:\"logclient\""
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
                        }
                    })

def basic_match(es):
    return es.search(body={
        'query': {
            'match': {
                'type' : 'nginx'
            }
        }
    })

def basic_match_and(es):
    return es.search(body={
        'query': {
            'match': {
                'message' : {
                    "query" : "192.168.206.1 poweredby", 
                    "operator" : "or"
                    #"operator" : "and"
                }
            }
        }
    })

def basic_test_01(es):
    return es.search(body={
        'query':
            {'filtered' :
                {'query' :
                    {'query_string' :
                        {'query' : 'some query string here'}
                    },
                    'filter' :
                        {'term' : { 'user' : 'kimchy' } }
                }
            }
         })



tracer = logging.getLogger('elasticsearch.trace')
tracer.setLevel(logging.INFO)
tracer.addHandler(logging.FileHandler('es_trace.log'))
tracer.propagate = False

es = Elasticsearch(['http://192.168.102.140:9200'])
info(es)
#print_hits(empty_search(es))
#print_hits(query_range(es))
#print_hits(basic_query(es))
print_hits(basic_test_01(es))
#print_hits(basic_query_nginx(es))
#print_hits(basic_query_nginx(es))
#print_hits(query_with_from_and_size(es))
#print_hits(query_sort(es))
#print_hits(query_field(es))
#print_hits(query_script_field(es))
#print_hits(query_data_field(es))
#print_hits(post_filter(es))
#print_hits(highlight(es))
#print_hits(collectd_01(es))
#print_hits(collectd_02(es))

#print_hits(basic_match_and(es))
