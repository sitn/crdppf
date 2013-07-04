# -*- coding: UTF-8 -*-

from owslib.wms import WebMapService
import pkg_resources
from datetime import datetime
import urllib

from crdppf.util.pdf_classes import Objectify, ExtractPDF

from crdppf.models import *

def getBBOX(geometry):
    """Returns the BBOX coordinates of an rectangle. Input : rectangle; output : bbox
       coordListStr : String with the list of the X,Y coordinates of the bounding box
       X,Y : coordinates in Swiss national projection
       bbox : Resulting dictionary with lower left (minX,minY) and upper right corner (maxX,maxY)
    """

    coordListStr = geometry.split("(")[2].split(")")[0].split(',')
    X = []
    Y = []
    for coordStr in coordListStr:
        X.append(float(coordStr.split(" ")[0]))
        Y.append(float(coordStr.split(" ")[1]))

    bbox = {'minX': min(X), 'minY': min(Y), 'maxX': max(X), 'maxY': max(Y)}

    return bbox

def getTranslations(lang):
    """Loads the translations for all the multilingual labels
    """
    locals = {}
    lang_dict = {
        'fr': Translations.fr,
        'de': Translations.de,
        'it': Translations.it,
        'en': Translations.en
    }
    translations = DBSession.query(Translations.varstr, lang_dict[lang]).all()
    for key, value in translations :
        locals[str(key)] = value

    return locals

def getPrintFormat(bbox):
    """Detects the best paper format and scale in function of the general form and size of the parcel
    This function determines the optimum scale and paper format (if different paper 
    formats are available) for the pdf print in dependency of the general form of 
    the selected parcel.
    """

    printFormat = {}

    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # TO DO : take care of a preselected paper format by the user
    # ===================
    formatChoice = 'A4'

    # Gets the list of all available formats and their parameters : name, orientation, height, width
    paperFormats = DBSession.query(PaperFormats).order_by(PaperFormats.scale.asc()).order_by(PaperFormats.orientation.desc()).all()

    fit = 'false'
    fitRatio = 0.9
    ratioW = 0
    ratioH = 0
    # Attention X and Y are standard carthesian and inverted in comparison to the Swiss Coordinate System 
    deltaX = bbox['maxX'] - bbox['minX']
    deltaY = bbox['maxY'] - bbox['minY']
    resolution = 150
    ratioInchMM = 25.4

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


def getFeatureInfo(request, translations):
    """The function gets the geometry of a parcel by it's ID and does an overlay 
    with other administrative layers to get the basic parcelInfo and attribute 
    information of the parcel : municipality, local names, and so on
    
    hint:
    for debbuging the query use str(query) in the console/browser window
    to visualize geom.wkt use session.scalar(geom.wkt)
    """

    SRS = 21781

    parcelInfo = {}
    parcelInfo['idemai'] = None
    Y = None
    X = None

    if request.params.get('id') :
        parcelInfo['idemai'] = request.params.get('id')
    elif request.params.get('X') and request.params.get('Y') :
        X = int(request.params.get('X'))
        Y = int(request.params.get('Y'))
    else :
        raise Exception(translations[''])

    if parcelInfo['idemai'] is not None:
        queryresult = DBSession.query(ImmeublesCanton).filter_by(idemai=parcelInfo['idemai']).first()
        # We should check unicity of the property id and raise an exception if there are multiple results 
    elif (X > 0 and Y > 0):
        if  Y > X :
            pointYX = WKTSpatialElement('POINT('+str(Y)+' '+str(X)+')',SRS)
        else:
            pointYX = WKTSpatialElement('POINT('+str(X)+' '+str(Y)+')',SRS)
        queryresult = DBSession.query(ImmeublesCanton).filter(ImmeublesCanton.geom.gcontains(pointYX)).first()
        parcelInfo['idemai'] = queryresult.idemai
    else : 
        # to define
        return HTTPBadRequest(translations['HTTPBadRequestMsg'])

    parcelInfo['geom'] = queryresult.geom
    parcelInfo['area'] = int(DBSession.scalar(queryresult.geom.area))

    queryresult1 = DBSession.query(NomLocalLieuDit).filter(NomLocalLieuDit.geom.intersects(parcelInfo['geom'])).first()
    queryresult2 = DBSession.query(Cadastre).filter(Cadastre.geom.buffer(1).gcontains(parcelInfo['geom'])).first()

    parcelInfo['nummai'] = queryresult.nummai # Parcel number
    parcelInfo['type'] = queryresult.typimm # Parcel type
    parcelInfo['lieu_dit'] = queryresult1.nomloc # Flurname
    parcelInfo['nomcad'] = queryresult2.cadnom
    parcelInfo['numcom'] = queryresult.numcom
    parcelInfo['nomcom'] = queryresult2.comnom
    parcelInfo['nufeco'] = queryresult2.nufeco
    parcelInfo['centerX'], parcelInfo['centerY'] = DBSession.scalar(queryresult.geom.centroid.x),DBSession.scalar(queryresult.geom.centroid.y)
    parcelInfo['BBOX'] = getBBOX(DBSession.scalar(queryresult.geom.envelope.wkt))

    # the getPrintFormat function is not needed any longer as the paper size has been fixed to A4 by the cantons
    parcelInfo['printFormat'] = getPrintFormat(parcelInfo['BBOX'])

    return parcelInfo


def getRestrictions(parcelInfo) :
    """ Geographic overlay to get all the restrictions within or adjacent to 
    the parcel
    """

    geom = parcelInfo['geom']
    restrictions = DBSession.query().all()

    return restrictionInfo


def getMap(restriction_layers,topicid,crdppf_wms,map_params,pdf_format):
    """Produces the map and the legend for each layer of an restriction theme
    """

    # Name of the pdf file - should be individualized with a timestamp or ref number
    pdf_name = 'extract'
    # Path to the output folder of the pdf
    temp_path = pkg_resources.resource_filename('crdppf', 'static/public/temp_files/')

    #pdf_path = pkg_resources.resource_filename('crdppf','static\public\pdf\\')

    # Map scale
    scale = pdf_format['scale']

    # List with the base layers of the map - the restriction layers get added to the list
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

    # temp var to hold the parameters of the legend
    legend_layers = []
    # temp var for the path to the created legend
    legend_path = []

    # Adding each layer of the restriction to the WMS
    for layer in restriction_layers:
        # Compile the layer list for the wms
        layers.append(layer.layername)

        # in the same time create the legend graphic for each layer and write it to disk
        legend = open(temp_path+str('legend_')+str(layer.layername)+'.png', 'wb')
        img = urllib.urlopen(crdppf_wms+ \
            str('?TRANSPARENT=TRUE&SERVICE=WMS&VERSION=1.1.1&REQUEST=GetLegendGraphic&FORMAT=image%2Fpng&LAYER=' \
            +str(layer.layername)))

        legend.write(img.read())
        legend.close()
        legend_path.append(temp_path+str('legend_')+str(layer.layername))

    # to recenter the map on the bbox of the feature, compute the best scale and add at least 10% of space we calculate a wmsBBOX
    wmsBBOX = {}
    wmsBBOX['centerY'] = int(map_params['bboxCenterY'])
    wmsBBOX['centerX'] = int(map_params['bboxCenterX'])
    # From the center point add and substract half the map distance in X and Y direction to get BBOX min/max coords
    wmsBBOX['minX'] = int(wmsBBOX['centerX']-(pdf_format['width']*scale/1000/2))
    wmsBBOX['maxX'] = int(wmsBBOX['centerX']+(pdf_format['width']*scale/1000/2))
    wmsBBOX['minY'] = int(wmsBBOX['centerY']-(pdf_format['height']*scale/1000/2))
    wmsBBOX['maxY'] = int(wmsBBOX['centerY']+(pdf_format['height']*scale/1000/2))

    # call the WMS and write the map to file
    wms = WebMapService(crdppf_wms, version='1.1.1')

    map = wms.getmap(
        layers=layers,
        srs='EPSG:21781',
        bbox=(wmsBBOX['minX'],wmsBBOX['minY'],wmsBBOX['maxX'],wmsBBOX['maxY']),
        size=(map_params['width'], map_params['height']),
        format='image/png',
        transparent=False
    )

    out = open(temp_path+pdf_name+str(topicid)+'.png', 'wb')
    out.write(map.read())
    out.close()
    mappath = temp_path + pdf_name + str(topicid) + '.png'
        
    return mappath, legend_path

def getAppendices(commune, pdfconfig, translations):

    appendix_pages = ExtractPDF(commune, pdfconfig, translations)

    # START APPENDIX
    appendix_pages.add_page()
    appendix_pages.set_margins(*pdfconfig.pdfmargins)
    appendix_pages.set_y(40)
    appendix_pages.set_font(*pdfconfig.textstyles['title3'])
    appendix_pages.multi_cell(0, 12, translations['appendiceslistlabel'])

    appendix_pages.set_y(60)
    appendix_pages.set_font(*pdfconfig.textstyles['bold'])
    appendix_pages.cell(15, 6, translations['pagelabel'], 0, 0, 'L')
    appendix_pages.cell(135, 6, translations['appendicestitlelabel'], 0, 1, 'L')

    return appendix_pages

def getTOC(commune, pdfconfig, translations):

    toc_pages = ExtractPDF(commune, pdfconfig, translations)

    # START TOC
    toc_pages.add_page()
    toc_pages.set_margins(*pdfconfig.pdfmargins)
    toc_pages.set_y(40)
    toc_pages.set_font(*pdfconfig.textstyles['title3'])
    toc_pages.multi_cell(0, 12, translations['toclabel'])

    toc_pages.set_y(60)
    toc_pages.set_font(*pdfconfig.textstyles['bold'])
    toc_pages.cell(12, 15, '', '', 0, 'L')
    toc_pages.cell(118, 15, '', 'L', 0, 'L')
    toc_pages.cell(15, 15, '', 'L', 0, 'C')
    toc_pages.cell(15, 15, '', 'L', 1, 'C')

    toc_pages.cell(12, 5, translations['pagelabel'], 'B', 0, 'L')
    toc_pages.cell(118 ,5, translations['toclabel'], 'LB', 0, 'L')
    y = toc_pages.get_y()
    x = toc_pages.get_x()
    toc_pages.rotate(90)
    toc_pages.text(x-4, y+8, translations['legalprovisionslabel'].replace(' ', '\n'))
    toc_pages.text(x-4, y+23, translations['referenceslabel'])
    toc_pages.rotate(0)
    toc_pages.cell(15, 5, '', 'LB', 0, 'L')
    toc_pages.cell(15, 5, '', 'LB', 1, 'L')

    return toc_pages

def getTitlePage(feature_info, crdppf_wms, nomcom, commune, pdfconfig, translations):

    temp_path = pkg_resources.resource_filename('crdppf', 'static/public/temp_files/')

    # the dictionnary for the document
    reportInfo = {}
    reportInfo['type'] = '[officiel]'

    # the dictionnary for the parcel
    feature_info['no_EGRID'] = 'to be defined'
    #feature_info['lastUpdate'] = datetime.now()
    feature_info['operator'] = 'F.Voisard - SITN'
    today= datetime.now()

    # Create property highlight sld
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
<sld:CssParameter name="stroke-width">5</sld:CssParameter>
</sld:Stroke>
</sld:PolygonSymbolizer>
<sld:TextSymbolizer>
<sld:Label>
<ogc:PropertyName>nummai</ogc:PropertyName>
</sld:Label> 
<sld:Font>
<sld:CssParameter name="font-family">pdfconfig.fontfamily</sld:CssParameter> 
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


    sldfile = open(temp_path+'sld_'+'siteplan'+'.xml', 'w')
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
        sld = pdfconfig.sld_url +'/sld_'+ 'siteplan'+'.xml',
        srs='EPSG:21781',
        bbox=(wmsBBOX['minX'],wmsBBOX['minY'],wmsBBOX['maxX'],wmsBBOX['maxY']),
        size=(1600,900),
        format='image/png',
        transparent=False
    )

    out = open(temp_path+'siteplan.png', 'wb')
    out.write(map.read())
    out.close()

    mappath = temp_path + 'siteplan.png'

    # Create PDF extract
    pdf = ExtractPDF(commune, pdfconfig, translations) 

    # START TITLEPAGE
    pdf.add_page()
    pdf.set_margins(*pdfconfig.pdfmargins)
    path = pkg_resources.resource_filename('crdppf', 'utils\\')

    # PageTitle
    pdf.set_y(45)
    pdf.set_font(*pdfconfig.textstyles['title1'])
    if reportInfo['type'] =='certified':
        pdf.multi_cell(0, 9, translations["certifiedextracttitlelabel"])
    elif reportInfo['type'] =='reduced':
        pdf.multi_cell(0, 9, translations['reducedextracttitlelabel'])
    elif reportInfo['type'] =='reducedcertified':
        pdf.multi_cell(0, 9, translations['reducedcertifiedextracttitlelabel'])
    else:
        pdf.multi_cell(0, 9, translations['normalextracttitlelabel'])
    pdf.set_font(*pdfconfig.textstyles['title2'])
    #pdf.multi_cell(0, 7, translations['extractsubtitlelabel'])
    pdf.multi_cell(0, 7, translations['extractsubtitlelabel'])
    pdf.ln()
    
    map = pdf.image(temp_path+'siteplan.png', 25, 80, 160, 90)

    y=pdf.get_y()
    pdf.rect(25, 80, 160, 90, '')
    pdf.set_y(y+105)
    # First infoline
    pdf.set_font(*pdfconfig.textstyles['bold'])
    pdf.cell(45, 5, translations['propertylabel'], 0, 0, 'L')

    pdf.set_font(*pdfconfig.textstyles['normal'])
    if feature_info['nomcad'] is not None:
        pdf.cell(50, 5, feature_info['nummai'].encode('iso-8859-1')+str(' (')+feature_info['nomcad'].encode('iso-8859-1')+str(') ')+str(' - ')+feature_info['type'].encode('iso-8859-1'), 0, 1, 'L')
    else : 
        pdf.cell(50, 5, feature_info['nummai'].encode('iso-8859-1'), 0, 1, 'L')
    
     # Second infoline : Area and EGRID
    pdf.set_font(*pdfconfig.textstyles['bold'])
    pdf.cell(45, 5, translations['propertyarealabel'], 0, 0, 'L')
    pdf.set_font(*pdfconfig.textstyles['normal'])
    pdf.cell(50, 5, str(feature_info['area'])+str(' m2').encode('iso-8859-1'), 0, 0, 'L')
    pdf.set_font(*pdfconfig.textstyles['bold'])
    pdf.cell(35, 5, translations['EGRIDlabel'], 0, 0, 'L')
    pdf.set_font(*pdfconfig.textstyles['normal'])
    pdf.cell(50, 5, feature_info['no_EGRID'].encode('iso-8859-1'), 0, 1, 'L')

    # Third infoline : Adresse/localisation
    pdf.set_font(*pdfconfig.textstyles['bold'])
    pdf.cell(45, 5, translations['addresslabel'], 0, 0, 'L')
    pdf.set_font(*pdfconfig.textstyles['normal'])
    pdf.cell(50, 5, str('Placeholder').encode('iso-8859-1'), 0, 1, 'L')

     # Fourth infoline : municipality and BFS number
    pdf.set_font(*pdfconfig.textstyles['bold'])
    pdf.cell(45, 5,  translations['municipalitylabel']+str(' (')+translations['federalmunicipalitynumberlabel']+str(')'), 0, 0, 'L')
    pdf.set_font(*pdfconfig.textstyles['normal'])
    pdf.cell(50, 5, feature_info['nomcom'].encode('iso-8859-1')+str(' (')+str(feature_info['nufeco']).encode('iso-8859-1')+str(')'), 0, 0, 'L')

    # Creation date and operator
    y= pdf.get_y()
    pdf.set_y(y+10)
    pdf.set_font(*pdfconfig.textstyles['bold'])
    pdf.cell(45, 5, translations['extractoperatorlabel'], 0, 0, 'L')
    pdf.set_font(*pdfconfig.textstyles['normal'])
    pdf.cell(70, 5, feature_info['operator'].encode('iso-8859-1'), 0, 1, 'L')

    y= pdf.get_y()
    pdf.set_y(y+5)
    pdf.set_font(*pdfconfig.textstyles['bold'])
    pdf.cell(0, 5, translations['signaturelabel'], 0, 0, 'L')

    pdf.set_y(250)
    pdf.set_font(*pdfconfig.textstyles['bold'])
    pdf.cell(0, 5, translations['disclaimerlabel'], 0, 1, 'L')
    pdf.set_font(*pdfconfig.textstyles['normal'])
    pdf.multi_cell(0, 5, translations['disclaimer'], 0, 1, 'L')

    # END TITLEPAGE

    return pdf
