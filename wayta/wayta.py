import os
from wsgiref.simple_server import make_server

import pyramid.httpexceptions as exc
from pyramid.config import Configurator
from pyramid.view import view_config, notfound_view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPNotFound
from elasticsearch import Elasticsearch

import utils
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

    data = {
        'query': None,
        'alert': None,
        'choices': []
    }

    if query:
        if index == 'institutions':
            result = request.databroker.similar_institutions(index, query)
        elif index == 'countries':
            result = request.databroker.similar_countries(index, query)

        data = {
            'query': query,
            'index': index,
            'alert': alerts.get(str(result['head']['match']), 'danger'),
            'match': str(result['head']['match']),
            'choices': result['choices']
        }

    return data


@view_config(route_name='institution', request_method='GET', renderer='json')
def institution(request):

    query = request.GET.get('q', None)
    country = request.GET.get('country', None)

    if query:
        result = request.databroker.similar_institutions('institutions', query)

    return result


@view_config(route_name='country', request_method='GET', renderer='json')
def country(request):

    query = request.GET.get('q', None)
    country = None

    if query:
        result = request.databroker.similar_countries('countries', query)

    return result


def main(settings):
    """ This function returns a Pyramid WSGI application.
    """

    
    def add_databroker(request):

        hosts = [
            {
                'host': settings['app:main']['elasticsearch_host'],
                'port': settings['app:main']['elasticsearch_port']
            }
        ]

        es = Elasticsearch(hosts)

        return controller.DataBroker(es)

    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('institution', '/api/v1/institution')
    config.add_route('country', '/api/v1/country')
    config.add_request_method(add_databroker, 'databroker', reify=True)

    config.scan()
    return config.make_wsgi_app()

config = utils.Configuration.from_file(os.environ.get('CONFIG_INI', os.path.dirname(__file__)+'/../config.ini'))

settings = dict(config.items())
app = main(settings)