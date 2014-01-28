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
from crdppf.util.pdf_functions import get_translations, get_feature_info, get_print_format, get_XML
from crdppf.util.pdf_classes import PDFConfig, Extract, AppendixFile
from crdppf.util.get_feature_functions import get_features_function

from PyPDF2 import PdfFileMerger, PdfFileReader, PdfFileWriter

import logging

log = logging.getLogger(__name__)

@view_config(route_name='create_extract')
def create_extract(request):
    """The function collects alle the necessary data from the subfunctions and classes
       and then writes the pdf file of the extract."""

    # Start a session
    session = request.session

    logon = request.registry.settings['logon']
    if logon == 'False':
        logon = False
    else:
        logon = True

    log2 = None

    if logon is True:
        now = datetime.now()
        log.warning("Entering PDF extract, min.sec: %s", str(now.minute)+'.'+str(now.second))
        log2 = log

    # Create an instance of an extract
    extract = Extract(request, log2)

    if logon is True:
        now = datetime.now()
        log.warning("Created Extract class, min.sec: %s", str(now.minute)+'.'+str(now.second))
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
    extract.lang = lang

    if logon is True:
        now = datetime.now()
        log.warning("Created language init, min.sec: %s", str(now.minute)+'.'+str(now.second))
    # GET the application configuration parameters such as base paths,
    # working directory and other default parameters
    extract.load_app_config()

    if logon is True:
        now = datetime.now()
        log.warning("load_app_config(), min.sec: %s", str(now.minute)+'.'+str(now.second))
    # GET the PDF Configuration parameters such as the page layout, margins
    # and text styles
    extract.set_pdf_config()

    if logon is True:
        now = datetime.now()
        log.warning("set_pdf_config(), min.sec: %s", str(now.minute)+'.'+str(now.second))
    # promote often used variables to facilitate coding
    pdfconfig = extract.pdfconfig

    if logon is True:
        now = datetime.now()
        log.warning("pdfconfig, min.sec: %s", str(now.minute)+'.'+str(now.second))

    translations = extract.translations

    if logon is True:
        now = datetime.now()
        log.warning("translations, min.sec: %s", str(now.minute)+'.'+str(now.second))
    # to get vars defined in the buildout  use : request.registry.settings['key']
    pdfconfig.sld_url = extract.sld_url

    if logon is True:
        now = datetime.now()
        log.warning("extract.sld_url, min.sec: %s", str(now.minute)+'.'+str(now.second))

# *************************
# MAIN PROGRAM PART
#=========================

    # 1) If the ID of the parcel is set get the basic attributs of the property
    # else get the ID (idemai) of the selected parcel first using X/Y coordinates of the center 
    #----------------------------------------------------------------------------------------------------
    extract.featureInfo = get_feature_info(request,translations) # '1_14127' # test parcel or '1_11340'

    featureInfo = extract.featureInfo

    # complete the dictionnary for the parcel - to be put in the appconfig
    extract.featureInfo['operator'] = translations['defaultoperatortext']
    
    extract.featureid = featureInfo['featureid']
    extract.set_filename()

    # the get_print_format function which would define the ideal paper format and orientation for the
    # extract. It is not needed any longer as the paper size has been fixed to A4 portrait by the cantons
    # BUT there could be a change of opinion after the start phase, so we keep this code part for now
    extract.printformat = get_print_format(featureInfo['BBOX'],pdfconfig.fitratio)

    # 2) Get the parameters for the paper format and the map based on the feature's geometry
    #---------------------------------------------------------------------------------------------------
    extract.get_map_format()

    # again we promote the variables one level
    printformat = extract.printformat

    # 3) Get the list of all the restrictions by topicorder set in a column
    #-------------------------------------------
    extract.topics = DBSession.query(Topics).order_by(Topics.topicorder).all()

    # Get the community name and escape special chars to place the logo in the header of the title page
    municipality = featureInfo['nomcom'].strip()

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

    # === TO IMPROVE thus code is left commented
    # Get the data for the federal data layers using the map extend
    #~ for topic in extract.topics:
        #~ if topic.topicid in extract.appconfig.ch_topics:
            #~ xml_layers = []
            #~ for xml_layer in topic.layers:
                #~ xml_layers.append(xml_layer.layername)
            #~ get_XML(extract.featureInfo['geom'],topic.topicid)

    # 4) Create the title page for the pdf extract
    #--------------------------------------------------



    extract.get_site_map()

    # 5) Create the pages of the extract for each topic in the list
    #---------------------------------------------------
    # Thematic pages
    count = 1
    for topic in extract.topics:
        if logon is True:
            now = datetime.now()
            log.warning("Begin of topic no %s, topic_id: %s min.sec: %s", count, topic.topicid, str(now.minute)+'.'+str(now.second))
        add = extract.add_topic(topic)

        if logon is True:
            now = datetime.now()
            log.warning("End of topic no %s, min.sec: %s", count, str(now.minute)+'.'+str(now.second))
            count += 1
        # to print the topics in ther right order - this could probably be done in a more elegant way
        extract.topicorder[topic.topicorder] = topic.topicid

    # Write pdf file to disc
    extract.get_title_page()

    if logon is True:
        now = datetime.now()
        log.warning("get_title_page, min.sec: %s", str(now.minute)+'.'+str(now.second))

    # Create the table of content
    #--------------------------------------------------
    extract.get_toc()

    if logon is True:
        now = datetime.now()
        log.warning("get_toc, min.sec: %s", str(now.minute)+'.'+str(now.second))
    # Create the list of appendices
    #--------------------------------------------------
    extract.Appendices()

    if logon is True:
        now = datetime.now()
        log.warning("Appendices, min.sec: %s", str(now.minute)+'.'+str(now.second))

    count = 1
    for topic in extract.topicorder.values():
        extract.write_thematic_page(topic)
        if logon is True:
            now = datetime.now()
            log.warning("write_thematic_page, page n° %s min.sec: %s", count, str(now.minute)+'.'+str(now.second))
        count += 1
    # Set the page number once all the pages are printed
    for key in extract.pages.keys():
        extract.pages[key] = extract.pages[key].replace('{no_pg}', str(' ')+str(key))

    extract.output(pdfconfig.pdfpath+pdfconfig.pdfname+'.pdf','F')

    if logon is True:
        now = datetime.now()
        log.warning("File created, min.sec: %s", str(now.minute)+'.'+str(now.second))

    path = extract.appconfig.legaldocsdir + str('pas_disponible.pdf')
    exception = extract.appconfig.legaldocsdir + str('exception.pdf')
    
    j = 1
    filenames = []
    # If report type is not 'reduced': Add a title page in front of every attached pdf
    if extract.reportInfo['type'] != 'reduced' and extract.reportInfo['type'] != 'reducedcertified':
        filenames = [pdfconfig.pdfpath+pdfconfig.pdfname+'.pdf']
        for appendix in extract.appendix_entries:
            appendixfile = AppendixFile()
            appendixfile.creationdate = str(extract.creationdate)
            appendixfile.timestamp = str(extract.timestamp)
            appendixfile.reporttype = str(extract.reportInfo['type'])
            appendixfile.translations = get_translations(lang)
            appendixfile.current_page = ' A' + str(j)
            appendixfile.load_app_config()
            appendixfile.set_pdf_config()
            appendixfile.municipalitylogopath = appendixfile.appconfig.municipalitylogodir + municipality_escaped + '.png'
            appendixfile.municipality = municipality # to clean up once code modified
            appendixfile.add_page()
            appendixfile.set_margins(*pdfconfig.pdfmargins)
            appendixfile.set_y(55)
            appendixfile.set_link(str(j))
            appendixfile.set_font(*pdfconfig.textstyles['title3'])
            appendixfile.cell(15, 10, str('Annexe '+str(j)), 0, 1, 'L')
            appendixfile.cell(100, 10, str(appendix['title']), 0, 1, 'L')
            appendixfile.output(pdfconfig.pdfpath+pdfconfig.pdfname+'_a'+str(j)+'.pdf','F')
            filenames.append(pdfconfig.pdfpath+pdfconfig.pdfname+'_a'+str(j)+'.pdf')
            filenames.append(appendix['url'])
            j += 1
        merger = PdfFileMerger()
        for filename in filenames:
            try:
                merger.append(PdfFileReader(file(filename, 'rb')))
            except:
                merger.append(PdfFileReader(file(exception, 'rb')))

        merger.write(pdfconfig.pdfpath+pdfconfig.pdfname+'.pdf')
        if logon is True:
            now = datetime.now()
            log.warning("Appendices, min.sec: %s", str(now.minute)+'.'+str(now.second))

    response = FileResponse(
        pdfconfig.pdfpath + pdfconfig.pdfname + '.pdf',
        request,
        None,
        'application/pdf'
    )
    response. content_disposition='attachment; filename='+ pdfconfig.pdfname +'.pdf'
    return response
