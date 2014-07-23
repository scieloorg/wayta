# coding: utf-8
import codecs
from datetime import datetime
from elasticsearch import Elasticsearch


es = Elasticsearch()

with codecs.open('normalized_aff.txt', 'r', encoding='iso-8859-1') as f:

    for line in f:
        splited = line.split('|')
        data = {
            'name': splited[1].strip(),
            'form': splited[0].strip(),
            'country': splited[2].strip(),
            'timestamp': datetime.now()
        }

        res = es.index(index='institutions', doc_type='institution', body=data)
