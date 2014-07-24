# coding: utf-8
import codecs
from datetime import datetime
from elasticsearch import Elasticsearch
import argparse


def institutions(tabfile='normalized_aff.txt', encoding='utf-8'):
    es = Elasticsearch()

    es.indices.delete(index='institutions', ignore=[400, 404])

    with codecs.open(tabfile, 'r', encoding=encoding) as f:

        for line in f:
            splited = line.split('|')
            data = {
                'name': splited[1].strip(),
                'form': splited[0].strip(),
                'country': splited[2].strip(),
                'timestamp': datetime.now()
            }

            res = es.index(index='institutions', doc_type='institution', body=data)


def countries(tabfile='normalized_country.txt', encoding='utf-8'):
    es = Elasticsearch()

    es.indices.delete(index='countries', ignore=[400, 404])

    with codecs.open(tabfile, 'r', encoding=encoding) as f:

        for line in f:
            splited = line.split('|')
            data = {
                'name': splited[1].strip(),
                'form': splited[0].strip(),
                'timestamp': datetime.now()
            }

            res = es.index(index='countries', doc_type='country', body=data)


def argp():
    parser = argparse.ArgumentParser(
        description="Reload index to elasticsearch")

    parser.add_argument(
        '--index',
        '-i',
        choices=['institutions', 'countries'],
        help='Index name that will be reloaded'
    )

    parser.add_argument(
        '--encoding',
        '-e',
        default='utf-8',
        choices=['utf-8', 'iso-8859-1'],
        help='Index name that will be reloaded'
    )

    args = parser.parse_args()

    if args.index == 'institutions':
        institutions(encoding=args.encoding)
        print 'Institutions index reloaded'
    elif args.index == 'countries':
        countries(encoding=args.encoding)
        print 'Countries index reloaded'
    else:
        print 'Nothing done! you must select an index'

if __name__ == "__main__":
    argp()
