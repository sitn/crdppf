from pyramid.config import Configurator
from sqlalchemy import engine_from_config
import sqlahelper

from pyramid.session import UnencryptedCookieSessionFactoryConfig

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
    config.add_static_view('static', 'crdppf:static', cache_max_age=3600)
    
    config.add_route('home', '/')
    config.add_view('crdppf.entry.Entry', route_name = 'home')
    
    
    config.add_route('create_extrait', 'create_extrait')
    
    
    
    
    config.scan()
    
    return config.make_wsgi_app()

