# -*- coding: utf-8 -*-
from pyramid.config import Configurator
from sqlalchemy import engine_from_config
import sqlahelper
from pyramid.session import UnencryptedCookieSessionFactoryConfig
from pyramid.mako_templating import renderer_factory as mako_renderer_factory
from papyrus.renderers import GeoJSON
import papyrus

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    
    engine = engine_from_config(
        settings,
        'sqlalchemy.',
        convert_unicode=False,
        encoding='utf-8'
        )
    sqlahelper.add_engine(engine)

    settings.setdefault('mako.directories','crdppf:templates')
    settings.setdefault('reload_templates',True)
    my_session_factory = UnencryptedCookieSessionFactoryConfig('itsaseekreet',2400)
    config = Configurator(settings=settings, session_factory = my_session_factory)
    config.include(papyrus.includeme)
    config.add_renderer('.js', mako_renderer_factory)
    config.add_renderer('geojson', GeoJSON())
    config.add_static_view('static', 'crdppf:static', cache_max_age=3600)

    # ROUTES
    config.add_route('home', '/')
    config.add_route('images', '/static/images/')
    config.add_route('create_extract', 'create_extract')
    config.add_route('get_features', 'get_features')
    config.add_route('set_language', 'set_language')
    config.add_route('get_language', 'get_language')
    config.add_route('crdppf', 'crdppf')
    config.add_route('test', 'test')
    config.add_route('map', 'map')

    config.add_route('globalsjs', '/globals.js')

    config.add_route('ogcproxy', '/ogcproxy')

    # VIEWS
    config.add_view('crdppf.views.entry.Entry', route_name = 'home')
    config.add_view('crdppf.views.entry.Entry', route_name = 'images')
    config.add_view('crdppf.views.entry.Entry', route_name='crdppf')
    config.add_view('crdppf.views.entry.Entry', route_name='test')

    config.scan()

    return config.make_wsgi_app()

