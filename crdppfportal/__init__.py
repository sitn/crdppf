# -*- coding: utf-8 -*-

from pyramid.config import Configurator
from sqlalchemy import engine_from_config
import sqlahelper
from pyramid.session import UnencryptedCookieSessionFactoryConfig
from pyramid.mako_templating import renderer_factory as mako_renderer_factory
from papyrus.renderers import GeoJSON
import papyrus

import os
import yaml

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    my_session_factory = UnencryptedCookieSessionFactoryConfig('itsaseekreet', 2400)
    config = Configurator(settings=settings, session_factory = my_session_factory)

    # Get tht Python stuff inside the crdppf_core folder (it's the crdppf folder which contains __init__.py)
    # this includes all routes and views needed by the crdppf application
    config.include('crdppf')
    
    config.scan()

    return config.make_wsgi_app()

