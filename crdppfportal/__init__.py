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


def read_tile_date(request):
    """
    Read the tile date from tile date file. Return "c2c", "c2c"
    if there's no tile date file. "c2c" corresponds to a static
    tile set that is always exists on the server.
    """

    tile_date_file = request.registry.settings['tile_date_file']
    if os.path.exists(tile_date_file):
        tile_date = yaml.load(file(tile_date_file))
        return tile_date['plan_cadastral'], tile_date['plan_ville']
    return 'c2c', 'c2c'

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    my_session_factory = UnencryptedCookieSessionFactoryConfig('itsaseekreet',2400)
    config = Configurator(settings=settings, session_factory = my_session_factory)

    # Get tht Python stuff inside the crdppf_core folder (it's the crdppf folder which contains __init__.py)
    # this includes all routes and views needed by the crdppf application
    config.include('crdppf')

    config.set_request_property(read_tile_date, name='tile_date', reify=True)

    config.scan()

    return config.make_wsgi_app()

