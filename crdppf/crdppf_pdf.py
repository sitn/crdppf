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
import urllib

import pkg_resources
from geojson import Feature, FeatureCollection, dumps, loads as gloads
from simplejson import loads as sloads,dumps as sdumps
    
from geoalchemy import *    
from crdppf.models import *

# FUNCTIONS
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
    paperFormats = DBSession.query(PaperFormats).filter_by(orientation='portrait').order_by(PaperFormats.format.desc()).order_by(PaperFormats.scale.asc()).order_by(PaperFormats.orientation.desc()).all()
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
        raise Exception('Aucun immeuble répondant à vos critères a pû être trouvé.')

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
        return HTTPBadRequest('Aucun immeuble n\'a pu être identifié')
        
    parcelInfo['geom'] = queryresult.geom
    parcelInfo['area'] = int(DBSession.scalar(queryresult.geom.area))

    queryresult1= DBSession.query(NomLocalLieuDit).filter(NomLocalLieuDit.geom.intersects(parcelInfo['geom'])).first()
    queryresult2= DBSession.query(Cadastre).filter(Cadastre.geom.buffer(1).gcontains(parcelInfo['geom'])).first()
    
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


def getMap(restriction_layers,topicid,crdppf_wms,map_params,pdf_format):
 
    # http://sitn.ne.ch/dev_crdppf/wmscrdppf?SERVICE=WMS&VERSION=1.1.1&REQUEST=GetMap&SRS=EPSG:21781&LAYERS=etat_mo,la3_limites_communales,mo22_batiments,at14_zones_communales&BBOX=559150,203560,559750,203960&WIDTH=600&HEIGHT=400&FORMAT=image/jpeg
    # Creates the pdf file
    pdf_name = 'extract'
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
        #~ 'mo14_servitudes_g_surf',
        #~ 'mo14_servitudes_g_lig',
        #~ 'mo14_servitudes_g_pts',
        #~ 'mo14_servitudes_a_surf',
        #~ 'mo14_servitudes_a_lig',
        #~ 'mo14_servitudes_c_surf',
        #~ 'mo14_servitudes_c_surf_autre',
        #~ 'mo14_servitudes_c_lig',
        'mo7_obj_divers_lineaire',
        'mo7_obj_divers_couvert',
        'mo7_obj_divers_piscine',
        'mo7_obj_divers_cordbois',
        'mo4_pfa_1',
        'mo4_pfp_3',
        #'mo9_immeubles_txt_rappel',
        'mo4_pfp_1_2',  
        'la3_limites_communales',
        'mo22_batiments'
    ]
    
    legend_layers = []
    legend_path = []

    for layer in restriction_layers:
        # Compile the layer list for the wms
        layers.append(layer.layername)
        
        #~ # in the same time create the legend graphic for each layer
        #~ legend = open(pdfpath+str('legend_')+str(layer.layername)+'.png', 'wb')
        #~ img = urllib.urlopen(crdppf_wms +str('?TRANSPARENT=TRUE&SERVICE=WMS&VERSION=1.1.1&REQUEST=GetLegendGraphic&FORMAT=image%2Fpng&LAYER='+str(layer.layername)))
        #~ legend.write(img.read())
        #~ legend.close()
        #~ legend_path.append(pdfpath+str('legend_')+str(layer.layername))
    
    #to recenter the map on the bbox of the feature, with the right scale and add at least 10% of space we calculate a wmsBBOX
    wmsBBOX = {}
    wmsBBOX['centerY'] =  int(map_params['bboxCenterY'])
    wmsBBOX['centerX'] =  int(map_params['bboxCenterX'])
    wmsBBOX['minX'] = int(wmsBBOX['centerX']-(pdf_format['width']*scale/1000/2))
    wmsBBOX['maxX'] = int(wmsBBOX['centerX']+(pdf_format['width']*scale/1000/2))
    wmsBBOX['minY'] = int(wmsBBOX['centerY']-(pdf_format['height']*scale/1000/2))
    wmsBBOX['maxY'] = int(wmsBBOX['centerY']+(pdf_format['height']*scale/1000/2))
    
    
    wms = WebMapService(crdppf_wms, version='1.1.1')
    
    map = wms.getmap(   
        layers=layers,
        srs='EPSG:21781',
        bbox=(wmsBBOX['minX'],wmsBBOX['minY'],wmsBBOX['maxX'],wmsBBOX['maxY']),
        size=(map_params['width'], map_params['height']),
        format='image/png',
        transparent=False
    )
    
    out = open(pdfpath+pdf_name+str(topicid)+'.png', 'wb')
    out.write(map.read())
    out.close()
    mappath = pdfpath+pdf_name+str(topicid)+'.png'
  
        
    return mappath,legend_path

class Objectify:
    def __init__(self, **kwds):
        self.__dict__.update(kwds)


class ExtractPDF(FPDF):
    # =============================
    # VARIABLES :
    # extract  = principal array holding all the data needed to create the pdf extract converted to an object to simplify the acces to the nested data
    # extract.featureInfo
    # extract.topicList
    # extract.pdfFormat
    # extract.mapFormat
    # =============================
    #~ def alias_title(self,i, alias='{title}'):
        #~ "Define an alias for total number of pages"
        #~ self.str_alias_title[i]=alias
        #~ return alias
        
    def __init__(self):
        FPDF.__init__(self)
        self.toc_entries = []
        self.appendix_entries = []

    def alias_nomcom(self, alias='{nomcom}'):
        "Define an alias for the county name"
        self.str_alias_nomcom=alias
        return alias
        
    def alias_no_page(self, alias='{no_pg}'):
        "Define an alias for total number of pages"
        self.str_alias_no_page=alias
        return alias
        
    def header(self):
        path = pkg_resources.resource_filename('crdppf','static\images\\')
        
        no_page = self.page_no()
        nb_pages = self.alias_nb_pages()
        nomcom = self.alias_nomcom()

        self.set_line_width(0.3)
        self.line(105,5,105,34)
        self.line(165,5,165,34)
        self.image(path+"ecussons\logoCH.png",10,8,55,31.03)
        self.image(path+"06ne_ch_RVB.jpg",108,8,43.4,13.8)
        self.image(path+'ecussons\Neuchatel.jpg',170,8,10,10.7)
        self.set_xy(170,19.5)
        self.set_font('Helvetica','',7)
        self.cell(30,3,unicode(nomcom,'utf-8').encode('iso-8859-1'),0,0,'L')

            
    def footer(self):
        # position footer at 15mm from the bottom     
        self.set_y(-20)
        self.set_font('Helvetica','',7);
        self.cell(0,10,unicode('Date d\'établissement :         ID Nr : 123456789           Page : ','utf-8').encode('iso-8859-1')+str(self.alias_no_page())+str('/')+str(self.alias_nb_pages()),0,0,'C');


    def add_toc_entry(self,num,label,r,g,b):
        self.toc_entries.append({'no_page':num,'title':label,'r':int(r),'g':int(g),'b':int(b)})

    def add_appendix(self,num,label,url):
        self.appendix_entries.append({'no_page':num,'title':label,'url':url})
        
#~ class PDFExtract(extract):

    #~ toclist ={}
    
    #~ # Add a line in the Table of Content
    #~ def addTOCEntry(count,title,page_no):
        #~ toclist[count] = {'title':title,'page':page_no}
        #~ return toclist   
     
    #~ # Creates the title page of the extract
    #~ def createTitlePage(featureInfo):

        #~ # Create PDF extract
        #~ title_page = ExtractPDF()
        
        #~ # START TITLEPAGE
        #~ title_page.add_page()
        #~ title_page.set_margins(25,25,25)
        #~ title_page = pkg_resources.resource_filename('crdppf','utils\\')

        #~ # PageTitle
        #~ title_page.set_y(70)
        #~ title_page.set_font('Helvetica','B',28)
        #~ title_page.multi_cell(0,12,unicode('Extrait ' , 'utf-8').encode('iso-8859-1'))
        #~ title_page.set_font('Helvetica','B',22)
        #~ title_page.multi_cell(0,12,unicode('du cadastre des restrictions de\ndroit public à la propriété foncière', 'utf-8').encode('iso-8859-1'))
        #~ title_page.ln()
        #~ title_page.ln()
        
        #~ return title_page
        
    #~ # Creates the 
    #~ def createTOC(titles):
        
        #~ if titles :
            #~ for title in titles:
                #~ toc_page.cell(37,5,title['title'].encode('iso-8859-1'),0,0,'L')
                #~ toc_page.cell(3,5,unicode(" ", 'utf-8').encode('iso-8859-1'),0,0,'L')
                #~ toc_page.cell(50,5,title['page'].encode('iso-8859-1'),0,1,'R')
        #~ else :
                #~ toc_page.cell(37,5,'Document vide!'.encode('iso-8859-1'),0,0,'L')
                #~ toc_page.cell(3,5,unicode(" ", 'utf-8').encode('iso-8859-1'),0,0,'L')
                #~ toc_page.cell(50,5,'... 0',0,1,'R')
        #~ return toc_page

    #~ def createThematicPages(extract):
        
        #~ # Thematic pages
        #~ for crdppfTopic in extract.topicList :
            #~ if crdppfTopic.layers :
                #~ layers = []    
                #~ for layer in crdppfTopic.layers:
                    #~ layers.append(layer.layername)          
                #~ if isinstance(layers, list):
                    #~ for sublayer in layers:
                        #~ params ={'id':featureInfo['idemai'],'layerList':str(sublayer)}
                        #~ extract.restrictionList = get_features.get_features_function(params)
                #~ else:
                    #~ params = {'id':featureInfo['idemai'],'layerList':str(layers)}
                    #~ extract.restrictionList = get_features.get_features_function(params)
            #~ else : 
                #~ extract.restrictionList = None

           #~ # PAGE X 
            #~ thematic_pages.add_page()
            #~ thematic_pages.set_y(55)
            #~ thematic_pages.set_font('Helvetica','B',16)
            #~ thematic_pages.multi_cell(0,6,str(crdppfTopic.topicid) +' - '+str(crdppfTopic.topicname.encode('iso-8859-1')),0,1,'L')
                
            #~ # Create entry in TOC
            #~ toclist = addTOCEntry(i,crdppfTopic.topicname,thematic_page.page_no())

            #~ if extract.restrictionList :
                #~ y = thematic_pages.get_y()
                #~ thematic_pages.set_y(y+10)
                #~ thematic_pages.set_font('Helvetica','B',12)
                #~ thematic_pages.cell(50,6,unicode('Restriction(s) touchant l\'immeuble', 'utf-8').encode('iso-8859-1'),0,1,'L')
                
                #~ y = thematic_pages.get_y()
                #~ thematic_pages.set_y(y+5)

                #~ for feature in extract.restrictionList:
                    #~ if feature['properties'] :
                        
                        #~ if feature['properties']['layerName']:
                            #~ thematic_pages.set_font('Helvetica','B',11)
                            #~ thematic_pages.cell(100,6,unicode('Nom de la donnée : ','utf-8').encode('iso-8859-1') +feature['properties']['layerName'].encode('iso-8859-1'),0,1,'L') 

                        #~ if feature['properties']['featureClass']:
                            #~ thematic_pages.set_font('Helvetica','I',10)
                            #~ thematic_pages.cell(100,6,unicode('Type d\'interaction : ','utf-8').encode('iso-8859-1') + feature['properties']['featureClass'].encode('iso-8859-1'),0,1,'L') 
                            
                        #~ # Attributes of topic layers intersection
                        #~ for key,value in feature['properties'].iteritems():
                            #~ if value is not None :
                                #~ if key !='layerName' and key != 'featureClass':
                                    #~ thematic_pages.set_font('Helvetica','B',10)
                                    #~ thematic_pages.cell(60,4.5,key.encode('iso-8859-1'),0,0,'L')
                                    #~ thematic_pages.set_font('Helvetica','',10)
                                    #~ if isinstance(value, float) or isinstance(value, int):
                                        #~ value = str(value)
                                    #~ thematic_pages.multi_cell(0,4.5,value.encode('iso-8859-1'),0,1,'L')
                    #~ y =thematic_pages.get_y()
                    #~ thematic_pages.set_y(y+5)
                    
            #~ else :
                #~ y = thematic_pages.get_y()
                #~ thematic_pages.set_y(y+10)
                #~ thematic_pages.set_font('Helvetica','B',12)
                #~ thematic_pages.cell(50,6,unicode('Aucune restriction pour ce thème', 'utf-8').encode('iso-8859-1'),0,1,'L')
                #~ y = thematic_pages.get_y()            
                #~ thematic_pages.set_y(y+5)
                
            #~ # Legal Provisions
            #~ y = thematic_pages.get_y()
            #~ thematic_pages.set_y(y+5)
            #~ thematic_pages.set_font('Helvetica','B',10)
            #~ thematic_pages.cell(50,6,unicode('Dispositions juridiques', 'utf-8').encode('iso-8859-1'),0,0,'L')
            #~ thematic_pages.set_font('Helvetica','',10)
            #~ thematic_pages.multi_cell(0,6,unicode(':  Le règlement de construction est donné à l\'annexe 1','utf-8').encode('iso-8859-1'),0,1,'L')
        
        #~ return thematic_pages

    #~ featureInfo = 'bla'
    #~ extract = createTitlePage(featureInfo)
    #~ #extract.update(createTitlePage())
    
    #~ extract.output(pdfpath+'extract.pdf','F')
    
    #~ response = FileResponse(
        #~ pdfpath + 'extract.pdf',
        #~ request,
        #~ None,
        #~ 'application/pdf'
    #~ )
    #~ response. content_disposition='attachment; filename='+ 'extract.pdf'
    #~ return response
    
def getAppendices():

    appendix_pages = ExtractPDF()
    
    # START APPENDIX
    appendix_pages.add_page()
    appendix_pages.set_margins(25,55,25)
    appendix_pages.set_y(55)
    appendix_pages.set_font('Helvetica','B',16)
    appendix_pages.multi_cell(0,12,unicode('Liste des annexes', 'utf-8').encode('iso-8859-1'))
    
    appendix_pages.set_font('Helvetica','B',11)
    appendix_pages.cell(15,6,str('Page'),0,0,'L')
    appendix_pages.cell(135,6,str('Titre de l\'annexe').encode('iso-8859-1'),0,1,'L')
    
    return appendix_pages
    
def getTOC():

    toc_pages = ExtractPDF()
    
    # START TOC
    toc_pages.add_page()
    toc_pages.set_margins(25,55,25)
    toc_pages.set_y(55)
    toc_pages.set_font('Helvetica','B',16)
    toc_pages.multi_cell(0,12,unicode('Table des matières', 'utf-8').encode('iso-8859-1'))

    toc_pages.set_font('Helvetica','B',10)
    toc_pages.cell(12,30,str(''),'R',0,'L')
    toc_pages.cell(118,30,str('').encode('iso-8859-1'),'LR',0,'L')
    toc_pages.cell(15,30,str(''),'LR',0,'C')
    toc_pages.cell(15,30,str(''),'L',1,'C')
    toc_pages.cell(12,5,str('Page'),'RB',0,'L')
    toc_pages.cell(118,5,str('Restriction').encode('iso-8859-1'),'LBR',0,'L')
    toc_pages.cell(15,5,str('Disp.jur.'),'LBR',0,'C')
    toc_pages.cell(15,5,str('Renvois'),'LB',1,'C')

    return toc_pages


def getTitlePage(feature_info,crdppf_wms,sld_url,pdf_path,nomcom):

    # the dictionnary for the document
    reportInfo = {}
    reportInfo['type'] = '[officiel]'
    
    # the dictionnary for the parcel
    feature_info['no_EGRID'] = 'Placeholder'
    feature_info['lastUpdate'] = datetime.now()
    feature_info['operator'] = 'F.Voisard - SITN'

    today= datetime.now()
    
    # Create PDF extract
    pdf = ExtractPDF()
    
    # START TITLEPAGE
    pdf.add_page()
    pdf.set_margins(25,55,25)
    path = pkg_resources.resource_filename('crdppf','utils\\')

    # PageTitle
    pdf.set_y(55)
    pdf.set_font('Helvetica','B',24)
    pdf.multi_cell(0,10,unicode('Extrait '+reportInfo['type'] , 'utf-8').encode('iso-8859-1'))
    pdf.set_font('Helvetica','B',20)
    pdf.multi_cell(0,8,unicode('du cadastre des restrictions de\ndroit public à la propriété foncière', 'utf-8').encode('iso-8859-1'))
    pdf.ln()
  
    # Create order sld
    sld = u"""<?xml version="1.0" encoding="UTF-8"?>
<sld:StyledLayerDescriptor version="1.0.0" xmlns="http://www.opengis.net/ogc" xmlns:sld="http://www.opengis.net/sld" xmlns:ogc="http://www.opengis.net/ogc" xmlns:gml="http://www.opengis.net/gml" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.opengis.net/sld http://schemas.opengis.net/sld/1.0.0/StyledLayerDescriptor.xsd">
<sld:NamedLayer>
<sld:Name>parcelles</sld:Name>
<sld:UserStyle>
<sld:Name>propertyIsEqualTo</sld:Name>
<sld:Title>propertyIsEqualTo</sld:Title>
<sld:FeatureTypeStyle>
<sld:Rule>	
<ogc:Filter>
<ogc:PropertyIsEqualTo>
<ogc:PropertyName>idemai</ogc:PropertyName>
<ogc:Literal>"""
    sld += str(feature_info['idemai'])
    sld += u"""</ogc:Literal>
</ogc:PropertyIsEqualTo>
</ogc:Filter>					
<sld:PolygonSymbolizer>
<sld:Stroke>
<sld:CssParameter name="stroke">#ff0000</sld:CssParameter>
<sld:CssParameter name="stroke-opacity">1</sld:CssParameter>
<sld:CssParameter name="stroke-width">4</sld:CssParameter>
</sld:Stroke>
</sld:PolygonSymbolizer>
<sld:TextSymbolizer>
<sld:Label>
<ogc:PropertyName>nummai</ogc:PropertyName>							
</sld:Label> 
<sld:Font>
<sld:CssParameter name="font-family">Arial</sld:CssParameter> 
<sld:CssParameter name="font-weight">bold</sld:CssParameter> 
<sld:CssParameter name="font-size">8</sld:CssParameter> 
</sld:Font>
<sld:Fill>
<sld:CssParameter name="fill">#000000</sld:CssParameter> 
</sld:Fill>
</sld:TextSymbolizer>
</sld:Rule>
</sld:FeatureTypeStyle>
</sld:UserStyle>
</sld:NamedLayer>
</sld:StyledLayerDescriptor>"""
    sldpath = pkg_resources.resource_filename('crdppf','static\public\pdf\sld')
    sldfile = open(pdf_path+'sld_'+ 'siteplan'+'.xml', 'w')
    sldfile.write(sld)
    sldfile.close()
    
    layers = [
        'parcelles',
        'mo22_batiments',
        'mo21_batiments_provisoires',
        'mo23_batiments_projetes',
        'ag1_parcellaire_provisoire',
        'mo9_immeubles',
        'mo5_point_de_detail',
        'mo7_obj_divers_lineaire',
        'mo7_obj_divers_couvert',
        'mo7_obj_divers_piscine',
        'mo7_obj_divers_cordbois',
        'mo4_pfa_1',
        'mo4_pfp_3',
        'mo4_pfp_1_2',  
        'la3_limites_communales',
        'mo22_batiments'
    ]
    
    scale = feature_info['printFormat']['scale']*2
    # SitePlan/Plan de situation/Situationsplan
    map_params = {'width':feature_info['printFormat']['mapWidth'],'height':feature_info['printFormat']['mapHeight']}
    map_params['bboxCenterX'] = (feature_info['BBOX']['maxX']+feature_info['BBOX']['minX'])/2
    map_params['bboxCenterY'] = (feature_info['BBOX']['maxY']+feature_info['BBOX']['minY'])/2
    #to recenter the map on the bbox of the feature, with the right scale and add at least 10% of space we calculate a wmsBBOX
    wmsBBOX = {}
    wmsBBOX['centerY'] =  int(map_params['bboxCenterY'])
    wmsBBOX['centerX'] =  int(map_params['bboxCenterX'])
    wmsBBOX['minX'] = int(wmsBBOX['centerX']-(160*scale/1000/2))
    wmsBBOX['maxX'] = int(wmsBBOX['centerX']+(160*scale/1000/2))
    wmsBBOX['minY'] = int(wmsBBOX['centerY']-(90*scale/1000/2))
    wmsBBOX['maxY'] = int(wmsBBOX['centerY']+(90*scale/1000/2))
    
    #wms = WebMapService('http://sitn.ne.ch/mapproxy/service', version='1.1.1')
    wms = WebMapService(crdppf_wms, version='1.1.1')
    #layers = 'plan_ville_c2c'

    map = wms.getmap(   
        layers=layers,
        sld = sld_url +'/sld_'+ 'siteplan'+'.xml',
        srs='EPSG:21781',
        bbox=(wmsBBOX['minX'],wmsBBOX['minY'],wmsBBOX['maxX'],wmsBBOX['maxY']),
        size=(1600,900),
        format='image/png',
        transparent=False
    )
    
    out = open(pdf_path+'siteplan.png', 'wb')
    out.write(map.read())
    out.close()

    mappath = pdf_path+'siteplan.png'

    map = pdf.image(pdf_path+'siteplan.png',25,90,160,90)

    y=pdf.get_y()
    pdf.rect(25,90,160,90,'')
    pdf.set_y(y+100)
    # First infoline
    pdf.set_font('Helvetica','B',10)
    pdf.cell(45,5,unicode("Immeuble n°", 'utf-8').encode('iso-8859-1'),0,0,'L')
    # ADD immeuble Type !!!!!!!
    pdf.set_font('Helvetica','',10)
    if feature_info['nomcad'] is not None:
        pdf.cell(50,5,feature_info['nummai'].encode('iso-8859-1')+str(' (')+feature_info['nomcad'].encode('iso-8859-1')+str(') '),0,1,'L')
    else : 
        pdf.cell(50,5,feature_info['nummai'].encode('iso-8859-1'),0,1,'L')
    
     # Second infoline : Area and EGRID
    pdf.set_font('Helvetica','B',10)
    pdf.cell(45,5,unicode('Surface de l\'immeuble', 'utf-8').encode('iso-8859-1'),0,0,'L')
    pdf.set_font('Helvetica','',10)
    pdf.cell(50,5,str(feature_info['area'])+str(' m2').encode('iso-8859-1'),0,0,'L')
    pdf.set_font('Helvetica','B',10)
    pdf.cell(35,5,unicode("N° EGRID", 'utf-8').encode('iso-8859-1'),0,0,'L')
    pdf.set_font('Helvetica','',10)
    pdf.cell(50,5,feature_info['no_EGRID'].encode('iso-8859-1'),0,1,'L')      

     # Third infoline : Adresse/localisation
    pdf.set_font('Helvetica','B',10)
    pdf.cell(45,5,unicode('Adresse/Nom local', 'utf-8').encode('iso-8859-1'),0,0,'L')
    pdf.set_font('Helvetica','',10)
    pdf.cell(50,5,str('Placeholder').encode('iso-8859-1'),0,1,'L')   
    
     # Fourth infoline : County and BFS number
    pdf.set_font('Helvetica','B',10)
    pdf.cell(45,5,unicode('Commune', 'utf-8').encode('iso-8859-1')+str(' (')+unicode('N° OFS', 'utf-8').encode('iso-8859-1')+str(')'),0,0,'L')
    pdf.set_font('Helvetica','',10)
    pdf.cell(50,5,feature_info['nomcom'].encode('iso-8859-1')+str(' (')+str(feature_info['nufeco']).encode('iso-8859-1')+str(')'),0,0,'L')
    
    # Creation date and operator
    y= pdf.get_y()
    pdf.set_y(y+10)
    pdf.set_font('Helvetica','B',10)
    pdf.cell(45,5,unicode('Extrait établi le', 'utf-8').encode('iso-8859-1'),0,0,'L')
    pdf.set_font('Helvetica','',10)
    pdf.cell(70,5, today.strftime('%d.%m.%Y - %Hh%M'),0,1,'L')
    pdf.set_font('Helvetica','B',10)
    pdf.cell(45,5,unicode('Editeur de l\'extrait', 'utf-8').encode('iso-8859-1'),0,0,'L')
    pdf.set_font('Helvetica','',10)
    pdf.cell(70,5,feature_info['operator'].encode('iso-8859-1'),0,1,'L')

    y= pdf.get_y()
    pdf.set_y(y+10)
    pdf.set_font('Helvetica','B',10)
    pdf.cell(0,5,unicode('Signature', 'utf-8').encode('iso-8859-1'),0,0,'L')

    pdf.set_y(250)
    pdf.set_font('Helvetica','B',10)
    pdf.cell(0,5,unicode('Indications générales', 'utf-8').encode('iso-8859-1'),0,1,'J')
    pdf.set_font('Helvetica','',10)
    pdf.multi_cell(0,5,unicode('Mise en garde : Le canton de Neuchâtel n\'engage pas sa responsabilité sur l\'exactitude ou la fiabilité des documents législatifs dans leur version électronique. Ces documents ne créent aucun autre droit ou obligation que ceux qui découlent des textes légalement adoptés et publiés, qui font seuls foi.', 'utf-8').encode('iso-8859-1'),0,1,'L')

    # END TITLEPAGE
    
    return pdf
    
@view_config(route_name='create_extract')
def create_extract(request):
    # to get vars defined in the buildout  use : request.registry.settings['key']
    crdppf_wms = request.registry.settings['crdppf_wms']
    sld_url = request.registry.settings['sld_url']

    # other basic parameters
    extract = Objectify()
    pdf_name = 'extract'
    pdf_name='crdppf_'+pdf_name
    pdfpath = pkg_resources.resource_filename('crdppf','static\public\pdf\\')
    extract.today= datetime.now()

    
# *************************
# MAIN PROGRAM PART
#=========================

    # 1) If the ID of the parcel is set get the basic attributs 
    # else get the ID (idemai) of the selected parcel first using X/Y coordinates of the center 
    #----------------------------------------------------------------------------------------------------
    extract.featureInfo = getFeatureInfo(request) # '1_14127' # test parcel or '1_11340'
    featureInfo = extract.featureInfo
    
    # 2) Get the parameters for the paper format and the map based on the feature's geometry
    #---------------------------------------------------------------------------------------------------
    map_params = {'width':featureInfo['printFormat']['mapWidth'],'height':featureInfo['printFormat']['mapHeight']}
    map_params['bboxCenterX'] = (featureInfo['BBOX']['maxX']+featureInfo['BBOX']['minX'])/2
    map_params['bboxCenterY'] = (featureInfo['BBOX']['maxY']+featureInfo['BBOX']['minY'])/2

    pdf_format = extract.featureInfo['printFormat']
    
    # 3) Get the list of all the restrictions
    #-------------------------------------------
    extract.topicList = DBSession.query(Topics).order_by(Topics.topicorder).all()

    # 4) Create the title page for the pdf extract
    #--------------------------------------------------
    pdf = getTitlePage(extract.featureInfo,crdppf_wms,sld_url,pdfpath,featureInfo['nomcom'])

    # 5) Create an empty pdf for the table of content
    #--------------------------------------------------
    #pdf.add_page()
    toc = getTOC()
    
    # 6) Create an empty pdf for the ?annexes?
    #-------------------------------------------------- 
    appendices = getAppendices()
    
    # 7) Create the pages of the extract for each topic in the list
    #---------------------------------------------------
    # Thematic pages
    
    # Loop on each topic
    for crdppfTopic in extract.topicList :
        if crdppfTopic.layers :
            layers = []    
            for layer in crdppfTopic.layers:
                layers.append(layer.layername)          
            if isinstance(layers, list):
                for sublayer in layers:
                    params ={'id':featureInfo['idemai'],'layerList':str(sublayer)}
                    extract.restrictionList = get_features.get_features_function(params)
            else:
                params = {'id':featureInfo['idemai'],'layerList':str(layers)}
                extract.restrictionList = get_features.get_features_function(params)
        else : 
            extract.restrictionList = None
            
        if extract.restrictionList :
            
            neighborhood = 'false'
            
           # PAGE X 
            pdf.add_page()
            pdf.set_margins(25,55,25)
            pdf.set_y(55)
            pdf.set_font('Helvetica','B',16)
            pdf.multi_cell(0,6,str(crdppfTopic.topicname.encode('iso-8859-1')),0,1,'L')
        
            y = pdf.get_y()
            pdf.set_y(y+10)

            for feature in extract.restrictionList:
                if feature['properties'] :

                    # Check if property is affected by the restriction otherwise just mention restrictions in neighborhood
                    if feature['properties']['featureClass'] == 'intersects' or feature['properties']['featureClass'] == 'within' :

                        # Description of the interaction of a restriction with the property
                        #~ if feature['properties']['featureClass']:
                            #~ pdf.set_font('Helvetica','I',10)
                            #~ pdf.cell(100,6,unicode('Type d\'interaction : ','utf-8').encode('iso-8859-1') + feature['properties']['featureClass'].encode('iso-8859-1'),0,1,'L') 

                        # !!! Hardcoding the returned attribute for testing purposes !!! 
                        if feature['properties']['layerName'] == 'at14_zones_communales':
                            pdf.set_font('Helvetica','B',10)
                            pdf.cell(60,5,unicode('Caractéristique:','utf-8').encode('iso-8859-1'),0,0,'L')
                            pdf.set_font('Helvetica','',10)
                            pdf.cell(60,5,feature['properties']['nom_communal'] .encode('iso-8859-1').strip(),0,1,'L')
                            
                        elif feature['properties']['layerName'] == 'en05_degres_sensibilite_bruit':
                            pdf.set_font('Helvetica','B',10)
                            pdf.cell(60,5,unicode('Caractéristique:','utf-8').encode('iso-8859-1'),0,0,'L')
                            pdf.set_font('Helvetica','',10)
                            pdf.cell(60,5,feature['properties']['type_ds'] .encode('iso-8859-1'),0,1,'L')
                       
                        elif feature['properties']['layerName'] == 'en01_zone_sect_protection_eaux':
                            pdf.set_font('Helvetica','B',10)
                            pdf.cell(60,5,unicode('Caractéristique:','utf-8').encode('iso-8859-1'),0,0,'L')
                            pdf.set_font('Helvetica','',10)
                            pdf.cell(60,5,feature['properties']['categorie'] .encode('iso-8859-1'),0,1,'L')
                            
                     
                        elif feature['properties']['layerName'] == 'clo_couloirs':
                            pdf.set_font('Helvetica','B',10)
                            pdf.cell(60,5,unicode('Caractéristique:','utf-8').encode('iso-8859-1'),0,0,'L')
                            pdf.set_font('Helvetica','',10)
                            pdf.cell(60,5,feature['properties']['type'] .encode('iso-8859-1'),0,1,'L')
                            
                        else: 
                            # Attributes of topic layers intersection
                            for key,value in feature['properties'].iteritems():
                                if value is not None :
                                    if key !='layerName' and key != 'featureClass':
                                        pdf.set_font('Helvetica','B',10)
                                        pdf.cell(50,5,unicode('Caractéristique:','utf-8').encode('iso-8859-1'),0,0,'L')
                                        pdf.set_font('Helvetica','',10)
                                        if isinstance(value, float) or isinstance(value, int):
                                            value = str(value)
                                        pdf.cell(60,5,value.encode('iso-8859-1'),0,1,'L')
                    elif feature['properties']['featureClass'] == 'adjacent':
                        neighborhood = 'true'
                
            if neighborhood == 'true':
                #~ pdf.set_font('Helvetica','B',11)
                #~ pdf.cell(100,6,unicode('Nom de la donnée : ','utf-8').encode('iso-8859-1') +feature['properties']['layerName'].encode('iso-8859-1'),0,1,'L') 
                pdf.set_font('Helvetica','I',10)
                pdf.cell(100,6,unicode('Remarque: Il y a des immeubles voisins affectés par cette restriction.','utf-8').encode('iso-8859-1'),0,1,'L') 
            
            y = pdf.get_y()
            pdf.set_y(y+5)
            
            # Legal Provisions/Dispositions légales/Gesetzliche Bestimmungen
            y = pdf.get_y()
            pdf.set_y(y+5)
            pdf.set_font('Helvetica','B',10)
            pdf.cell(55,6,unicode('Dispositions légales', 'utf-8').encode('iso-8859-1'),0,0,'L')
            pdf.set_font('Helvetica','',10)
            if crdppfTopic.legalprovisions:
                for provision in crdppfTopic.legalprovisions:
                    pdf.add_appendix('A',unicode(provision.officialtitle).encode('iso-8859-1'),unicode(provision.legalprovisionurl).encode('iso-8859-1'))
                    pdf.cell(0,5,unicode(provision.officialtitle).encode('iso-8859-1'),0,1,'L')
                    pdf.set_text_color(0,0,255)
                    pdf.set_x(80)
                    pdf.multi_cell(0,6,unicode(provision.legalprovisionurl).encode('iso-8859-1'))
                    pdf.set_text_color(0,0,0)
            else:
                    pdf.multi_cell(0,6,unicode('None').encode('iso-8859-1'))

            # References and complementary information/Renvois et informations supplémentaires/Verweise und Zusatzinformationen
            y = pdf.get_y()
            pdf.set_y(y+5)
            pdf.set_font('Helvetica','B',10)
            pdf.cell(55,6,unicode('Renvois et informations compl.', 'utf-8').encode('iso-8859-1'),0,0,'L')
            pdf.set_font('Helvetica','',10)
            if crdppfTopic.references:
                for reference in crdppfTopic.references:
                    pdf.multi_cell(0,6,unicode(reference.officialtitle).encode('iso-8859-1'))
            else:
                    pdf.multi_cell(0,6,unicode('None','utf-8').encode('iso-8859-1')) 

            # Temporary provisions/Dispositions transitoires et renvois supplémentaires/Übergangsbestimmungen und Zusatzinformationen
            y = pdf.get_y()
            pdf.set_y(y+5)
            pdf.set_font('Helvetica','B',10)
            pdf.cell(55,6,unicode('Dispositions transitoires', 'utf-8').encode('iso-8859-1'),0,0,'L')
            pdf.set_font('Helvetica','',10)
            if crdppfTopic.temporaryprovisions:
                for temp_provision in crdppfTopic.temporaryprovisions:
                    pdf.multi_cell(0,6,unicode(temp_provision.officialtitle).encode('iso-8859-1'),0,1,'L')
                    if temp_provision.temporaryprovisionurl :
                        pdf.set_text_color(0,0,255)
                        pdf.set_x(80)
                        pdf.multi_cell(0,6,unicode(temp_provision.temporaryprovisionurl).encode('iso-8859-1'))
                        pdf.set_text_color(0,0,0)
            else:
                    pdf.multi_cell(0,6,unicode('None','utf-8').encode('iso-8859-1'),0,1,'L')

            # Competent Authority/Service competent/Zuständige Behörde
            y = pdf.get_y()
            pdf.set_y(y+5)
            pdf.set_font('Helvetica','B',10)
            pdf.cell(55,3.9,unicode('Service compétent', 'utf-8').encode('iso-8859-1'),0,0,'L')
            pdf.set_font('Helvetica','',10)
            
            if crdppfTopic.authority.authorityname is not None:
                pdf.cell(120,3.9,crdppfTopic.authority.authorityname.encode('iso-8859-1'),0,1,'L')
            if crdppfTopic.authority.authoritydepartment is not None:
                pdf.cell(55,3.9,str(' '),0,0,'L')
                pdf.cell(120,3.9,crdppfTopic.authority.authoritydepartment.encode('iso-8859-1'),0,1,'L')
            if crdppfTopic.authority.authorityphone1 is not None:
                pdf.cell(55,3.9,str(' '),0,0,'L')
                pdf.cell(120,3.9,unicode('Tél: ','utf-8').encode('iso-8859-1')+crdppfTopic.authority.authorityphone1.encode('iso-8859-1'),0,1,'L')
            if crdppfTopic.authority.authoritywww is not None:
                pdf.cell(55,3.9,str(' '),0,0,'L')
                pdf.cell(120,3.9,str('Web: ').encode('iso-8859-1')+crdppfTopic.authority.authoritywww.encode('iso-8859-1'),0,1,'L')        
            #~ if crdppfTopic.authority.authoritystreet1 is not None:
                #~ pdf.cell(55,3.9,str(' '),0,0,'L')
                #~ pdf.cell(120,3.9,crdppfTopic.authority.authoritystreet1.encode('iso-8859-1'),0,1,'L')
            #~ if crdppfTopic.authority.authoritystreet2 is not None:
                #~ pdf.cell(55,3.9,str(' '),0,0,'L')
                #~ pdf.cell(120,3.9,crdppfTopic.authority.authoritystreet2.encode('iso-8859-1'),0,1,'L')
            #~ if crdppfTopic.authority.authorityzip is not None and crdppfTopic.authority.authoritycity is not None :
                #~ pdf.cell(55,3.9,str(' '),0,0,'L')
                #~ pdf.cell(120,3.9,str(crdppfTopic.authority.authorityzip).encode('iso-8859-1') +str(' ') +crdppfTopic.authority.authoritycity.encode('iso-8859-1'),0,1,'L')
            
            # Legal bases/Bases légales/Gesetzliche Grundlagen
            y = pdf.get_y()
            pdf.set_y(y+5)
            pdf.set_font('Helvetica','B',10)
            pdf.cell(55,6,unicode('Base(s) légale(s)', 'utf-8').encode('iso-8859-1'),0,0,'L')
            pdf.set_font('Helvetica','',10)
            if crdppfTopic.legalbases:
                for legalbase in crdppfTopic.legalbases:
                    pdf.multi_cell(0,6,str(crdppfTopic.legalbases).encode('iso-8859-1'))
            else:
                pdf.multi_cell(0,6,unicode('Legal base(s) placeholder','utf-8').encode('iso-8859-1'))
            
            #~ # TemporaryProvisions/Dispositions transitoires/Übergangsbestimmungen
            #~ y = pdf.get_y()
            #~ pdf.set_y(y+5)
            #~ pdf.set_font('Helvetica','B',10)
            #~ pdf.cell(47,6,unicode('Dispositions transitoires', 'utf-8').encode('iso-8859-1'),0,0,'L')
            #~ pdf.cell(3,6,unicode(': ', 'utf-8').encode('iso-8859-1'),0,0,'L')
            #~ pdf.set_font('Helvetica','',10)
            #~ pdf.multi_cell(0,3.9,unicode('Plan d\'affectation Quartier Nord du 21 décembre 1975\nValable jusqu\'au 31.12.2013','utf-8').encode('iso-8859-1'),0,1,'L')

            # Thematic map/Carte thématique/Thematische Karte
            if crdppfTopic.layers :
                crdppfTopic.mappath,crdppfTopic.legendpath = getMap(crdppfTopic.layers,crdppfTopic.topicid,crdppf_wms,map_params,pdf_format)
                pdf.add_page(str(pdf_format['orientation'] + ','+pdf_format['format']))
                pdf.set_font('Helvetica','B',11)
                pdf.set_xy(10,25)
                pdf.multi_cell(140,5,crdppfTopic.topicname.encode('iso-8859-1')+str(' (plan)'))
                y = pdf.get_y()
                map = pdf.image(crdppfTopic.mappath,10,y+5,pdf_format['width'] ,pdf_format['height'] )
                pdf.set_y(y+5)
                pdf.set_x(10)
                pdf.cell(pdf_format['width'],pdf_format['height'] ,'',1,1,'L')
                y = pdf.get_y()
                pdf.set_xy(15,y+5)
                pdf.cell(50,6,unicode('Légende', 'utf-8').encode('iso-8859-1'),0,1,'L')
                pdf.set_font('Helvetica','',10)
                if crdppfTopic.topicid == '73':
                    for graphic in crdppfTopic.legendpath:
                        legend = pdf.image(crdppfTopic.legendpath,10,y+20,50,50)
                else:
                    pdf.cell(50,6,unicode('Legend placeholder', 'utf-8').encode('iso-8859-1'),0,1,'L')
                
                try: 
                    for graphic in crdppfTopic.legendpath:
                        legend = pdf.image(crdppfTopic.legendpath,10,y+20,50,50)
                except:
                    pass
                pdf.rect(10,y,pdf_format['width'],50,'')
                
            else : 
                y = pdf.get_y()
                pdf.multi_cell(0,6,'Pas de carte.')
                pdf.ln()

                
        # Set the titles
        if crdppfTopic.layers :
            if extract.restrictionList :
                pdf.add_toc_entry(pdf.page_no(),str(crdppfTopic.topicname.encode('iso-8859-1')),255,255,255)
            else : 
                pdf.add_toc_entry('',str(crdppfTopic.topicname.encode('iso-8859-1')),0,250,0)
        else:
            pdf.add_toc_entry('',str(crdppfTopic.topicname.encode('iso-8859-1')),230,0,0)

    # Get the page count of all the chapters
    nb_pages_pdf =  len(pdf.pages)
    nb_pages_toc =  len(toc.pages)
    nb_pages_appendix =  len(appendices.pages)

    nb_pages_total = nb_pages_pdf + nb_pages_toc + nb_pages_appendix
    delta = nb_pages_toc + nb_pages_appendix

    if pdf.toc_entries :
        pdf.add_page()
        pdf.set_margins(25,55,25)
        for entry in pdf.toc_entries :
            toc.set_font('Helvetica','B',11)
            toc.set_fill_color(entry['r'],entry['g'],entry['b'])
            toc.cell(12,6,str(entry['no_page']),'TRB',0,'L')
            toc.cell(118,6,str(entry['title']),1,0,'L',1)
            toc.cell(15,6,str(''),1,0,'L')
            toc.cell(15,6,str(''),'LB',1,'L')
            toc.set_fill_color(255,255,255)
        toc.ln()
        toc.ln()
        toc.set_text_color(0,0,180)
        toc.cell(120,5,unicode('L\'information n\'est pas contraignante.', 'utf-8').encode('iso-8859-1'),0,1,'L')
        toc.set_text_color(0,180,0)
        toc.cell(120,5,unicode('L\'immeuble n\'est pas touché par cette restriction.', 'utf-8').encode('iso-8859-1'),0,1,'L')
        toc.set_text_color(180,0,0)
        toc.cell(120,5,unicode('La restriction n\'est pas disponible.', 'utf-8').encode('iso-8859-1'),0,1,'L')
        toc.set_text_color(0,0,0)
        toc.ln()
        toc.cell(120,5,unicode('1 Les indications font référence à la position des annexes.', 'utf-8').encode('iso-8859-1'),0,1,'L')

    if pdf.appendix_entries :
        pdf.add_page()
        pdf.set_margins(25,55,25)
        for appendix in pdf.appendix_entries:
            appendices.set_font('Helvetica','B',11)
            appendices.cell(15,6,str(appendix['no_page']),0,0,'L')
            appendices.cell(120,6,str(appendix['title']),0,1,'L')
            appendices.set_x(40)
            appendices.set_font('Helvetica','',9)
            appendices.set_text_color(0,0,255)
            appendices.multi_cell(0,6,str(appendix['url']))
            appendices.set_text_color(0,0,0)            
        
    # Make room for the toc anc annexes pushing the content
    for i in range((nb_pages_total+1),(delta),-1):
        pdf.pages[int(i)]=str(pdf.pages[int(i-delta)])

    # Insert the TOC after the title page
    pdf.pages[int(2)]=str(toc.pages[int(1)])
    
    # Insert the annexes after the toc
    for k in range(1,nb_pages_appendix+1):
        pdf.pages[int(nb_pages_toc+1+k)]=str(appendices.pages[int(k)])

    for p in range(1,len(pdf.pages)+1):
        pdf.pages[int(p)] = str(pdf.pages[int(p)]).replace('{no_pg}',str(int(p)))
    
    for l in range(1,len(pdf.pages)):
         pdf.pages[int(l)] = str(pdf.pages[int(l)].replace('{nomcom}',featureInfo['nomcom'].encode('iso-8859-1')))

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
    