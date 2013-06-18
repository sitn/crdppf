# -*- coding: utf-8 -*-

from pyramid.view import view_config


class Entry(object):
    
    def __init__(self, request):
        self.debug = "debug" in request.params
        self.settings = request.registry.settings
        self.request = request
    
    @view_config(route_name='home', renderer = '/base/index.mako')
    def home(self):
        d = {
            'debug': self.debug
        }
        return d

    @view_config(route_name='crdppf',renderer = '/derived/crdppf.mako')
    def crdppf(self):
        d = {
            'debug': self.debug
        }
        return d    
    
    @view_config(route_name='test',renderer = '/derived/test.mako')
    def test(self):
        d = {
            'debug': self.debug
        }
        return d

    @view_config(route_name='map',renderer = '/derived/map.mako')
    def map(self):
        d = {
            'debug': self.debug
        }
        return d