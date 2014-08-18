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
    config.include('crdppf')
    
    #specific_tmp_path = os.path.join(settings['specific_root_dir'], 'templates')
    #specific_static_path = os.path.join(settings['specific_root_dir'], 'static')
    
    #settings.setdefault('mako.directories',['crdppf:templates', specific_tmp_path])
    #settings.setdefault('reload_templates',True)

    global db_config
    db_config = yaml.load(file(settings.get('db.cfg')))['db_config']
    settings.update(yaml.load(file(settings.get('app.cfg')))) 

    config.set_request_property(read_tile_date, name='tile_date', reify=True)

    # add the static view (for static resources)
    #config.add_static_view('static', 'crdppf:static', cache_max_age=3600)
    #config.add_static_view('proj', 'crdppfportal:static', cache_max_age=3600)

    # ROUTES
    #config.add_route('home', '/')
    #config.add_route('images', '/static/images/')
    #config.add_route('create_extract', 'create_extract')
    #config.add_route('get_features', 'get_features')
    #config.add_route('set_language', 'set_language')
    #config.add_route('get_language', 'get_language')
    #config.add_route('get_translation_dictionary', 'get_translation_dictionary')
    #config.add_route('get_interface_config', 'get_interface_config')
    #config.add_route('get_baselayers_config', 'get_baselayers_config')
    #config.add_route('test', 'test')
    #config.add_route('formulaire_reglements', 'formulaire_reglements')
    #config.add_route('getTownList', 'getTownList')
    #config.add_route('getTopicsList', 'getTopicsList')
    #config.add_route('createNewDocEntry', 'createNewDocEntry')
    #config.add_route('getLegalDocuments', 'getLegalDocuments')
    #config.add_route('map', 'map')

    #config.add_route('globalsjs', '/globals.js')

    #config.add_route('ogcproxy', '/ogcproxy')

    # VIEWS
    #config.add_view('crdppf.views.entry.Entry', route_name = 'home')
    #config.add_view('crdppf.views.entry.Entry', route_name = 'images')
    #config.add_view('crdppf.views.entry.Entry', route_name='formulaire_reglements')
    #config.add_view('crdppf.views.entry.Entry', route_name='test')
    #config.add_route('catchall_static', '/*subpath')
    #config.add_view('crdppf.static.static_view', route_name='catchall_static')
    config.scan()

    return config.make_wsgi_app()

