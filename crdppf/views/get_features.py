# -*- coding: UTF-8 -*-
from pyramid.view import view_config

from crdppf.util.get_feature_functions import get_features_function
from crdppf.models import DBSession
from crdppf.models import Property

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
    queryParcel =DBSession.query(Property).filter_by(idemai=parcelId).first()
    parcelGeom = queryParcel.geom
    return parcelGeom