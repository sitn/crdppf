# -*- coding: UTF-8 -*-
from pyramid.view import view_config

from simplejson import loads as sloads

from crdppf.models import DBSession
from crdppf.models import Topics, LegalBases, LegalProvisions, References
from crdppf.models import TemporaryProvisions
from crdppf.models import Town

@view_config(route_name='getTownList', renderer='json')
def getTownList(request):
    """ Loads the list of the cadastres of the Canton."""
    
    results = {}

    if 'numcad' in Town.__table__.columns.keys():
        results = DBSession.query(Town).order_by(Town.numcad.asc()).all()
    else:
        results = DBSession.query(Town).order_by(Town.numcom.asc()).all()

    towns = []
    for town in results :
        if 'numcad' in Town.__table__.columns.keys():
            numcad = town.numcad
            cadnom = town.cadnom
        else:
            numcad = None
            cadnom = None

        towns.append({
            'idobj': town.idobj,
            'numcom': town.numcom,
            'comnom': town.comnom,
            'numcad': numcad,
            'cadnom': cadnom,
            'nufeco': town.nufeco
        })

    return towns

@view_config(route_name='getTopicsList', renderer='json')
def getTopicsList(request):
    """ Loads the list of the topics."""
    
    results = {}
    results = DBSession.query(Topics).order_by(Topics.topicid.asc()).all()

    topics = []
    for topic in results :
        topics.append({
            'topicid':topic.topicid, 
            'topicname':topic.topicname, 
            'authorityfk':topic.authorityfk, 
            #'publicationdate':topic.publicationdate.isoformat(), 
            'topicorder':topic.topicorder
        })

    return topics

@view_config(route_name='createNewDocEntry', renderer='json')
def createNewDocEntry(request):
    # Attention il faut que l'utilisateur puisse écrire dans la table et d'1, mais aussi qu'il ait le droit sur la SEQUENCE dans PG
    # Généralement si erreur 'waitress' > problème avec PG/droits dans PG
    session = request.session
    #~ Add login to check user
    data = sloads(request.POST['data'])
    
    document = Documents()
    
    if data['numcom']:
        document.nocom = int(data['numcom'])
    else:
        document.nocom = None
    if data['nufeco']:
        document.nufeco = int(data['nufeco'])
    else:
        document.nufeco = None
    if data['numcad']:    
        document.nocad = int(data['numcad'])
    else:
        document.nocad = None
    document.nomcom = data['comnom']
    document.doctype = data['doctype']
    document.topicfk = data['topicfk']
    document.titre = data['titre']
    document.titreofficiel = data['titreofficiel']
    document.abreviation = data['abreviation']
    document.noofficiel = data['noofficiel']
    document.url = data['url']
    document.statutjuridique = data['statutjuridique']
    if data['datesanction']:
        document.datesanction = data['datesanction']
    else:
        document.datesanction = None
    if data['dateabrogation']:
        document.dateabrogation = data['dateabrogation']
    else:
        document.dateabrogation = None
    document.operateursaisie = data['operateursaisie']
    if data['datesaisie']:
        document.datesaisie = data['datesaisie']
    else:
        document.datesaisie = None
    document.canton = data['canton']

    DBSession.add(document)

    DBSession.flush()

    return {'success':True}

@view_config(route_name='getLegalDocuments', renderer='json')
def getLegalDocuments(request):
    """Gets all the legal documents related to a feature.
    """
    legalbases = {}
    legalbases = DBSession.query(LegalBases).order_by(LegalBases.legalbaseid.asc()).all()

    doclist = []
    for legalbase in legalbases :
        doclist.append({
            'documentid':legalbase.legalbaseid,
            'doctype':'legalbase',
            'numcom':legalbase.topicfk, 
            'topicfk':legalbase.title, 
            'title':legalbase.title, 
            'officialtitle':legalbase.officialtitle, 
            'abreviation':legalbase.abreviation, 
            'officialnb':legalbase.officialnb,
            'canton':legalbase.canton,
            'commune':legalbase.commune,
            'documenturl':legalbase.legalbaseurl,
            'legalstate':legalbase.legalstate,
            'publishedsince':legalbase.publishedsince.isoformat()
        })

    legalprovisions = {}
    legalprovisions = DBSession.query(LegalProvisions).order_by(LegalProvisions.legalprovisionid.asc()).all()

    for legalprovision in legalprovisions :
        doclist.append({
            'documentid':legalprovision.legalprovisionid,
            'doctype':'legalprovision',
            'numcom':legalprovision.topicfk, 
            'topicfk':legalprovision.title, 
            'title':legalprovision.title, 
            'officialtitle':legalprovision.officialtitle, 
            'abreviation':legalprovision.abreviation, 
            'officialnb':legalprovision.officialnb,
            'canton':legalprovision.canton,
            'commune':legalprovision.commune,
            'documenturl':legalprovision.legalprovisionurl,
            'legalstate':legalprovision.legalstate,
            'publishedsince':legalprovision.publishedsince.isoformat()
        })

    temporaryprovisions = {}
    temporaryprovisions = DBSession.query(TemporaryProvisions).order_by(TemporaryProvisions.temporaryprovisionid.asc()).all()

    for temporaryprovision in temporaryprovisions :
        doclist.append({
            'documentid':temporaryprovision.temporaryprovisionid,
            'doctype':'temporaryprovsion',
            'numcom':temporaryprovision.topicfk, 
            'topicfk':temporaryprovision.title, 
            'title':temporaryprovision.title, 
            'officialtitle':temporaryprovision.officialtitle, 
            'abreviation':temporaryprovision.abreviation, 
            'officialnb':temporaryprovision.officialnb,
            'canton':temporaryprovision.canton,
            'commune':temporaryprovision.commune,
            'documenturl':temporaryprovision.temporaryprovisionurl,
            'legalstate':temporaryprovision.legalstate,
            'publishedsince':temporaryprovision.publishedsince.isoformat()
        })

    references = {}
    references = DBSession.query(References).order_by(References.referenceid.asc()).all()

    for reference in references :
        doclist.append({
            'documentid':reference.referenceid,
            'doctype':'reference',
            'numcom':reference.topicfk, 
            'topicfk':reference.title, 
            'title':reference.title, 
            'officialtitle':reference.officialtitle, 
            'abreviation':reference.abreviation, 
            'officialnb':reference.officialnb,
            'canton':reference.canton,
            'commune':reference.commune,
            'documenturl':reference.referenceurl,
            'legalstate':reference.legalstate,
            'publishedsince':reference.publishedsince.isoformat()
        })

    return doclist