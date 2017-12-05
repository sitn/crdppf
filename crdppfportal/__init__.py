# -*- coding: utf-8 -*-
from pyramid.config import Configurator


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """

    config = Configurator(settings=settings)

    # Get tht Python stuff inside the crdppf_core folder (it's the crdppf folder which contains __init__.py)
    # this includes all routes and views needed by the crdppf application
    config.include('crdppf')
    config.include('pyramid_oereb', route_prefix='oereb')
    config.scan()

    return config.make_wsgi_app()
