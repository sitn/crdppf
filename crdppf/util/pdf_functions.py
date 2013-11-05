# -*- coding: UTF-8 -*-

from owslib.wms import WebMapService
import pkg_resources
from datetime import datetime
import urllib
from PIL import Image

from crdppf.models import *

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
