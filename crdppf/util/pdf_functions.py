# -*- coding: UTF-8 -*-

import urllib
import types

# geometry related librabries
from shapely.geometry import Point as splPoint, Polygon as splPolygon
from shapely.geometry import MultiPolygon as splMultiPolygon, LinearRing as splLinearRing
from geoalchemy import WKTSpatialElement

from xml.dom.minidom import parseString

from crdppf.models import DBSession
from crdppf.models import Translations, PaperFormats
from crdppf.models import Town, Property, LocalName
from crdppf.models import CHAirportSecurityZonesPDF, CHAirportProjectZonesPDF, CHPollutedSitesPublicTransportsPDF

def geom_from_coordinates(coords):
    """ Function to convert a list of coordinates in a geometry
    """
    if (len(coords) > 1 and len(coords) % 2 == 0):
        geom = splPolygon(coords)
    elif (len(coords) > 0 and len(coords) % 2 == 0):
        geom = splPoint(coords)
    else:
        geom = None

    return geom

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

# STILL to implement if valdiation is not done automatically by minidom
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

def get_XML(geometry, topicid, extracttime, lang, translations):
    """Gets the XML extract of the federal data feature service for a given topic
        and validates it against the schema.
    """
    # baseurl of the server of the swiss confederation
    server = 'https://api3.geo.admin.ch'
    # rest service call
    url = '/rest/services/api/MapServer/identify'
    #layers = 'all:ch.bazl.sicherheitszonenplan.oereb'
    #bbox = 'mapExtent=671164.31244,253770,690364.31244,259530'
    # geometry of the feature to call the feature server for
    feature = geometry
    #geomtype = 'geometryType=esriGeometryEnvelope'
    wktfeature = DBSession.scalar(geometry.wkt)
    bbox = get_bbox_from_geometry(wktfeature)
    # geometrytype used for feature service call
    geomtype = 'esriGeometryPolygon'
    # geomtype = 'esriGeometryEnvelope' - BBOX
    # geomtype = 'esriGeometryPoint' - Point
    # Size and resolution of the returned image
    mapparams = '1920,576,96'
    # geometry tolerance for intersection
    tolerance=5
    # data format
    format='interlis'
    xml_layers = {
        '103':'ch.bazl.projektierungszonen-flughafenanlagen.oereb',
        '108':'ch.bazl.sicherheitszonenplan.oereb',
        '119':'ch.bav.kataster-belasteter-standorte-oev.oereb'
        }
    
    coords = geometry.coords(DBSession)
    # Stupid ESRI stuff: double quotes are needed to call the feature service, thus we have to hardcode "rings"
    esrifeature = '{"rings":'+ str(coords)+'}'

    # Composing the feature service request
    fsurl = server+url
    
    params = {
        'geometry': esrifeature,
        'geometryType': geomtype,
        'layers': 'all:'+xml_layers[topicid],
        'mapExtent': str(bbox.values()).strip('[]'),
        'imageDisplay': mapparams,
        'tolerance': str(tolerance),
        'geometryFormat': format,
        'lang': lang
    }
    params = urllib.urlencode(params)
        
    # Call the feature service URL wich sends back an XML Interlis 2.3 file in the OEREB Transfer structure
    response = urllib.urlopen(fsurl, params)
    content = response.read()

    # trim all whitespace and newlines
    content_lines = content.splitlines()
    count = 0
    for line in content_lines:
        content_lines[count] = line.strip()
        count += 1
    content = ''.join(content_lines)

    # validate XML
    #xmldoc = parseString(content).firstChild
    xmldoc = parseString(content).getElementsByTagName("TRANSFER")[0]
    # extract the datasection from the response
    datasection = xmldoc.getElementsByTagName("DATASECTION")[0]
    # extract the complete tranfert structure
    transferstructure = xmldoc.getElementsByTagName("OeREBKRM09trsfr.Transferstruktur")
    
    if len(transferstructure[0].childNodes) > 0:
        
        # Get the competent authority for the legal provisions
        vsauthority = {
            'shortname':xmldoc.getElementsByTagName("OeREBKRM09vs.Vorschriften.Amt")[0].getAttributeNode("TID").value, 
            'namede':xmldoc.getElementsByTagName("OeREBKRM09vs.Vorschriften.Amt")[0].getElementsByTagName("Text")[0].firstChild.data,
            'namefr':xmldoc.getElementsByTagName("OeREBKRM09vs.Vorschriften.Amt")[0].getElementsByTagName("Text")[1].firstChild.data,
            'namefr':xmldoc.getElementsByTagName("OeREBKRM09vs.Vorschriften.Amt")[0].getElementsByTagName("Text")[2].firstChild.data,
            'url':xmldoc.getElementsByTagName("OeREBKRM09vs.Vorschriften.Amt")[0].getElementsByTagName("AmtImWeb")[0].firstChild.data
            }
        vslegalprovisions = xmldoc.getElementsByTagName("OeREBKRM09vs.Vorschriften.Dokument")
        # Get the WMS and it's legend
        xtfwms = {
            'wmsurl':xmldoc.getElementsByTagName("OeREBKRM09trsfr.Transferstruktur.DarstellungsDienst")[0].getElementsByTagName("VerweisWMS")[0].firstChild.data,
            'wmslegend':xmldoc.getElementsByTagName("OeREBKRM09trsfr.Transferstruktur.DarstellungsDienst")[0].getElementsByTagName("LegendeImWeb")[0].firstChild.data
            }
        # GET restrictions
        xtfrestrictions = xmldoc.getElementsByTagName("OeREBKRM09trsfr.Transferstruktur.Eigentumsbeschraenkung")
        if xtfrestrictions:
            restrictions = []
            restriction = {}
            for xtfrestriction in xtfrestrictions:
                restriction = {
                    'restrictionid':xtfrestriction.getAttributeNode("TID").value,
                    'teneurde':xtfrestriction.getElementsByTagName("Aussage")[0].getElementsByTagName("Text")[0].firstChild.data,
                    'teneurfr':xtfrestriction.getElementsByTagName("Aussage")[0].getElementsByTagName("Text")[1].firstChild.data,
                    'teneurit':xtfrestriction.getElementsByTagName("Aussage")[0].getElementsByTagName("Text")[2].firstChild.data,
                    'topic':xtfrestriction.getElementsByTagName("Thema")[0].firstChild.data,
                    'legalstate':xtfrestriction.getElementsByTagName("Rechtsstatus")[0].firstChild.data,
                    'publishedsince':xtfrestriction.getElementsByTagName("publiziertAb")[0].firstChild.data,
                    'url':xtfrestriction.getElementsByTagName("DarstellungsDienst")[0].getAttributeNode("REF").value,
                    'authority':xtfrestriction.getElementsByTagName("ZustaendigeStelle")[0].getAttributeNode("REF").value
                    }
                restrictions.append(restriction)

        xtfvslinkprovisions = xmldoc.getElementsByTagName("OeREBKRM09trsfr.Transferstruktur.HinweisVorschrift")
        vslinkprovisions = []
        for vslinkprovision in xtfvslinkprovisions:
            vslinkprovisions.append({
                'origin':vslinkprovision.getElementsByTagName("Eigentumsbeschraenkung")[0].getAttributeNode("REF").value,
                'link':vslinkprovision.getElementsByTagName("Vorschrift")[0].getAttributeNode("REF").value
                })

        xtfvslinkreferences = xmldoc.getElementsByTagName("OeREBKRM09vs.Vorschriften.HinweisWeitereDokumente")
        vslinkreferences = []
        for vslinkreference in xtfvslinkreferences:
            vslinkreferences.append({
                'origin':vslinkreference.getElementsByTagName("Ursprung")[0].getAttributeNode("REF").value,
                'link':vslinkreference.getElementsByTagName("Hinweis")[0].getAttributeNode("REF").value
                })

        xtfvslegalprovisions = xmldoc.getElementsByTagName("OeREBKRM09vs.Vorschriften.Rechtsvorschrift")
        vslegalprovisions = []
        for vslegalprovision in xtfvslegalprovisions:
            vslegalprovisions.append({
                'provisionid':vslegalprovision.getAttributeNode("TID").value,
                'titel':vslegalprovision.getElementsByTagName("Text")[0].firstChild.data,
                'legalstate':vslegalprovision.getElementsByTagName("Rechtsstatus")[0].firstChild.data,
                'publishedsince':vslegalprovision.getElementsByTagName("publiziertAb")[0].firstChild.data,
                'authority':vslegalprovision.getElementsByTagName("ZustaendigeStelle")[0].getAttributeNode("REF").value,
                'url':vslegalprovision.getElementsByTagName("TextImWeb")[0].firstChild.data
                })

        xtfvsdocuments = xmldoc.getElementsByTagName("OeREBKRM09vs.Vorschriften.Dokument")
        vsdocuments = []
        for vsdocument in xtfvsdocuments:
            vsdocuments.append({
                'provisionid':vsdocument.getAttributeNode("TID").value,
                'titel':vsdocument.getElementsByTagName("Text")[0].firstChild.data,
                'legalstate':vsdocument.getElementsByTagName("Rechtsstatus")[0].firstChild.data,
                'publishedsince':vsdocument.getElementsByTagName("publiziertAb")[0].firstChild.data,
                'authority':vsdocument.getElementsByTagName("ZustaendigeStelle")[0].getAttributeNode("REF").value,
                'url':vsdocument.getElementsByTagName("TextImWeb")[0].firstChild.data
                })
                
        xtflegalprovisions = xmldoc.getElementsByTagName("OeREBKRM09trsfr.Transferstruktur.HinweisVorschrift")
        feature = []
        for xtflegalprovision in xtflegalprovisions:
            feature.append({
                'restrictionid':xtflegalprovision.getElementsByTagName("Eigentumsbeschraenkung")[0].getAttributeNode("REF").value,
                'provision':xtflegalprovision.getElementsByTagName("Vorschrift")[0].getAttributeNode("REF").value
                })

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
                            multipolygon = []
                            for polyline in polylines:
                                coordlist = []
                                for coords in polyline.childNodes:
                                    coordlist.append((
                                        float(coords.getElementsByTagName("C1")[0].firstChild.data), 
                                        float(coords.getElementsByTagName("C2")[0].firstChild.data)
                                        ))
                                #del coordlist[-1]
                                polygon = splPolygon(coordlist)
                                if len(polylines) > 1:
                                    multipolygon.append(polygon)
                                    geom = splMultiPolygon(multipolygon)
                                else:
                                    geom = polygon

            geometries.append({
                'tid':xtfgeom.getAttributeNode("TID").value,
                'restrictionid':xtfgeom.getElementsByTagName("Eigentumsbeschraenkung")[0].getAttributeNode("REF").value,
                'competentAuthority':xtfgeom.getElementsByTagName("ZustaendigeStelle")[0].getAttributeNode("REF").value,
                'legalstate':xtfgeom.getElementsByTagName("Rechtsstatus")[0].firstChild.data,
                'publishedsince':xtfgeom.getElementsByTagName("publiziertAb")[0].firstChild.data,
                #'metadata':xtfgeom.getElementsByTagName("MetadatenGeobasisdaten")[0].firstChild.data,
                'geom':geom.wkt
                })

        for geometry in geometries:
            if topicid ==  '103':
                xml_model = CHAirportProjectZonesPDF()
                xml_model.theme = translations['CHAirportProjectZonesThemeLabel'] # u'Zones réservées des installations aéroportuaires'
                xml_model.teneur = translations['CHAirportProjectZonesContentLabel'] # u'Limitation de la hauteur des bâtiments et autres obstacles'
            elif topicid ==  u'108':
                xml_model = CHAirportSecurityZonesPDF()
                xml_model.theme = translations['CHAirportSecurityZonesThemeLabel'] # u'Plan de la zone de sécurité des aéroports' 
                xml_model.teneur = translations['CHAirportSecurityZonesContentLabel'] # u'Limitation de la hauteur des bâtiments et autres obstacles'
            elif topicid ==  u'119':
                xml_model = CHPollutedSitesPublicTransportsPDF()
                xml_model.theme = translations['CHPollutedSitesPublicTransportsThemeLabel'] # u'Cadastre des sites pollués - domaine des transports publics'
                xml_model.teneur = translations['CHPollutedSitesPublicTransportsContentLabel'] # u'Sites pollués' 

            xml_model.codegenre = None
            if geometry['legalstate'] ==  u'inKraft':
                xml_model.statutjuridique = translations['legalstateLabelvalid'] # u'En vigueur' 
            else:
                xml_model.statutjuridique = translations['legalstateLabelmodification'] # u'En cours d\'approbation' 
            if geometry['publishedsince']:
                xml_model.datepublication = geometry['publishedsince']
            else:
                xml_model.datepublication = None
            # It is very important to set the SRID if it's not the default EPSG:4326 !!
            xml_model.idobj = str(extracttime)+'_'+str(geometry['restrictionid'])
            xml_model.geom = WKTSpatialElement(geometry['geom'], 21781)
            DBSession.add(xml_model)

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
        queryresult = DBSession.query(Property).filter_by(idemai=parcelInfo['featureid']).first()
        # We should check unicity of the property id and raise an exception if there are multiple results 
    elif (X > 0 and Y > 0):
        if  Y > X :
            pointYX = WKTSpatialElement('POINT('+str(Y)+' '+str(X)+')',SRS)
        else:
            pointYX = WKTSpatialElement('POINT('+str(X)+' '+str(Y)+')',SRS)
        queryresult = DBSession.query(Property).filter(Property.geom.gcontains(pointYX)).first()
        parcelInfo['featureid'] = queryresult.idemai
    else : 
        # to define
        return HTTPBadRequest(translations['HTTPBadRequestMsg'])

    parcelInfo['geom'] = queryresult.geom
    parcelInfo['area'] = int(DBSession.scalar(queryresult.geom.area))

    if isinstance(LocalName, (types.ClassType)) is False:
        queryresult1 = DBSession.query(LocalName).filter(LocalName.geom.intersects(parcelInfo['geom'])).first()
        parcelInfo['lieu_dit'] = queryresult1.nomloc # Flurname

    queryresult2 = DBSession.query(Town).filter(Town.geom.buffer(1).gcontains(parcelInfo['geom'])).first()

    parcelInfo['nummai'] = queryresult.nummai # Parcel number
    parcelInfo['type'] = queryresult.typimm # Parcel type
    parcelInfo['source'] = queryresult.source # Parcel type
    if parcelInfo['type'] == None :
        parcelInfo['type'] = translations['UndefinedPropertyType']

    if 'numcad' in queryresult2.__table__.columns.keys():
        parcelInfo['nomcad'] = queryresult2.cadnom

    parcelInfo['numcom'] = queryresult.numcom
    parcelInfo['nomcom'] = queryresult2.comnom
    parcelInfo['nufeco'] = queryresult2.nufeco
    parcelInfo['centerX'] = DBSession.scalar(queryresult.geom.centroid.x)
    parcelInfo['centerY'] = DBSession.scalar(queryresult.geom.centroid.y)
    parcelInfo['BBOX'] = get_bbox_from_geometry(DBSession.scalar(queryresult.geom.envelope.wkt))

    # the get_print_format function is not needed any longer as the paper size has been fixed to A4 by the cantons
    # but we keep the code because the decision will be revoked 
    # parcelInfo['printFormat'] = get_print_format(parcelInfo['BBOX'])

    return parcelInfo

def get_bbox_from_geometry(geometry):
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
