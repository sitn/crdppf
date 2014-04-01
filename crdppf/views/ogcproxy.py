# -*- coding: UTF-8 -*-
from pyramid.response import Response
from pyramid.view import view_config

from pyramid.httpexceptions import HTTPNotAcceptable

import httplib2
import urllib
from urlparse import urlparse

from crdppf.lib.wfsparsing import is_get_feature, limit_featurecollection

@view_config(route_name='ogcproxy', renderer='json')
def ogcproxy(request):

    params = dict(request.params)

    params_encoded = {}

    for k, v in params.iteritems():
        if k == 'callback':
            continue
        params_encoded[k] = unicode(v).encode('utf-8')
    query_string = urllib.urlencode(params_encoded)

    if len(params_encoded) > 0:
        _url = '?' + query_string
    else:
        _url = ''

    method = request.method

    url = request.registry.settings['crdppf_wms']

    h = dict(request.headers)

    if urlparse(url).hostname != 'localhost':
        h.pop("Host", h)
    
    body = None
    
    if method in ("POST", "PUT"):
        body = request.body
    
    url += _url
    
    http = httplib2.Http()

    resp, content = http.request(url, method=method, body=body, headers=h)

    if method == "POST" and is_get_feature(body):
        content = limit_featurecollection(content, limit=1)

    headers = {"Content-Type": resp["content-type"]}
    
    return Response(content, status=resp.status, headers=headers)