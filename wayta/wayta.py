import os

import pyramid.httpexceptions as exc
from pyramid.view import view_config, notfound_view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPNotFound
import pyramid.httpexceptions as exc

import controller


alerts = {
    "by_similarity": 'info',
    "exact": 'success',
    "multiple": 'warning'
}


@notfound_view_config(append_slash=True)
def notfound(request):
    return HTTPNotFound('Not found')


@view_config(route_name='home', renderer='templates/home.pt')
def home(request):
    query = request.POST.get('q', None)
    index = request.POST.get('index', None)
    accuracy = int(request.POST.get('accuracy', 1))

    data = {
        'query': query,
        'index': index,
        'alert': None,
        'choices': [],
        'accuracy': accuracy,
    }


    if query:
        if index == 'wayta_institutions':
            result = request.databroker.similar_institutions(index, query, accuracy=accuracy)
        elif index == 'wayta_countries':
            result = request.databroker.similar_countries(index, query, accuracy=accuracy)

        data = {
            'query': query,
            'index': index,
            'accuracy': accuracy,
            'alert': alerts.get(str(result['head']['match']), 'danger'),
            'match': str(result['head']['match']),
            'choices': result['choices'],
        }

    return data


@view_config(route_name='institution', request_method='GET', renderer='jsonp')
def institution(request):

    query = request.GET.get('q', None)
    country = request.GET.get('country', None)
    accuracy = request.GET.get('accuracy', 1)

    try:
        accuracy = int(accuracy)
    except:
        raise exc.HTTPBadRequest('Parameter accuracy must be [1,2,3]')

    if not query:
        raise exc.HTTPBadRequest('Parameter q is mandatory')

    result = request.databroker.similar_institutions('wayta_institutions', query, country, accuracy=accuracy)

    return result


@view_config(route_name='country', request_method='GET', renderer='jsonp')
def country(request):

    query = request.GET.get('q', None)
    accuracy = request.GET.get('accuracy', 1)

    try:
        accuracy = int(accuracy)
    except:
        raise exc.HTTPBadRequest('Parameter accuracy must be [1,2,3]')

    if not query:
        raise exc.HTTPBadRequest('Parameter q is mandatory')

    result = request.databroker.similar_countries('wayta_countries', query, accuracy=accuracy)

    return result
