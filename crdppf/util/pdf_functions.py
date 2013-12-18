# -*- coding: UTF-8 -*-

from owslib.wms import WebMapService
import pkg_resources
from datetime import datetime
import urllib
from PIL import Image
# geometry related librabries
from shapely.geometry import Point as splPoint, Polygon as splPolygon, MultiPolygon as splMultiPolygon, LinearRing as splLinearRing
from shapely.wkb import loads as loads_wkb
from shapely.wkt import loads as loads_wkt

from xml.dom.minidom import parseString

from crdppf.models import *

from geoalchemy import WKBSpatialElement

def get_translations(lang):
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

def validate_XML(xmlparser, xmlfilename):
    try:
        with open(xmlfilename, 'r') as f:
            etree.fromstring(f.read(), xmlparser) 
        return True
    except:
        return False

    #~ with open(schema_file, 'r') as f:
        #~ schema_root = etree.XML(f.read())

    #~ schema = etree.XMLSchema(schema_root)
    #~ xmlparser = etree.XMLParser(schema=schema)

    #~ filenames = ['input1.xml', 'input2.xml', 'input3.xml']
    #~ for filename in filenames:
        #~ if validate(xmlparser, filename):
            #~ xmlvalid = True
        #~ else:
            #~ xmlvalid = False

    return xmlvalid
def get_XML(geometry):
    """Gets the XML extract of the federal data feature service for a given topic
        and validates it against the schema.
    """
    # baseurl of the server of the swiss confederation
    server = 'https://api3.geo.admin.ch'
    # rest service call
    url = '/rest/services/api/MapServer/identify?'
    # geometry of the feature to call the feature server for
    feature = geometry
    geomtype = 'geometryType=esriGeometryEnvelope'
    layers = 'all:ch.bazl.sicherheitszonenplan.oereb'
    bbox = 'mapExtent=671164.31244,253770,690364.31244,259530'
    mapparams = 'imageDisplay=1920,576,96'
    tolerance=5
    format='interlis'

    sampleurl = 'https://api3.geo.admin.ch/rest/services/api/MapServer/identify?geometry=515000,180000,580000,230000&geometryType=esriGeometryEnvelope&layers=all:ch.bazl.sicherheitszonenplan.oereb&mapExtent=515000,180000,580000,230000&imageDisplay=1920,576,96&tolerance=5&geometryFormat=interlis'

    #xmlurl = server+url+'geometry='+feature+geomtype+'layers='layers+
    # Call the feature service URL wich sends back an XML Interlis 2.3 file in the OEREB Transfer structure
    response = urllib.urlopen(sampleurl)
    content = response.read()
    xmldoc = parseString(content).firstChild
    # extract the datasection from the response
    datasection = xmldoc.getElementsByTagName("DATASECTION")[0]
    # extract the complete tranfert structure
    transferstructure = xmldoc.getElementsByTagName("OeREBKRM09trsfr.Transferstruktur")
    # Get the competent authority for the legal provisions
    vsauthority = {'shortname':xmldoc.getElementsByTagName("OeREBKRM09vs.Vorschriften.Amt")[0].getAttributeNode("TID").value, 
        'namede':xmldoc.getElementsByTagName("OeREBKRM09vs.Vorschriften.Amt")[0].getElementsByTagName("Text")[0].firstChild.data,
        'namefr':xmldoc.getElementsByTagName("OeREBKRM09vs.Vorschriften.Amt")[0].getElementsByTagName("Text")[1].firstChild.data,
        'namefr':xmldoc.getElementsByTagName("OeREBKRM09vs.Vorschriften.Amt")[0].getElementsByTagName("Text")[2].firstChild.data,
        'url':xmldoc.getElementsByTagName("OeREBKRM09vs.Vorschriften.Amt")[0].getElementsByTagName("AmtImWeb")[0].firstChild.data}
    vslegalprovisions = xmldoc.getElementsByTagName("OeREBKRM09vs.Vorschriften.Dokument")
    # Get the WMS and it's legend
    xtfwms = {'wmsurl':xmldoc.getElementsByTagName("OeREBKRM09trsfr.Transferstruktur.DarstellungsDienst")[0].getElementsByTagName("VerweisWMS")[0].firstChild.data,
        'wmslegend':xmldoc.getElementsByTagName("OeREBKRM09trsfr.Transferstruktur.DarstellungsDienst")[0].getElementsByTagName("LegendeImWeb")[0].firstChild.data
        }
    # GET restrictions
    xtfrestrictions = xmldoc.getElementsByTagName("OeREBKRM09trsfr.Transferstruktur.Eigentumsbeschraenkung")
    if xtfrestrictions:
        restrictions = []
        restriction = {}
        for xtfrestriction in xtfrestrictions:
            restriction = {'restrictionid':xtfrestriction.getAttributeNode("TID").value,
                'teneurde':xtfrestriction.getElementsByTagName("Aussage")[0].getElementsByTagName("Text")[0].firstChild.data,
                'teneurfr':xtfrestriction.getElementsByTagName("Aussage")[0].getElementsByTagName("Text")[1].firstChild.data,
                'teneurit':xtfrestriction.getElementsByTagName("Aussage")[0].getElementsByTagName("Text")[2].firstChild.data,
                'topic':xtfrestriction.getElementsByTagName("Thema")[0].firstChild.data,
                'legalstate':xtfrestriction.getElementsByTagName("Rechtsstatus")[0].firstChild.data,
                'publishedsince':xtfrestriction.getElementsByTagName("publiziertAb")[0].firstChild.data,
                'url':xtfrestriction.getElementsByTagName("DarstellungsDienst")[0].getAttributeNode("REF").value,
                'authority':xtfrestriction.getElementsByTagName("ZustaendigeStelle")[0].getAttributeNode("REF").value}
            restrictions.append(restriction)

    xtfvslinkprovisions = xmldoc.getElementsByTagName("OeREBKRM09trsfr.Transferstruktur.HinweisVorschrift")
    vslinkprovisions = []
    for vslinkprovision in xtfvslinkprovisions:
        vslinkprovisions.append({'origin':vslinkprovision.getElementsByTagName("Eigentumsbeschraenkung")[0].getAttributeNode("REF").value,
            'link':vslinkprovision.getElementsByTagName("Vorschrift")[0].getAttributeNode("REF").value})

    xtfvslinkreferences = xmldoc.getElementsByTagName("OeREBKRM09vs.Vorschriften.HinweisWeitereDokumente")
    vslinkreferences = []
    for vslinkreference in xtfvslinkreferences:
        vslinkreferences.append({'origin':vslinkreference.getElementsByTagName("Ursprung")[0].getAttributeNode("REF").value,
            'link':vslinkreference.getElementsByTagName("Hinweis")[0].getAttributeNode("REF").value})

    xtfvslegalprovisions = xmldoc.getElementsByTagName("OeREBKRM09vs.Vorschriften.Rechtsvorschrift")
    vslegalprovisions = []
    for vslegalprovision in xtfvslegalprovisions:
        vslegalprovisions.append({'provisionid':vslegalprovision.getAttributeNode("TID").value,
            'titel':vslegalprovision.getElementsByTagName("Text")[0].firstChild.data,
            'legalstate':vslegalprovision.getElementsByTagName("Rechtsstatus")[0].firstChild.data,
            'publishedsince':vslegalprovision.getElementsByTagName("publiziertAb")[0].firstChild.data,
            'authority':vslegalprovision.getElementsByTagName("ZustaendigeStelle")[0].getAttributeNode("REF").value,
            'url':vslegalprovision.getElementsByTagName("TextImWeb")[0].firstChild.data})

    xtfvsdocuments = xmldoc.getElementsByTagName("OeREBKRM09vs.Vorschriften.Dokument")
    vsdocuments = []
    for vsdocument in xtfvsdocuments:
        vsdocuments.append({'provisionid':vsdocument.getAttributeNode("TID").value,
            'titel':vsdocument.getElementsByTagName("Text")[0].firstChild.data,
            'legalstate':vsdocument.getElementsByTagName("Rechtsstatus")[0].firstChild.data,
            'publishedsince':vsdocument.getElementsByTagName("publiziertAb")[0].firstChild.data,
            'authority':vsdocument.getElementsByTagName("ZustaendigeStelle")[0].getAttributeNode("REF").value,
            'url':vsdocument.getElementsByTagName("TextImWeb")[0].firstChild.data})
            
    #swet
    xtflegalprovisions = xmldoc.getElementsByTagName("OeREBKRM09trsfr.Transferstruktur.HinweisVorschrift")
    feature = []
    for xtflegalprovision in xtflegalprovisions:
        feature.append({'restrictionid':xtflegalprovision.getElementsByTagName("Eigentumsbeschraenkung")[0].getAttributeNode("REF").value,'provision':xtflegalprovision.getElementsByTagName("Vorschrift")[0].getAttributeNode("REF").value})

    xtfreferences = xmldoc.getElementsByTagName("OeREBKRM09vs.Vorschriften.HinweisWeitereDokumente")

    xtfgeoms = xmldoc.getElementsByTagName("OeREBKRM09trsfr.Transferstruktur.Geometrie")
    geometries = []
    for xtfgeom in xtfgeoms:
        if xtfgeom.getElementsByTagName("Flaeche"):
            if xtfgeom.getElementsByTagName("SURFACE"):
                surfaces = xtfgeom.getElementsByTagName("SURFACE")
                if xtfgeom.getElementsByTagName("BOUNDARY"):
                    boundaries = xtfgeom.getElementsByTagName("BOUNDARY")
                    if xtfgeom.getElementsByTagName("POLYLINE"):
                        polylines = xtfgeom.getElementsByTagName("POLYLINE")
                        if len(polylines) > 1:
                            multipolygon = []
                        for polyline in polylines:
                            coordlist = []
                            for coords in polyline.childNodes:
                                coordlist.append((float(coords.getElementsByTagName("C1")[0].firstChild.data), float(coords.getElementsByTagName("C2")[0].firstChild.data)))
                            #del coordlist[-1]
                            polygon = splPolygon(coordlist)
                            if len(polylines) > 1:
                                multipolygon.append(polygon)
                                geom = splMultiPolygon(multipolygon)
                            else:
                                geom = polygon

        geometries.append({'tid':xtfgeom.getAttributeNode("TID").value,
            'restrictionid':xtfgeom.getElementsByTagName("Eigentumsbeschraenkung")[0].getAttributeNode("REF").value,
            'competentAuthority':xtfgeom.getElementsByTagName("ZustaendigeStelle")[0].getAttributeNode("REF").value,
            'legalstate':xtfgeom.getElementsByTagName("Rechtsstatus")[0].firstChild.data,
            'publishedsince':xtfgeom.getElementsByTagName("publiziertAb")[0].firstChild.data,
            'metadata':xtfgeom.getElementsByTagName("MetadatenGeobasisdaten")[0].firstChild.data,
            'geom':geom.wkt})

    for geometry in geometries:
        securityzone = CHAirportSecurityZones()
        #securityzone.idobj = geometry['restrictionid']
        securityzone.theme = u'Plan de la zone de sécurité des aéroports'
        securityzone.codegenre = None
        securityzone.teneur = u'Limitation de la hauteur des bâtiments et autres obstacles'
        if geometry['legalstate'] ==  u'inKraft':
            securityzone.statutjuridique = u'En vigueur'
        else:
            securityzone.statutjuridique = u'En cours d\'approbation'
        if geometry['publishedsince']:
            securityzone.datepublication = geometry['publishedsince']
        else:
            securityzone.datepublication = None
        # It is very important to set the SRID if it's not the default EPSG:4326 !!
        securityzone.geom = WKTSpatialElement(geometry['geom'], 21781)
        DBSession.add(securityzone)

    DBSession.flush()
    
    return

def get_feature_info(request, translations):
    """The function gets the geometry of a parcel by it's ID and does an overlay 
    with other administrative layers to get the basic parcelInfo and attribute 
    information of the parcel : municipality, local names, and so on
    
    hint:
    for debbuging the query use str(query) in the console/browser window
    to visualize geom.wkt use session.scalar(geom.wkt)
    """

    SRS = 21781

    parcelInfo = {}
    parcelInfo['featureid'] = None
    Y = None
    X = None

    if request.params.get('id') :
        parcelInfo['featureid'] = request.params.get('id')
    elif request.params.get('X') and request.params.get('Y') :
        X = int(request.params.get('X'))
        Y = int(request.params.get('Y'))
    else :
        raise Exception(translations[''])

    if parcelInfo['featureid'] is not None:
        queryresult = DBSession.query(ImmeublesCanton).filter_by(idemai=parcelInfo['featureid']).first()
        # We should check unicity of the property id and raise an exception if there are multiple results 
    elif (X > 0 and Y > 0):
        if  Y > X :
            pointYX = WKTSpatialElement('POINT('+str(Y)+' '+str(X)+')',SRS)
        else:
            pointYX = WKTSpatialElement('POINT('+str(X)+' '+str(Y)+')',SRS)
        queryresult = DBSession.query(ImmeublesCanton).filter(ImmeublesCanton.geom.gcontains(pointYX)).first()
        parcelInfo['featureid'] = queryresult.idemai
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
    parcelInfo['BBOX'] = get_bbox(DBSession.scalar(queryresult.geom.envelope.wkt))

    # the get_print_format function is not needed any longer as the paper size has been fixed to A4 by the cantons
    # parcelInfo['printFormat'] = get_print_format(parcelInfo['BBOX'])

    return parcelInfo

def get_bbox(geometry):
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

def get_print_format(bbox, fitRatio):
    """Detects the best paper format and scale in function of the general form and size of the parcel
    This function determines the optimum scale and paper format (if different paper 
    formats are available) for the pdf print in dependency of the general form of 
    the selected parcel.
    """

    printFormat = {}

    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # Enhancement : take care of a preselected paper format by the user
    # ===================
    formatChoice = 'A4'
    # if fixedpaperformat == True:
    #     paperFormats = {predefinedPaperFormat}
    # else:
    # Gets the list of all available formats and their parameters : name, orientation, height, width
    paperFormats = DBSession.query(PaperFormats).order_by(PaperFormats.scale.asc()).order_by(PaperFormats.orientation.desc()).all()

    fit = 'false'
    # fitRation defines the minimum spare space between the property limits and the map border. Here 10%
    # fitRatio = 0.9
    ratioW = 0
    ratioH = 0
    # Attention X and Y are standard carthesian and inverted in comparison to the Swiss Coordinate System 
    deltaX = bbox['maxX'] - bbox['minX']
    deltaY = bbox['maxY'] - bbox['minY']
    resolution = 150 # 150dpi print resolution
    ratioInchMM = 25.4 # conversion inch to mm

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
