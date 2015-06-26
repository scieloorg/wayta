# coding: utf-8
from datetime import datetime
from elasticsearch import Elasticsearch
import argparse
import csv

from wayta import utils

config = utils.Configuration.from_env()
settings = dict(config.items())
ESHOST = settings['app:main'].get('elasticsearch_host', '127.0.0.1')
ESPORT = settings['app:main'].get('elasticsearch_port', '9200')

def institutions(tabfile='normalized_aff.csv'):
    es = Elasticsearch(ESHOST, port=ESPORT)

    mapping = {
        "mappings": {
            "institution": {
                "properties": {
                   "city": {
                      "type": "string"
                   },
                   "country": {
                      "type": "string"
                   },
                   "form": {
                      "type": "string"
                   },
                   "iso-3166": {
                      "type": "string",
                      "index": "not_analyzed"
                   },
                   "name": {
                      "type": "string"
                   },
                   "state": {
                      "type": "string"
                   }
                }
            }
        }
    }

    es.indices.delete(index='wayta_institutions', ignore=[400, 404])
    es.indices.create(index='wayta_institutions', body=mapping)

    with open(tabfile, 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';', quotechar='"')
        for line in spamreader:
            data = {
                'name': line[1].strip(),
                'form': line[0].strip(),
                'country': line[2].strip(),
                'iso-3166': line[3].strip(),
                'state': line[4].strip(),
                'city': line[5].strip(),
                'timestamp': datetime.now()
            }

            res = es.index(index='wayta_institutions', doc_type='institution', body=data)


def countries(tabfile='normalized_country.csv'):
    es = Elasticsearch(ESHOST, port=ESPORT)

    mapping = {
        "mappings": {
            "country": {
                "properties": {
                    "form": {
                        "type": "string"
                   },
                    "iso-3166": {
                        "type": "string",
                        "index": "not_analyzed"
                   },
                    "name": {
                        "type": "string"
                   }           
                }
            }
        }
    }

    es.indices.delete(index='wayta_countries', ignore=[400, 404])
    es.indices.create(index='wayta_countries', body=mapping)

    with open(tabfile, 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';', quotechar='"')

        for line in spamreader:
            data = {
                'name': line[1].strip(),
                'iso-3166': line[2].strip(),
                'form': line[0].strip(),
                'timestamp': datetime.now()
            }

            res = es.index(index='wayta_countries', doc_type='country', body=data)


def main():
    parser = argparse.ArgumentParser(
        description="Reload index to elasticsearch")

    parser.add_argument(
        '--index',
        '-i',
        choices=['institutions', 'countries'],
        help='Index name that will be reloaded'
    )

    parser.add_argument(
        '--csv_file',
        '-f',
        help='CSV file with the data that will be loaded to Wayta'
    )

    args = parser.parse_args()

    if args.index == 'institutions':
        institutions(tabfile=args.csv_file)
        print 'Institutions index reloaded'
    elif args.index == 'countries':
        countries(tabfile=args.csv_file)
        print 'Countries index reloaded'
    else:
        print 'Nothing done! you must select an index'
