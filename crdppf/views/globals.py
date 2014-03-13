# -*- coding: UTF-8 -*-
from pyramid.view import view_config

@view_config(route_name='globalsjs', renderer='derived/globals.js')
def globalsjs(request):
    request.response.content = 'application/javascript'
    d = {}
    return d

