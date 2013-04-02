# -*- coding: UTF-8 -*-
from pyramid.response import FileResponse, Response
from pyramid.renderers import render_to_response
from pyramid.httpexceptions import HTTPForbidden, HTTPBadRequest
from pyramid.view import view_config
from fpdf import FPDF
from datetime import datetime
import httplib
from owslib.wms import WebMapService
import get_features

import pkg_resources
from geojson import Feature, FeatureCollection, dumps, loads as gloads
from simplejson import loads as sloads,dumps as sdumps
    
from geoalchemy import *    
from crdppf.models import *

# FUNCTIONS
# initialisation
# getFeatureInfoByXY
# getFeatureInfoByID
# getFeatureInfoByAdresse
# getRestrictions
# getMap
# getLegalBases
# getLegalProvisions
# getComplemantaryInformation
# writePDF
# getTitlePage


# Creates empty arrays for the get parameters
def initialisation(self):
    """Sets the default type and values of the global variables"""
    # Creation d'un tableau vide qui accueillit le(s) parametre(s) passé(s) en get
    parametres = {}
    parametres['numcom'] = None
    parametres['numcad'] = None
    parametres['bien_fonds'] = None
    parametres['X'] = None
    parametres['Y'] = None
    
    parcelInfo = {}
    parcelInfo['nummai'] = None
    parcelInfo['idemai'] = None
    parcelInfo['lieu_dit'] = None
    parcelInfo['adresses'] = None
    parcelInfo['numcad'] = None
    parcelInfo['nomcad'] = None
    parcelInfo['numcom'] = None
    parcelInfo['nomcom'] = None
    parcelInfo['nufeco'] = None
    parcelInfo['centerX'] = None
    parcelInfo['centerY'] = None
    parcelInfo['BBOX'] = None
    parcelInfo['geom'] = None
    
    
# Returns the BBOX coordinates of an rectangle
def getBBOX(geometry):
    coordListStr = geometry.split("(")[2].split(")")[0].split(',')
    X = []
    Y = []
    for coordStr in coordListStr:
        X.append(float(coordStr.split(" ")[0]))
        Y.append(float(coordStr.split(" ")[1]))

    bbox = {'minX': min(X), 'minY': min(Y), 'maxX': max(X), 'maxY': max(Y)}
    
    return bbox

# Detects the best paper format and scale in function of the general form and size of the parcel
def getPrintFormat(bbox):
    """This function determines the ideal paper format and scale for the pdf print in dependency of the general form of the selected parcel"""
    
    printFormat = {}
    
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # TO DO : take care of a preselected paper format by the user
    # ===================
    formatChoice = 'A4'

    # Gets the list of all available formats and their parameters : name, orientation, height, width
    paperFormats = DBSession.query(PaperFormats).order_by(PaperFormats.format.desc()).order_by(PaperFormats.scale.asc()).order_by(PaperFormats.orientation.desc()).all()
    fit = 'false'
    fitRatio = 0.9
    ratioW = 0
    ratioH = 0
    # Attention X and Y are standard carthesian and inverted in comparison to the Swiss Coordinate System 
    deltaX = bbox['maxX']-bbox['minX']
    deltaY = bbox['maxY']-bbox['minY']
    resolution = 96
    ratioInchMM =25.4

    # Decides what parcel orientation 
    if deltaX >= deltaY :
        # landscape
        bboxWidth = deltaX
        bboxHeight = deltaY
    else :
        # portrait
        bboxWidth = deltaY
        bboxHeight = deltaX

    # Get the appropriate paper format for the print
    for paperFormat in paperFormats :
        ratioW = bboxWidth*1000/paperFormat.width/paperFormat.scale
        ratioH = bboxHeight*1000/paperFormat.height/paperFormat.scale

        if ratioW <= fitRatio and ratioH <= fitRatio :
            printFormat.update(paperFormat.__dict__)
            printFormat['mapHeight'] = int(printFormat['height']/ratioInchMM*resolution)
            printFormat['mapWidth'] = int(printFormat['width']/ratioInchMM*resolution)
            fit = 'true'
            break
            
    return printFormat


# Intersection d'un polygone de bien_fonds avec les différentes couches pour récuperer
# des informations quant au lieu_dit, le cadastre, la commune et les adresses
def getFeatureInfo(request):
    """The function gets the geometry of a parcel by it's ID and does an overlay with other administrative layers to get the basic parcelInfo and attribute information of the parcel : County, local names, and so on"""
    # hint:
    # for debbuging the query use str(query) in the console/browser window
    # to visualize geom.wkt use session.scalar(geom.wkt)
    
    parcelInfo = {}
    parcelInfo['idemai'] = None
    Y = None
    X = None

    if request.params.get('id') :
        parcelInfo['idemai']  = request.params.get('id')
    elif request.params.get('X') and request.params.get('Y') :
        X =int(request.params.get('X'))
        Y =int(request.params.get('Y'))
    else :
        raise Exception('Aucun bien-fonds répondant à vos critères a pû être trouvé.')

    if parcelInfo['idemai'] is not None :
        queryresult =DBSession.query(ImmeublesCanton).filter_by(idemai=parcelInfo['idemai']).first()
    elif (X > 0 and Y > 0) :
        if  Y > X :
            pointYX = WKTSpatialElement('POINT('+str(Y)+' '+str(X)+')',21781)
        else :
            pointYX = WKTSpatialElement('POINT('+str(X)+' '+str(Y)+')',21781)
        queryresult =DBSession.query(ImmeublesCanton).filter(ImmeublesCanton.geom.gcontains(pointYX)).first()
        parcelInfo['idemai']  = queryresult.idemai
    else : 
        # to define
        return HTTPBadRequest('Aucun bien-fonds n\'a pu être identifié')
        
    parcelInfo['geom'] = queryresult.geom

    queryresult1= DBSession.query(NomLocalLieuDit).filter(NomLocalLieuDit.geom.intersects(parcelInfo['geom'])).first()
    queryresult2= DBSession.query(Cadastre).filter(Cadastre.geom.gcontains(parcelInfo['geom'])).first()
    
    parcelInfo['nummai'] = queryresult.nummai
    parcelInfo['lieu_dit']  = queryresult1.nomloc
    parcelInfo['numcad'] = queryresult2.numcad
    parcelInfo['nomcad'] = queryresult2.cadnom
    parcelInfo['numcom'] = queryresult.numcom
    parcelInfo['nomcom'] = queryresult2.comnom
    parcelInfo['nufeco'] = queryresult2.nufeco
    parcelInfo['centerX'],parcelInfo['centerY'] = DBSession.scalar(queryresult.geom.centroid.x),DBSession.scalar(queryresult.geom.centroid.y)
    parcelInfo['BBOX'] = getBBOX(DBSession.scalar(queryresult.geom.envelope.wkt))
    parcelInfo['printFormat'] = getPrintFormat(parcelInfo['BBOX'])
    
    #adresses = self.getAdresses(parcelInfo['centerX'],parcelInfo['centerY'] )
    #if adresses is not None :
    #    parcelInfo['adresses'] = adresses 

    return parcelInfo


def getRestrictions(parcelInfo) :
    """ Geographic overlay to get all the restrictions within or adjacent to the parcel """	
    geom = parcelInfo['geom']
    restrictions = DBSession.query().all()
    
    return restrictionInfo


def getMap(restriction_layers,crdppf_wms,map_params,pdf_format):
 
    # http://sitn.ne.ch/dev_crdppf/wmscrdppf?SERVICE=WMS&VERSION=1.1.1&REQUEST=GetMap&SRS=EPSG:21781&LAYERS=etat_mo,la3_limites_communales,mo22_batiments,at14_zones_communales&BBOX=559150,203560,559750,203960&WIDTH=600&HEIGHT=400&FORMAT=image/jpeg
    # Creates the pdf file
    pdf_name = 'extrait'
    pdf_name='crdppf_'+pdf_name
    pdfpath = pkg_resources.resource_filename('crdppf','static\public\pdf\\')
    scale = pdf_format['scale']
    
    layers = [
        'parcelles',
        'mo22_batiments',
        'mo21_batiments_provisoires',
        'mo23_batiments_projetes',
        'ag1_parcellaire_provisoire',
        'mo9_immeubles',
        'mo5_point_de_detail',
        'mo14_servitudes_g_surf',
        'mo14_servitudes_g_lig',
        'mo14_servitudes_g_pts',
        'mo14_servitudes_a_surf',
        'mo14_servitudes_a_lig',
        'mo14_servitudes_c_surf',
        'mo14_servitudes_c_surf_autre',
        'mo14_servitudes_c_lig',
        'mo7_obj_divers_lineaire',
        'mo7_obj_divers_couvert',
        'mo7_obj_divers_piscine',
        'mo7_obj_divers_cordbois',
        'mo4_pfa_1',
        'mo4_pfp_3',
#        'mo9_immeubles_txt_rappel',
        'mo4_pfp_1_2',  
        'etat_mo',
        'la3_limites_communales',
        'mo22_batiments',
        restriction_layers
    ]

    #to recenter the map on the bbox of the feature, with the right scale and add at least 10% of space we calculate a wmsBBOX
    wmsBBOX = {}
    wmsBBOX['centerY'] =  int(map_params['bboxCenterY'])
    wmsBBOX['centerX'] =  int(map_params['bboxCenterX'])
    wmsBBOX['minX'] = int(wmsBBOX['centerX']-(pdf_format['width']*scale/1000/2))
    wmsBBOX['maxX'] = int(wmsBBOX['centerX']+(pdf_format['width']*scale/1000/2))
    wmsBBOX['minY'] = int(wmsBBOX['centerY']-(pdf_format['height']*scale/1000/2))
    wmsBBOX['maxY'] = int(wmsBBOX['centerY']+(pdf_format['height']*scale/1000/2))
    
    
    i = 0
    wms = WebMapService(crdppf_wms, version='1.1.1')
    
    for layer in restriction_layers:
        img = wms.getmap(   
            layers=layers,
            srs='EPSG:21781',
            bbox=(wmsBBOX['minX'],wmsBBOX['minY'],wmsBBOX['maxX'],wmsBBOX['maxY']),
            size=(map_params['width'], map_params['height']),
            format='image/png',
            transparent=False
        )
        
        out = open(pdfpath+pdf_name+str(i)+'.png', 'wb')
        out.write(img.read())
        out.close()

    return i
    
    
class ExtraitPDF(FPDF):

    def header(self):

        path = pkg_resources.resource_filename('crdppf','utils\\')
        
        no_page = self.page_no()

        if no_page == 1:
            self.image(path+"Canepo2.jpg",0,0,210,30)
            self.set_y(45)
            self.set_x(149)
            self.image(path+"06ne_ch_RVB.jpg",150,30,43.4,13.8)
            self.set_font('Arial','B',8)
            self.multi_cell(0,3.9,unicode('DEPARTEMENT DE LA GESTION\nDU TERRITOIRE', 'utf-8').encode('iso-8859-1'))
            self.set_font('Arial','',8)
            self.set_x(149)
            self.multi_cell(0,3.9,unicode('SERVICE DE LA GÉOMATIQUE ET\nDU REGISTRE FONCIER', 'utf-8').encode('iso-8859-1'))
            
    def footer(self):
        # position footer at 15mm from the bottom
        self.set_y(-20)
        self.set_font('Arial','',7);
        self.cell(0,10,'RUE DE TIVOLI 22, CH-2003 NEUCHATEL 3   TEL. 032 889 67 50   FAX 032 889 61 21   SGRF@NE.CH  WWW.NE.CH/SGRF',0,0,'C');

#~ def getTitlePage(request):
    #~ return
    
@view_config(route_name='create_extrait')
def create_extrait(request):
    # to get vars defined in the buildout  use : request.registry.settings['key']
    crdppf_wms = request.registry.settings['crdppf_wms']
    sld_url = request.registry.settings['sld_url']

    # the dictionnary for the document
    reportInfo = {}
    reportInfo['type'] = '[officiel]'
    
    # the dictionnary for the parcel
    featureInfo = {}
    featureInfo['no_EGRID'] = 'xxxxx'
    featureInfo['CoordSys'] = 'MN03'
    featureInfo['lastUpdate'] = datetime.now()
    featureInfo['operator'] = 'F.Voisard - SITN'

    # If the ID of the parcel is set get the basic attributs else get the ID (idemai) of the selected parcel first using X/Y coordinates of the center 
    featureInfo.update(getFeatureInfo(request)) # '1_14127' # test parcel or '1_11340'
    
    # temporary variables for developping purposes - will be assigned by DB requests
    restriction_layers = ['affectation','canepo','foret']

 
    map_params = {'width':featureInfo['printFormat']['mapWidth'],'height':featureInfo['printFormat']['mapHeight']}
    map_params['bboxCenterX'] = (featureInfo['BBOX']['maxX']+featureInfo['BBOX']['minX'])/2
    map_params['bboxCenterY'] = (featureInfo['BBOX']['maxY']+featureInfo['BBOX']['minY'])/2

    pdf_format = featureInfo['printFormat']
    
    # Creates the pdf file
    pdf_name = 'extrait'
    pdf_name='crdppf_'+pdf_name
    pdfpath = pkg_resources.resource_filename('crdppf','static\public\pdf\\')
    
    today= datetime.now()

    competentAuthority = DBSession.query(Authority).all()
    crdppfTopics = DBSession.query(Topics).all()

    result = {}
    params = {'id':featureInfo['idemai'],'layerList':'at14_zones_communales'}
    for crdppfTopic in crdppfTopics :
        result['restriction'] = get_features.get_features_function(params)
        if crdppfTopic.topicid == '73':
            result['map'] = getMap(params['layerList'],crdppf_wms,map_params,pdf_format)
        # getLegalBases()
        # getLegalProvisions()
        # getComplemantaryInformation()


    # Create order PDF
    pdf = ExtraitPDF()
    #pdf=FPDF(format='A4')    
    
    # START TITLEPAGE
    pdf.add_page()
    pdf.set_margins(25,25,25)
    path = pkg_resources.resource_filename('crdppf','utils\\')

    # PageTitle
    pdf.set_y(70)
    pdf.set_font('Arial','B',28)
    pdf.multi_cell(0,12,unicode('Extrait '+reportInfo['type'] , 'utf-8').encode('iso-8859-1'))
    pdf.set_font('Arial','B',22)
    pdf.multi_cell(0,12,unicode('du cadastre des restrictions de\ndroit public à la propriété foncière', 'utf-8').encode('iso-8859-1'))
    pdf.ln()
    pdf.ln()
    
    # First infoline
    pdf.set_font('Arial','B',12)
    pdf.cell(37,5,unicode("Bien-fonds n°", 'utf-8').encode('iso-8859-1'),0,0,'L')
    pdf.cell(3,5,unicode(": ", 'utf-8').encode('iso-8859-1'),0,0,'L')
    pdf.cell(50,5,featureInfo['nummai'].encode('iso-8859-1'),0,0,'L')
    pdf.cell(37,5,unicode("N° EGRID", 'utf-8').encode('iso-8859-1'),0,0,'L')
    pdf.cell(3,5,unicode(": ", 'utf-8').encode('iso-8859-1'),0,0,'L')
    pdf.cell(50,5,featureInfo['no_EGRID'].encode('iso-8859-1'),0,1,'L')
    
     # Second infoline   
    pdf.cell(37,5,unicode("Cadastre", 'utf-8').encode('iso-8859-1'),0,0,'L')
    pdf.cell(3,5,unicode(": ", 'utf-8').encode('iso-8859-1'),0,0,'L')
    pdf.cell(50,5,featureInfo['nomcad'].encode('iso-8859-1'),0,1,'L')
    
    # Third infoline
    pdf.cell(37,5,unicode('Commune', 'utf-8').encode('iso-8859-1'),0,0,'L')
    pdf.cell(3,5,unicode(": ", 'utf-8').encode('iso-8859-1'),0,0,'L')
    pdf.cell(50,5,featureInfo['nomcom'].encode('iso-8859-1'),0,0,'L')
    pdf.cell(37,5,unicode('N° OFS', 'utf-8').encode('iso-8859-1'),0,0,'L')
    pdf.cell(3,5,unicode(": ", 'utf-8').encode('iso-8859-1'),0,0,'L')
    pdf.cell(50,5,str(featureInfo['nufeco']).encode('iso-8859-1'),0,1,'L')

    pdf.set_y(165)
    pdf.set_font('Arial','B',10)
    pdf.cell(65,5,unicode('Extrait établi le', 'utf-8').encode('iso-8859-1'),0,0,'L')
    pdf.cell(40,5, ': '+today.strftime('%d.%m.%Y - %Hh%M'),0,1,'L')
    pdf.cell(65,5,unicode('Dernière mise à jour des données', 'utf-8').encode('iso-8859-1'),0,0,'L')
    pdf.cell(40,5,': '+featureInfo['lastUpdate'].strftime('%d.%m.%Y'),0,1,'L')
    pdf.cell(65,5,unicode('Editeur de l\'extrait', 'utf-8').encode('iso-8859-1'),0,0,'L')
    pdf.cell(40,5,': '+featureInfo['operator'].encode('iso-8859-1'),0,1,'L')

    pdf.set_y(190)
    pdf.cell(65,5,unicode('Etat des données de la MO', 'utf-8').encode('iso-8859-1'),0,0,'L')
    pdf.cell(40,5,unicode(':', 'utf-8').encode('iso-8859-1'),0,1,'L')
    pdf.cell(65,5,unicode('Cadre de référence', 'utf-8').encode('iso-8859-1'),0,0,'L')
    pdf.cell(40,5,': '+featureInfo['CoordSys'].encode('iso-8859-1'),0,1,'L')


    pdf.image(path+"Neuchatel.jpg",180,180,20,22)

    pdf.set_y(215)
    pdf.set_font('Arial','',10)
    pdf.cell(0,5,unicode('Signature', 'utf-8').encode('iso-8859-1'),0,0,'L')

    pdf.set_y(240)
    pdf.set_font('Arial','B',10)
    pdf.cell(0,5,unicode('Indications générales', 'utf-8').encode('iso-8859-1'),0,1,'J')
    pdf.set_font('Arial','',10)
    pdf.multi_cell(0,5,unicode('Mise en garde : Le canton de Neuchâtel n\'engage pas sa responsabilité sur l\'exactitude ou la fiabilité des documents législatifs dans leur version électronique. Ces documents ne créent aucun autre droit ou obligation que ceux qui découlent des textes légalement adoptés et publiés, qui font seuls foi.', 'utf-8').encode('iso-8859-1'),0,1,'L')

    # END TITLEPAGE

    layers= [    
        'la3_limites_communales',
        'at14_zones_communales',
        'at08_zones_cantonales',
        'mo22_batiments',
        'mo21_batiments_provisoires',
        'mo9_immeubles',
        'ag1_parcellaire_provisoire'
    ]

    wms = WebMapService(crdppf_wms, version='1.1.1')
    img = wms.getmap(   
        layers=layers,
        srs='EPSG:21781',
        bbox=(559150,203560,559750,203960),
        size=(map_params['width'], map_params['height']),
        format='image/jpeg',
        transparent=False
    )

    out = open(pdfpath+pdf_name+'.jpg', 'wb')
    out.write(img.read())
    out.close()

    layers2= [
        'parcelles',
        'en07_canepo_accidents',
        'en07_canepo_entreprises',
        'en07_canepo_decharges'
    ]    
    #~ layers2= [
        #~ 'ch.bazl.segelflugkarte',
        #~ 'ch.bazl.projektierungszonen-flughafenanlage'
    #~ ]
    
    #http://sitn.ne.ch/ogc-sitn-poi/wms?SERVICE=WMS&VERSION=1.1.1&REQUEST=GetMap&SRS=EPSG:21781&LAYERS=en07_canepo_accidents,en07_canepo_entreprises,en07_canepo_decharges&BBOX=559150,203560,559750,203960&WIDTH=600&HEIGHT=400&FORMAT=image/png
    #wms2 = WebMapService('http://wms.geo.admin.ch/', version='1.1.1')
    #~ wms2 = WebMapService(crdppf_wms, version='1.1.1')
    #~ img2 = wms2.getmap(   
        #~ layers=layers2,
        #~ srs='EPSG:21781',
        #~ bbox=(559150,203560,559750,203960),
        #~ size=(bbox['width'], bbox['height']),
        #~ #bbox=(640000, 200000,750000,280000),
        #~ #size=(800,582),
        #~ format='image/png',
        #~ transparent=False
    #~ )

    #~ out2 = open(pdfpath+ pdf_name+'2.png', 'wb')
    #~ out2.write(img2.read())
    #~ out2.close()
    
    # PAGE 2 
    pdf.add_page()
    pdf.set_y(25)
    pdf.set_font('Arial','B',16)
    pdf.multi_cell(0,6,'73 - Plan d\'affectation')
    
    # Attributes of topic layers intersection
    pdf.set_y(35)
    pdf.set_font('Arial','B',10)
    pdf.cell(50,6,unicode('Nom de la zone', 'utf-8').encode('iso-8859-1'),0,0,'L')
    pdf.set_font('Arial','',10)
    pdf.multi_cell(0,3.9,unicode(':  Zone d\'habitation / secteur d\'ordre non-contigu 1.2','utf-8').encode('iso-8859-1'),0,1,'L')
    pdf.set_font('Arial','B',10)
    pdf.cell(50,6,unicode('Surface', 'utf-8').encode('iso-8859-1'),0,0,'L')
    pdf.set_font('Arial','',10)
    pdf.multi_cell(0,6,unicode(':  712 m2','utf-8').encode('iso-8859-1'),0,1,'L')
    
    pdf.set_draw_color(200,200,200)
    pdf.set_line_width(0.4)
    y = pdf.get_y()
    pdf.line(25,y+1,185,y+1)
    
    # Legal Provisions
    pdf.set_y(y+5)
    pdf.set_font('Arial','B',10)
    pdf.cell(50,6,unicode('Dispositions juridiques', 'utf-8').encode('iso-8859-1'),0,0,'L')
    pdf.set_font('Arial','',10)
    pdf.multi_cell(0,6,unicode(':  Le règlement de construction est donné à l\'annexe 1','utf-8').encode('iso-8859-1'),0,1,'L')


    pdf.set_draw_color(200,200,200)
    pdf.set_line_width(0.4)
    y = pdf.get_y()
    pdf.line(25,y+1,185,y+1)

    # Assent date
    pdf.set_y(y+5)
    pdf.set_font('Arial','B',10)
    pdf.cell(47,6,unicode('Sanction par le Conseil d\'Etat', 'utf-8').encode('iso-8859-1'),0,0,'L')
    pdf.cell(3,6,unicode(':', 'utf-8').encode('iso-8859-1'),0,0,'L')
    pdf.set_font('Arial','',10)
    pdf.cell(3,6,unicode('5 juillet 1999 et 13 juin 2001', 'utf-8').encode('iso-8859-1'),0,1,'L')

    pdf.set_draw_color(200,200,200)
    y = pdf.get_y()
    pdf.line(25,y+1,185,y+1)

    # Complementary provisions and information
    pdf.set_y(y+5)
    pdf.set_font('Arial','B',10)
    pdf.cell(0,6,unicode('Infos et renvois supplémentaires', 'utf-8').encode('iso-8859-1'),0,1,'L')
    pdf.set_font('Arial','',10)
    pdf.set_x(35)
    pdf.multi_cell(0,6,unicode('-  Plan spécial \"Gare Nord\"\n-  Plan de quartier \"Les Fahys\"','utf-8').encode('iso-8859-1'),0,1,'L')

    pdf.set_draw_color(200,200,200)
    y = pdf.get_y()
    pdf.line(25,y+1,185,y+1)

    # Competent Authority
    y = pdf.get_y()
    pdf.set_y(y+5)
    pdf.set_font('Arial','B',10)
    pdf.cell(47,3.9,unicode('Service compétent', 'utf-8').encode('iso-8859-1'),0,0,'L')
    pdf.cell(3,3.9,unicode(': ', 'utf-8').encode('iso-8859-1'),0,0,'L')
    pdf.set_font('Arial','',10)
    pdf.multi_cell(120,3.9,unicode('Commune de Neuchâtel\nENVIRONNEMENT - Service de l\'aménagement urbain\nFbg du Lac 3\n2000 Neuchâtel\nTél: 032 717\'76\'61\nE-Mail: urbanisme.neuchatel@ne.ch', 'utf-8').encode('iso-8859-1'),0,1,'L')
    pdf.set_font('Arial','B',10)
    pdf.cell(47,6,unicode('Personne de contact', 'utf-8').encode('iso-8859-1'),0,0,'L')
    pdf.cell(3,6,unicode(': ', 'utf-8').encode('iso-8859-1'),0,0,'L')
    pdf.set_font('Arial','',10)
    pdf.cell(120,6,unicode('Fabien Coquillat', 'utf-8').encode('iso-8859-1'),0,1,'L')
    
    pdf.set_draw_color(200,200,200)
    y = pdf.get_y()
    pdf.line(25,y+1,185,y+1)

    # Legal bases
    pdf.set_y(y+5)
    pdf.set_font('Arial','B',10)
    pdf.cell(47,6,unicode('Base(s) légale(s)', 'utf-8').encode('iso-8859-1'),0,0,'L')
    pdf.cell(3,6,unicode(': ', 'utf-8').encode('iso-8859-1'),0,0,'L')
    pdf.set_font('Arial','',10)
    pdf.multi_cell(0,3.9,unicode('RS 700 Loi fédérale sur l\'aménagement du territoire (art. 14, 26)\nRSN 701.0 Loi cantonale sur l\'aménagement du territoire (art. 43 al. 2 lit a, 45-64a)','utf-8').encode('iso-8859-1'),0,1,'L')
    
    pdf.set_draw_color(200,200,200)
    pdf.set_line_width(0.4)
    y = pdf.get_y()
    pdf.line(25,y+1,185,y+1)

    pdf.set_y(y+5)
    pdf.set_font('Arial','B',10)
    pdf.cell(47,6,unicode('Dispositions transitoires', 'utf-8').encode('iso-8859-1'),0,0,'L')
    pdf.cell(3,6,unicode(': ', 'utf-8').encode('iso-8859-1'),0,0,'L')
    pdf.set_font('Arial','',10)
    pdf.multi_cell(0,3.9,unicode('Plan d\'affectation Quartier Nord du 21 décembre 1975\nValable jusqu\'au 31.12.2013','utf-8').encode('iso-8859-1'),0,1,'L')
    
    # Thematic map
    pdf.add_page(str(pdf_format['orientation'] + ','+pdf_format['format']))
    pdf.set_font('Arial','B',16)
    pdf.multi_cell(0,6,'73 - Plan d\'affectation')
    y = pdf.get_y()
    pdf.image(pdfpath+pdf_name+str(result['map'])+'.png',10,y+5,pdf_format['width'] ,pdf_format['height'] )
    pdf.ln()

    # PAGE 3
    pdf.add_page()
    pdf.set_y(25)
    pdf.set_font('Arial','B',16)
    pdf.multi_cell(0,6,unicode('116 Cadastre des sites pollués','utf-8').encode('iso-8859-1'))
    pdf.ln()
    
    # PAGE 4
    pdf.add_page()
    pdf.set_font('Arial','B',16)
    pdf.multi_cell(0,6,unicode('131 Zones de protection des eaux souterraines','utf-8').encode('iso-8859-1'))
    #pdf.image(pdf_name+'2.png',20,35,90,70)
    pdf.ln()
    
    # Write pdf file to disc
    pdf.output(pdfpath+pdf_name+'.pdf','F')
    
    response = FileResponse(
        pdfpath + pdf_name + '.pdf',
        request,
        None,
        'application/pdf'
    )
    response. content_disposition='attachment; filename='+ pdf_name +'.pdf'
    return response
    
def dummyFunctionForUnusedCode():
  
    #~ conn = httplib.HTTPConnection("wms.geo.admin.ch")
    #~ filter1 = '/?lang=fr&QUERY_LAYERS=ch.bazl.projektierungszonen-flughafenanlagen&LAYERS=ch.bazl.projektierungszonen-flughafenanlagen&VERSION=1.1.1&SERVICE=WMS&REQUEST=GetFeatureInfo&SRS=EPSG%3A21781&INFO_FORMAT=text/plain&BBOX=680153.65034247,256316,684977.65034247,257741&WIDTH=2412&HEIGHT=712&X=1206&Y=355'
    #~ conn.request("GET",filter1)
    #~ r1 = conn.getresponse()
    #~ query = r1.read()


    #~ layers3= [
        #~ 'ch.bazl.segelflugkarte',
        #~ 'ch.bazl.projektierungszonen-flughafenanlage'
    #~ ]
    
    #~ #http://sitn.ne.ch/ogc-sitn-poi/wms?SERVICE=WMS&VERSION=1.1.1&REQUEST=GetMap&SRS=EPSG:21781&LAYERS=en07_canepo_accidents,en07_canepo_entreprises,en07_canepo_decharges&BBOX=559150,203560,559750,203960&WIDTH=600&HEIGHT=400&FORMAT=image/png
    #~ wms3 = WebMapService('http://wms.geo.admin.ch/', version='1.1.1')
    #~ img3 = wms3.getmap(   
        #~ layers=layers3,
        #~ srs='EPSG:21781',
        #~ bbox=(640000, 200000,750000,280000),
        #~ size=(800,582),
        #~ format='image/png',
        #~ transparent=False
    #~ )

    #~ out3 = open(pdfpath+ pdf_name+'3.png', 'wb')
    #~ out3.write(img3.read())
    #~ out3.close()

    #~ toto = 'ola'

    #~ if toto == 'ola' :
        #~ return HTTPBadRequest(detail='C\'est faux, car:'+toto)
        
    return true