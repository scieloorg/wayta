# coding: utf-8

import unittest

import controller


class ControllerTests(unittest.TestCase):

    def setUp(self):
        self.sample_data = {
            "took": 12,
            "timed_out": False,
            "_shards": {
                "total": 5,
                "successful": 5,
                "failed": 0
            },
            "hits": {
                "total": 9768,
                "max_score": 7.0640388,
                "hits": [
                    {
                        "_index": u"institutions",
                        "_type": u"institution",
                        "_id": u"z6-6J_3LQt-AgMc7_ewonw",
                        "_score": 7.0640388,
                        "_source": {
                            u"country": "Brazil",
                            u"name": "Universidade de Mogi das Cruzes",
                            u"form": "Universidade de Mogi das Cruzes"
                        }
                    },
                    {
                        "_index": u"institutions",
                        "_type": u"institution",
                        "_id": u"z6-6J_3LQt-AgMc7_ewonw",
                        "_score": 6.0640388,
                        "_source": {
                            u"country": "Brazil",
                            u"name": "Universidade de Mogi das Cruzes",
                            u"form": "UMC/PUC"
                        }
                    },
                    {
                        "_index": u"institutions",
                        "_type": u"institution",
                        "_id": u"d7ZqX4o-TMKGkADnGhVB8A",
                        "_score": 5.0640388,
                        "_source": {
                            u"country": "Brazil",
                            u"name": "Universidade de Mogi das Cruzes",
                            u"form": "Universidade de Mogi das Cruzes São Paulo"
                        }
                    },
                    {
                        "_index": u"institutions",
                        "_type": u"institution",
                        "_id": u"ZmWiK2WkRfabdpZMaAP4rg",
                        "_score": 4.0640388,
                        "_source": {
                            u"country": "Brazil",
                            u"name": "Universidade de Mogi das Cruzes",
                            u"form": "Universidade de Mogi das Cruzes/Universidade Braz Cubas"
                        }
                    }
                ]
            }
        }

    def test_parse_data_exact_match(self):

        dummy_elasticsearch = 'dummy'

        db = controller.DataBroker(dummy_elasticsearch)

        parsed = db._parse_data(self.sample_data, u'Universidade de Mogi das Cruzes')

        expected = {
            'head': {
                'match': 'exact'
            },
            'choices': [
                {
                    'value':u'Universidade de Mogi das Cruzes',
                    'score': 7.0640388
                }
            ]
        }

        self.assertEqual(expected['head']['match'], parsed['head']['match'])
        self.assertEqual(len(expected['choices']), len(parsed['choices']))
        self.assertEqual(expected['choices'][0]['score'], parsed['choices'][0]['score'])

    def test_parse_data_not_match(self):

        dummy_elasticsearch = 'dummy'

        db = controller.DataBroker(dummy_elasticsearch)

        self.sample_data['hits']['hits'] = []

        parsed = db._parse_data(self.sample_data, u'Universidade de Mogi das Cruzes')

        expected = {
            'head': {
                'match': False
            },
            'choices': []
        }

        self.assertEqual(expected['head']['match'], parsed['head']['match'])
        self.assertEqual(len(expected['choices']), len(parsed['choices']))

    def test_parse_data_match_by_similarity(self):

        dummy_elasticsearch = 'dummy'

        db = controller.DataBroker(dummy_elasticsearch)

        self.sample_data['hits']['hits'] = self.sample_data['hits']['hits'][1:]

        parsed = db._parse_data(self.sample_data, u'Universidade de Mogi das Cruzes')

        expected = {
            'head': {
                'match': 'by_similarity'
            },
            'choices': [
                {
                    'value': u'Universidade de Mogi das Cruzes',
                    'score': 6.0640388
                }
            ]
        }

        self.assertEqual(expected['head']['match'], parsed['head']['match'])
        self.assertEqual(len(expected['choices']), len(parsed['choices']))
        self.assertEqual(expected['choices'][0]['score'], parsed['choices'][0]['score'])

    def test_parse_data_multiple_match(self):

        dummy_elasticsearch = 'dummy'

        db = controller.DataBroker(dummy_elasticsearch)

        usp = {
            "_index": u"institutions",
            "_type": u"institution",
            "_id": u"ZmWiK2WkRfabdpZMaAP4rg",
            "_score": 3.0640388,
            "_source": {
                u"country": "Brazil",
                u"name": "Universidade de São Paulo",
                u"form": "Universidade de São Paulo"
            }
        }
        self.sample_data['hits']['hits'] = self.sample_data['hits']['hits'][1:]
        self.sample_data['hits']['hits'].append(usp)

        parsed = db._parse_data(self.sample_data, u'Universidade de Mogi das Cruzes')

        expected = {
            'head': {
                'match': 'multiple'
            },
            'choices': [
                {
                    'value': u'Universidade de Mogi das Cruzes',
                    'score': 6.0640388
                },
                {
                    'value': u'Universidade de São Paulo',
                    'score': 3.0640388
                }
            ]
        }

        self.assertEqual(expected['head']['match'], parsed['head']['match'])
        self.assertEqual(len(expected['choices']), len(parsed['choices']))
        self.assertEqual(expected['choices'][0]['score'], parsed['choices'][0]['score'])
        self.assertEqual(expected['choices'][1]['score'], parsed['choices'][1]['score'])
