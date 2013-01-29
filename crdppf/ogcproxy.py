# -*- coding: UTF-8 -*-
from pyramid.response import Response
from pyramid.view import view_config

from pyramid.httpexceptions import HTTPNotAcceptable

import httplib2

from crdppf.lib.wfsparsing import is_get_feature, limit_featurecollection

@view_config(route_name='ogcproxy', renderer='json')
def ogcproxy(request):

    params = dict(request.params)

    method = request.method

    if method == "GET":
        return HTTPNotAcceptable()

    h = dict(request.headers)
    h.pop("Host", h)
    
    body = None
    
    if method in ("POST", "PUT"):
        body = request.body

    url = request.registry.settings['crdppf_wms']
    
    http = httplib2.Http()
    
    resp, content = http.request(url, method=method, body=body, headers=h)

    if method == "POST" and is_get_feature(body):
        content = limit_featurecollection(content, limit=200)

    headers = {"Content-Type": resp["content-type"]}
    
    return Response(content, status=resp.status, headers=headers)