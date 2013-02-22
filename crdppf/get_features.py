# -*- coding: UTF-8 -*-
from pyramid.response import FileResponse
from pyramid.renderers import render_to_response
from pyramid.httpexceptions import HTTPForbidden
from pyramid.view import view_config
from fpdf import FPDF
from datetime import datetime
import httplib
from owslib.wms import WebMapService
import pkg_resources
from geojson import Feature, FeatureCollection, dumps, loads as gloads
from simplejson import loads as sloads,dumps as sdumps   
from crdppf.models import *
from geojson import GeoJSON, Feature, FeatureCollection, dumps, loads as geojsonloads
import csv

@view_config(route_name='get_features',renderer='json')
def get_features(request):
    # for dev purposes: matching dictionnary model-table name
    table2model =   {'at39_itineraires_pedestres':'PedestrianWays',
                    'at14_zones_communales': 'CommunalArea',
                    'at08_zones_cantonales': 'StateArea',
                    'clo_couloirs': 'Corridors',
                    'clo_cotes_altitude_surfaces': 'AltitudeRatings',
                    'en07_canepo_accidents': 'PollutedSitesAccidents',
                    'en07_canepo_decharges': 'PollutedSitesLandDumps',
                    'en07_canepo_decharges_points': 'PollutedSitesLandDumpsPts',
                    'en07_canepo_decharges_polygones': 'PollutedSitesLandDumpsPoly',
                    'en07_canepo_entreprises': 'PollutedSitesCompanies',
                    'en07_canepo_entreprises_points': 'PollutedSitesCompaniesPts',
                    'en07_canepo_entreprises_polygones': 'PollutedSitesCompaniesPoly'}
                
    params = dict(request.params)
    parcelId = params['id']
    # get the parcel geometry
    queryresult =DBSession.query(ImmeublesCanton).filter_by(idemai=parcelId).first()
    sourceParcelGeom = queryresult.geom
    # split the layer list string into proper python list
    layersList = csv.reader([params['layerList']], skipinitialspace=True)
    test = []
    # iterte over layer and make intersects queries
    for layer in layersList:
        test.append(layer);

    queryresult1= DBSession.query(Zoneprotection).filter(Zoneprotection.geom.intersects(sourceParcelGeom)).first()
    out = queryresult1.geom.wkt
    out2 = table2model['at39_itineraires_pedestres']
    return test[0]