# coding: utf-8

INDEXES_DOC_TYPE = {
    'institutions': 'institution',
    'countries': 'country',
}


class DataBroker(object):

    def __init__(self, es):
        self.es = es

    def _parse_data(self, data, q):

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

            if 'iso-3661' in data['hits']['hits'][0]['_source']:
                response['choices'][0]['iso3661'] = data['hits']['hits'][0]['_source']['iso-3661']

            return response

        # Loading just the high scored choice
        choices = {}
        for hit in data['hits']['hits']:

            choices.setdefault(hit['_source']['name'], {'country': hit['_source']['name'], 'score': float(hit['_score'])})
            if 'iso-3661' in hit['_source']:
                choices[hit['_source']['name']]['iso-3661'] = hit['_source']['iso-3661']

        #
        best_choices = []
        for choice, values in choices.items():
            best_choice = {'value': choice, 'country': values['country'], 'score': values['score']}

            if 'iso-3661' in values:
                best_choice['iso3661'] = values['iso-3661']

            best_choices.append(best_choice)

        response['choices'] = sorted(best_choices, key=lambda k: k['score'], reverse=True)

        if len(response['choices']) == 1:
            response['head']['match'] = 'by_similarity'
        else:
            response['head']['match'] = 'multiple'

        return response

    def similar(self, index, q):

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

        return self._parse_data(
            self.es.search(
                index=index,
                doc_type=INDEXES_DOC_TYPE[index],
                body=qbody
            ),
            q
        )
