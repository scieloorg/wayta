# coding: utf-8

INDEXES_DOC_TYPE = {
    'institutions': 'wayta_institution',
    'countries': 'wayta_country',
}


class DataBroker(object):

    def __init__(self, es):
        self.es = es

    def _parse_data_countries(self, data, q):
        response = {
            'head': {
                'match': None,
            },
            'choices': []
        }

        if len(data['hits']['hits']) == 0:
            response['head']['match'] = False
            return response

        if data['hits']['hits'][0]['_source']['form'].lower() == q.lower():
            response['head']['match'] = 'exact'
            response['choices'].append(
                {
                    'value': data['hits']['hits'][0]['_source']['name'],
                    'score': data['hits']['hits'][0]['_score'],
                    'iso3661': data['hits']['hits'][0]['_source']['iso-3661']
                }
            )

            return response

        # Loading just the high scored choice
        choices = {}
        for hit in data['hits']['hits']:

            choices.setdefault(hit['_source']['name'], {
                'country': hit['_source']['name'],
                'score': float(hit['_score']),
                'iso3661': hit['_source']['iso-3661']
            })

        best_choices = []
        for choice, values in choices.items():
            best_choice = {
                'value': choice,
                'country': values['country'],
                'score': values['score'],
                'iso3661': values['iso3661']
            }

            best_choices.append(best_choice)

        response['choices'] = sorted(
            best_choices, key=lambda k: k['score'], reverse=True
        )

        if len(response['choices']) == 1:
            response['head']['match'] = 'by_similarity'
        else:
            response['head']['match'] = 'multiple'

        return response

    def _parse_data_institutions(self, data, q):

        response = {
            'head': {
                'match': None,
            },
            'choices': []
        }

        if len(data['hits']['hits']) == 0:
            response['head']['match'] = False
            return response

        if data['hits']['hits'][0]['_source']['form'].lower() == q.lower():
            response['head']['match'] = 'exact'
            response['choices'].append(
                {
                    'value': data['hits']['hits'][0]['_source']['name'],
                    'score': data['hits']['hits'][0]['_score'],
                }
            )

            return response

        # Loading just the high scored choice
        choices = {}
        for hit in data['hits']['hits']:

            choices.setdefault(hit['_source']['name'], {
                'country': hit['_source']['country'],
                'score': float(hit['_score'])
            })

        best_choices = []
        for choice, values in choices.items():
            best_choice = {
                'value': choice,
                'country': values['country'],
                'score': values['score']
            }

            best_choices.append(best_choice)

        response['choices'] = sorted(
            best_choices, key=lambda k: k['score'], reverse=True
        )

        if len(response['choices']) == 1:
            response['head']['match'] = 'by_similarity'
        else:
            response['head']['match'] = 'multiple'

        return response

    def similar_countries(self, index, q):

        if not index in INDEXES_DOC_TYPE:
            raise TypeError('Invalid index name: %s' % index)

        data = {}

        if q:
            data['form'] = q

        qbody = {
            'query': {
                'fuzzy_like_this_field': {
                    'form': {
                        'like_text': q,
                        'fuzziness': 2,
                        'max_query_terms': 100
                    }
                }
            }
        }

        parsed_data = self._parse_data_countries(
            self.es.search(
                index=index,
                doc_type=INDEXES_DOC_TYPE[index],
                body=qbody
            ),
            q
        )

        return parsed_data

    def similar_institutions(self, index, q):

        if not index in INDEXES_DOC_TYPE:
            raise TypeError('Invalid index name: %s' % index)

        data = {}

        if q:
            data['form'] = q

        qbody = {
            'query': {
                'fuzzy_like_this_field': {
                    'form': {
                        'like_text': q,
                        'fuzziness': 2,
                        'max_query_terms': 100
                    }
                }
            }
        }

        parsed_data = self._parse_data_institutions(
            self.es.search(
                index=index,
                doc_type=INDEXES_DOC_TYPE[index],
                body=qbody
            ),
            q
        )

        return parsed_data
