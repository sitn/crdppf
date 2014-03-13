# -*- coding: UTF-8 -*-
from pyramid.view import view_config
from crdppf.models import DBSession
from crdppf.models import Themes, Layers

@view_config(route_name='get_interface_config', renderer='json')
def get_interface_config(request):
    """Return a JSON file including all the parameters required to configure the interface
    """    
    
    themes = DBSession.query(Themes).filter_by(publish = True).order_by(Themes.order).all()
    themeList = []
    for theme in themes :
        layers = DBSession.query(Layers).filter_by(theme_id = theme.id).filter_by(baselayer = False).all()
        layerDico = {}
        for layer in layers:
            layerDico[layer.layername] = layer.layername
        themeList.append({'id': theme.id, 'image': theme.image, 'name': theme.varstr, 'layers': layerDico})        
    return {"type": "ThemesCollection", "themes": themeList}
    
@view_config(route_name='get_baselayers_config', renderer='json')
def get_baselayers_config(request):
    """Return a JSON file defining the base layers
    """    
    layers = DBSession.query(Layers).filter_by(baselayer = True).all()
    layerList = []
    for layer in layers:
        layerDico = {}
        layerDico['id'] = layer.layerid
        layerDico['image'] = layer.image
        layerDico['name'] = layer.layername
        layerDico['wmtsname'] = layer.wmtsname
        layerList.append(layerDico)
    return {'baseLayers': layerList}