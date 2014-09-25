from elasticsearch import Elasticsearch
from pyramid.config import Configurator

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """

    def add_databroker(request):
        hosts = [
            {
                'host': settings['elasticsearch_host'],
                'port': settings['elasticsearch_port']
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