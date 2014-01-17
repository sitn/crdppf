# -*- coding: UTF-8 -*-
from pyramid.response import FileResponse, Response
from pyramid.renderers import render_to_response
from pyramid.httpexceptions import HTTPForbidden, HTTPBadRequest
from pyramid.view import view_config


from datetime import datetime, time
import httplib, urllib2
import pkg_resources
from geojson import Feature, FeatureCollection, dumps, loads as gloads
from simplejson import loads as sloads,dumps as sdumps
from geoalchemy import *
from PIL import Image

from crdppf.models import *
from crdppf.util.pdf_functions import get_bbox, get_translations, get_feature_info, get_print_format

from crdppf.util.pdf_classes import PDFConfig, Extract
from crdppf.views.get_features import get_features, get_features_function


@view_config(route_name='create_extract')
def create_extract(request):
    """The function collects alle the necessary data from the subfunctions and classes
       and then writes the pdf file of the extract."""

    # Start a session
    session = request.session

    # Create an instance of an extract
    extract = Extract(request)

    # Define the extract type if not set in the request parameters
    # defaults to 'standard': no certification, with pdf attachements
    # other values :
    # certified : with certification and with all pdf attachements
    # reduced : no certification, no pdf attachements
    # reducedcertified : with certification, without pdf attachments

    extract.reportInfo = {}
    defaulttype = 'standard'

    if request.params.get('type') :
        extract.reportInfo['type'] = str(request.params.get('type').lower())
    else : 
        extract.reportInfo['type'] = defaulttype

    # Define language to get multilingual labels for the selected language
    # defaults to 'fr': french - this may be changed in the appconfig
    if 'lang' not in session:
        lang = request.registry.settings['default_language'].lower()
    else : 
        lang = session['lang'].lower()
    extract.translations = get_translations(lang)

    # GET the application configuration parameters
    extract.load_app_config(request.registry.settings['app_config'])
    
    # GET the PDF Configuration parameters
    extract.set_pdf_config(request.registry.settings['pdf_config'])

    # promote often used variables to facilitate coding
    pdfconfig = extract.pdfconfig
    translations = extract.translations

    # to get vars defined in the buildout  use : request.registry.settings['key']
    extract.wms = request.registry.settings['crdppf_wms']
    pdfconfig.sld_url = extract.sld_url


# *************************
# MAIN PROGRAM PART
#=========================

    # 1) If the ID of the parcel is set get the basic attributs of the property
    # else get the ID (idemai) of the selected parcel first using X/Y coordinates of the center 
    #----------------------------------------------------------------------------------------------------
    extract.featureInfo = get_feature_info(request,translations) # '1_14127' # test parcel or '1_11340'
    featureInfo = extract.featureInfo

    # complete the dictionnary for the parcel - to be put in the appconfig
    extract.featureInfo['operator'] = 'Portail Internet'
    
    extract.featureid = featureInfo['featureid']
    extract.set_filename()

    # the get_print_format function which would define the ideal paper format and orientation for the
    # extract. It is not needed any longer as the paper size has been fixed to A4 portrait by the cantons
    extract.printformat = get_print_format(featureInfo['BBOX'],pdfconfig.fitratio)

    # 2) Get the parameters for the paper format and the map based on the feature's geometry
    #---------------------------------------------------------------------------------------------------
    extract.get_map_format()
    printformat = extract.printformat

    # 3) Get the list of all the restrictions
    #-------------------------------------------
    extract.topics = DBSession.query(Topics).order_by(Topics.topicorder).all()

    # Get the community name and escape special chars to place the logo in the header of the title page
    municipality = featureInfo['nomcom'].strip()
    #  START Temporary code for development after municipality fusions 
    if municipality in ['Colombier (NE)','Auvernier','Bôle']:
        municipality = 'Milvignes'
        extract.featureInfo['nomcom'] = 'Milvignes'
        extract.featureInfo['nufeco'] = '6416'

    if municipality in ['Brot-Plamboz','Plamboz']:
        municipality = 'Brot-Plamboz'
        extract.featureInfo['nomcom'] = 'Brot-Plamboz'
        extract.featureInfo['nufeco'] = '6433'
    
    if municipality in ['Neuchâtel','La Coudre']:
        municipality = 'Neuchatel'
        extract.featureInfo['nomcom'] = 'Neuchâtel'
        extract.featureInfo['nufeco'] = '6458'

    if municipality in ['Les Eplatures']:
        municipality = 'La Chaux-de-Fonds'
        extract.featureInfo['nomcom'] = 'La Chaux-de-Fonds'
        extract.featureInfo['nufeco'] = '6421'

    if municipality in ['Boudevilliers','Cernier','Chézard-Saint-Martin','Coffrane','Dombresson','Engollon','Fenin-Vilars-Saules','Fontaines','Fontainemelon','Les Geneveys-sur-Coffrane','Les Hauts-Geneveys','Montmollin','Le Pâquier','Savagnier','Villiers']:
        municipality = 'Val-de-Ruz'
        extract.featureInfo['nomcom'] = 'Val-de-Ruz'
        extract.featureInfo['nufeco'] = '6487'
    # END temporary code

    # AS does the german language, the french contains a few accents we have to replace to fetch the banner which has no accents in its pathname...
    conversion = [
        [u'â', 'a'],
        [u'ä' ,'a'],
        [u'à', 'a'],
        [u'ô', 'o'],
        [u'ö', 'o'],
        [u'ò', 'o'],
        [u'û', 'u'],
        [u'ü', 'u'],
        [u'ù', 'u'],
        [u'î', 'i'],
        [u'ï', 'i'],
        [u'ì', 'i'],
        [u'ê', 'e'],
        [u'ë', 'e'],
        [u'è', 'e'],
        [u'é', 'e'],
        [u' ', ''],
        [u'-','_'],
        [u'(NE)', ''],
        [u' (NE)', '']
    ]

    municipality_escaped = municipality.strip()

    for char in conversion:
        municipality_escaped = municipality_escaped.replace(char[0], char[1])

    extract.municipalitylogopath = extract.appconfig.municipalitylogodir + municipality_escaped + '.png'
    extract.municipality = municipality # to clean up once code modified

    # 4) Create the title page for the pdf extract
    #--------------------------------------------------
    extract.get_site_map()
    # enable auto page break
    extract.set_auto_page_break(1,margin=25)

    # 5) Create the pages of the extract for each topic in the list
    #---------------------------------------------------
    # Thematic pages
    
    for topic in extract.topics:
        extract.add_topic(topic)

    # Write pdf file to disc
    extract.get_title_page()
    
    # Create the table of content
    #--------------------------------------------------
    extract.get_toc()
    
    # Create the list of appendices
    #--------------------------------------------------
    if extract.reportInfo['type'] != 'reduced' and extract.reportInfo['type'] != 'reducedcertified':
        extract.Appendices()

    for topic in extract.topiclist:
        extract.write_thematic_page(topic)

    j = 1
    # If report type is not 'reduced': Add a title page in front of every attached pdf
    if extract.reportInfo['type'] != 'reduced' and extract.reportInfo['type'] != 'reducedcertified':
        for appendix in extract.appendix_entries:
            extract.add_page()
            extract.set_margins(*pdfconfig.pdfmargins)
            extract.set_y(55)
            extract.set_link(str(j))
            extract.set_font(*pdfconfig.textstyles['title3'])
            extract.cell(15, 10, str('Annexe '+str(j)), 0, 1, 'L')
            extract.cell(100, 10, str(appendix['title']), 0, 1, 'L')
            j = j+1
                
    # Set the page number once all the pages are printed
    for key in extract.pages.keys():
        extract.pages[key] = extract.pages[key].replace('{no_pg}', str(' ')+str(key))

    extract.output(pdfconfig.pdfpath+pdfconfig.pdfname+'.pdf','F')

    response = FileResponse(
        pdfconfig.pdfpath + pdfconfig.pdfname + '.pdf',
        request,
        None,
        'application/pdf'
    )
    response. content_disposition='attachment; filename='+ pdfconfig.pdfname +'.pdf'
    return response
