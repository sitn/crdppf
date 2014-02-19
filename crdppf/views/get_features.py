# -*- coding: UTF-8 -*-
from pyramid.response import FileResponse
from pyramid.renderers import render_to_response
from pyramid.httpexceptions import HTTPForbidden
from pyramid.view import view_config
from fpdf import FPDF
from datetime import datetime
import httplib
from owslib.wms import WebMapService
from simplejson import loads as sloads 
import pkg_resources
from crdppf.models import *
import csv
from sqlalchemy import or_
from papyrus.geojsonencoder import dumps
import math
from crdppf.util.get_feature_functions import get_features_function

@view_config(route_name='get_features', renderer='json')
def get_features(request):
    params = dict(request.params)
    parcelGeom = getParcelGeom(params['id'])
    result = get_features_function(parcelGeom, params)
    # append feature list to the response
    return {'type':'FeatureCollection', 'features': result}
    
def getParcelGeom(parcelId):
    """ Return the parcel geometry for a given parcel ID
    """  
    queryParcel =DBSession.query(ImmeublesCanton).filter_by(idemai=parcelId).first()
    parcelGeom = queryParcel.geom
    return parcelGeom