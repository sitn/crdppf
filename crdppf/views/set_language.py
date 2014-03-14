# -*- coding: utf-8 -*-
from pyramid.view import view_config

@view_config(route_name='set_language',renderer='string')
def set_language(request):
    params = dict(request.params)
    session = request.session
    lang = params['lang']
    session['lang']=lang
    
@view_config(route_name='get_language',renderer='json')
def get_language(request):
    session = request.session
    if 'lang' not in session:
        session['lang'] = request.registry.settings['default_language']

    return dict(lang=session['lang'])