# coding: utf-8
import codecs
from datetime import datetime
from elasticsearch import Elasticsearch
import argparse


def institutions(tabfile='normalized_aff.txt'):
    es = Elasticsearch()

    with codecs.open(tabfile, 'r', encoding='iso-8859-1') as f:

        for line in f:
            splited = line.split('|')
            data = {
                'name': splited[1].strip(),
                'form': splited[0].strip(),
                'country': splited[2].strip(),
                'timestamp': datetime.now()
            }

            res = es.index(index='institutions', doc_type='institution', body=data)


def countries(tabfile='normalized_country.txt'):
    es = Elasticsearch()

    with codecs.open(tabfile, 'r', encoding='iso-8859-1') as f:

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

    args = parser.parse_args()

    if args.index == 'institutions':
        institutions()
    else:
        countries()

if __name__ == "__main__":
    argp()
