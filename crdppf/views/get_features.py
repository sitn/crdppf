# -*- coding: UTF-8 -*-
from pyramid.response import FileResponse
from pyramid.renderers import render_to_response
from pyramid.httpexceptions import HTTPForbidden
from pyramid.view import view_config
from fpdf import FPDF
from datetime import datetime
import httplib
from owslib.wms import WebMapService
from simplejson import loads as sloads,dumps as sdumps   
import pkg_resources
from crdppf.models import *
import csv
from sqlalchemy import or_
from papyrus.geojsonencoder import dumps
import math

def get_features_function(params):
    # for dev purposes: matching dictionnary model-table name
    table2model = {
        'r73_affectations_primaires': PrimaryLandUseZones,
        'r73_zones_superposees': SecondaryLandUseZones,
        'r73_perimetres_superposes': ComplementaryLandUsePerimeters,
        'r73_contenus_lineaires': LandUseLinearConstraints,
        'r73_contenus_ponctuels': LandUsePointConstraints,
        'r103_bazl_projektierungszonen_flughafenanlagen': CHAirportProjectZones,
        'r108_bazl_sicherheitszonenplan': CHAirportSecurityZones,
        'r116_sites_pollues': PollutedSites,
        'r131_zone_prot_eau': Zoneprotection,
        'r132_perimetre_prot_eau': WaterProtectionPerimeters,
        'r145_sens_bruit': RoadNoise,
        'r157_lim_foret': ForestLimits,
        'r159_dist_foret': ForestDistances
    }

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

    test = 'empty'
    # retrieve models from table2model
    for layer in layerList:
        model = table2model[layer]

    # spatial analysis
    featureList = []
    for layer in layerList:
        targetModel = table2model[layer]
        intersectResult = DBSession.query(targetModel).filter(or_(targetModel.geom.intersects(parcelGeom), targetModel.geom.within(parcelGeom))).all()
        if intersectResult:
            # create geojson output with custom attributes
            for feature in intersectResult:
                geometryType = DBSession.scalar(feature.geom.geometry_type())
                geomType = ''
                intersectionMeasure = -9999
                intersectionMeasureTxt = ''
                if geometryType == 'ST_Polygon' or geometryType == 'ST_MultiPolygon':
                    intersectionMeasure = DBSession.scalar(feature.geom.intersection(parcelGeom).area())
                    if intersectionMeasure >= 1:
                        intersectionMeasureTxt = ' : ' + str(math.ceil(intersectionMeasure*10)/10) + ' [m2]'
                        geomType = 'Polygone'
                        jsonFeature = sloads(dumps(feature))
                        jsonFeature['properties']['layerName'] = layer
                        jsonFeature['properties']['intersectionMeasure'] = intersectionMeasureTxt
                        featureList.append(jsonFeature)

                elif geometryType == 'ST_Line' or geometryType == 'ST_MultiLineString' or geometryType == 'ST_LineString':
                    intersectionMeasure = intersectionMeasure = DBSession.scalar(feature.geom.intersection(parcelGeom).length())
                    if intersectionMeasure >= 1:
                        intersectionMeasureTxt = ' : ' + str(math.ceil(intersectionMeasure*10)/10) + ' [m]'
                        geomType = 'Ligne'
                        jsonFeature = sloads(dumps(feature))
                        jsonFeature['properties']['layerName'] = layer
                        jsonFeature['properties']['intersectionMeasure'] = intersectionMeasureTxt
                        featureList.append(jsonFeature)
                elif geometryType == 'ST_Point' or geometryType == 'ST_MultiPoint':
                    featureMeasure = -9999
                    geomType = 'Point'
                    intersectionMeasureTxt = ' : point'
                    jsonFeature = sloads(dumps(feature))
                    jsonFeature['properties']['layerName'] = layer
                    jsonFeature['properties']['intersectionMeasure'] = intersectionMeasureTxt
                    featureList.append(jsonFeature)

    return featureList


@view_config(route_name='get_features', renderer='json')
def get_features(request):
    params = dict(request.params)
    result = get_features_function(params)
    # append feature list to the response
    return {'type':'FeatureCollection', 'features': result}