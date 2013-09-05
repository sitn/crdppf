# -*- coding: UTF-8 -*-
from pyramid.response import FileResponse
from pyramid.renderers import render_to_response
from pyramid.httpexceptions import HTTPForbidden
from pyramid.view import view_config

from simplejson import loads as sloads,dumps as sdumps 

from crdppf.models import *
import pkg_resources
from datetime import datetime

from crdppf.models import *

@view_config(route_name='getCadastreList', renderer='json')
def getCadastreList(request):
    """ Loads the list of the cadastres of the Canton."""
    
    cadastres = {}
    cadastres = DBSession.query(Cadastre).order_by(Cadastre.numcad.asc()).all()

    list = []
    for cadastre in cadastres :
        list.append({
            'idobj':cadastre.idobj, 
            'numcom':cadastre.numcom, 
            'comnom':cadastre.comnom, 
            'numcad':cadastre.numcad, 
            'cadnom':cadastre.cadnom, 
            'nufeco':cadastre.nufeco
        })
    
    return list

@view_config(route_name='createNewDocEntry', renderer='json')
def createNewDocEntry(request):
    # Attention il faut que l'utilisateur puisse écrire dans la table et d'1, mais aussi qu'il ait le droit sur la SEQUENCE dans PG
    # Généralement si erreur 'waitress' > problème avec PG/droits dans PG
    session = request.session
    #~ Add login to check user
    data = sloads(request.POST['data'])
    
    document = Documents()
    
    document.nocom = int(data['numcom'])
    document.nufeco = int(data['nufeco'])
    document.nocad = int(data['numcad'])
    document.nomcom = data['comnom']
    document.titre = data['titre']
    document.titreofficiel = data['titreofficiel']
    document.abreviation = data['abreviation']
    document.noofficiel = data['noofficiel']
    document.url = data['url']
    document.statutjuridique = data['statutjuridique']
    document.datesanction = data['datesanction']
    document.dateabrogation = data['dateabrogation']
    document.operateursaisie = data['operateursaisie']
    document.datesaisie = data['datesaisie']
    document.canton = data['canton']

    DBSession.add(document)

    DBSession.flush()

    return {'success':True}
