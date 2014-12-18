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


def query_range(es):
    return es.search(body={
                        'query': {
                            'range': {
                                '@timestamp': {
                                    'from':'2014-12-16',
                                    'to': '2014-12-17'
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




tracer = logging.getLogger('elasticsearch.trace')
tracer.setLevel(logging.INFO)
tracer.addHandler(logging.FileHandler('es_trace.log'))
tracer.propagate = False

es = Elasticsearch(['http://192.168.145.147:9200'])
#info(es)
#print_hits(empty_search(es))
print_hits(query_range(es))
#print_hits(basic_query(es))
#print_hits(query_with_from_and_size(es))
#print_hits(query_sort(es))
#print_hits(query_field(es))
#print_hits(query_script_field(es))
#print_hits(query_data_field(es))
#print_hits(post_filter(es))
#print_hits(highlight(es))
