# -*- coding: UTF-8 -*-

import urllib2

def set_proxy(config):
    proxy_support = urllib2.ProxyHandler({'http':config})
    opener = urllib2.build_opener(proxy_support)
    urllib2.install_opener(opener)  

def unset_proxy():
    proxy_support = urllib2.ProxyHandler({})
    opener = urllib2.build_opener(proxy_support)
    urllib2.install_opener(opener)
