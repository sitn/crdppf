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
from sqlalchemy import or_

@view_config(route_name='get_features',renderer='geojson')
def get_features(request):
    # for dev purposes: matching dictionnary model-table name
    table2model =   {'at39_itineraires_pedestres':PedestrianWays,
                    'at14_zones_communales': CommunalArea,
                    'at08_zones_cantonales': StateArea,
                    'clo_couloirs': Corridors,
                    'clo_cotes_altitude_surfaces': AltitudeRatings,
                    'en07_canepo_accidents': PollutedSitesAccidents,
                    'en07_canepo_decharges': PollutedSitesLandDumps,
                    'en07_canepo_decharges_points': PollutedSitesLandDumpsPts,
                    'en07_canepo_decharges_polygones': PollutedSitesLandDumpsPoly,
                    'en07_canepo_entreprises': PollutedSitesCompanies,
                    'en07_canepo_entreprises_points': PollutedSitesCompaniesPts,
                    'en07_canepo_entreprises_polygones': PollutedSitesCompaniesPoly}
                
    params = dict(request.params)
    parcelId = params['id']
    # get the parcel geometry
    queryParcel =DBSession.query(ImmeublesCanton).filter_by(idemai=parcelId).first()
    parcelGeom = queryParcel.geom
    # split the layer list string into proper python list
    csvReader = csv.reader([params['layerList']], skipinitialspace=True)

    # iterate over layer and make intersects queries
    itemList = []
    for item in csvReader:
        itemList.append(item)
    layerList = itemList[0]
    response = []
    test = 'empty'
    for layer in layerList:
        targetModel = table2model[layer]
        intersectResult = DBSession.query(targetModel).filter(or_(targetModel.geom.intersects(parcelGeom),targetModel.geom.within(parcelGeom))).all()
        if intersectResult:
            for feature in intersectResult:
                response.append(feature)

    return response