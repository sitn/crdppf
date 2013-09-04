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
from crdppf.util.pdf_functions import getBBOX, getTranslations, getPrintFormat, getFeatureInfo
from crdppf.util.pdf_functions import getRestrictions, getMap, getAppendices
from crdppf.util.pdf_functions import getTOC, getTitlePage

from crdppf.util.pdf_classes import PDFConfig, Extract
from crdppf.views.get_features import get_features, get_features_function


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


@view_config(route_name='create_extract')
def create_extract(request):
    """Writes the pdf file."""
    session = request.session

    # to get vars defined in the buildout  use : request.registry.settings['key']
    crdppf_wms = request.registry.settings['crdppf_wms']

    # other basic parameters
    extract = Extract()
    extract.today = datetime.now()
    
    # GET the PDF Configuration parameters
    extract.pdfconfig = PDFConfig(request)
    pdfconfig = extract.pdfconfig

    # GET Multilingual labels for the selected language
    if 'lang' not in session:
        lang = request.registry.settings['default_language'].lower()
    else : 
        lang = session['lang'].lower()

    extract.translations = getTranslations(lang)
    translations = extract.translations

# *************************
# MAIN PROGRAM PART
#=========================

    # 1) If the ID of the parcel is set get the basic attributs 
    # else get the ID (idemai) of the selected parcel first using X/Y coordinates of the center 
    #----------------------------------------------------------------------------------------------------
    extract.featureInfo = getFeatureInfo(request, translations) # '1_14127' # test parcel or '1_11340'
    featureInfo = extract.featureInfo

    # 2) Get the parameters for the paper format and the map based on the feature's geometry
    #---------------------------------------------------------------------------------------------------
    map_params = {'width':featureInfo['printFormat']['mapWidth'], 'height':featureInfo['printFormat']['mapHeight']}
    map_params['bboxCenterX'] = (featureInfo['BBOX']['maxX']+featureInfo['BBOX']['minX'])/2
    map_params['bboxCenterY'] = (featureInfo['BBOX']['maxY']+featureInfo['BBOX']['minY'])/2

    pdf_format = extract.featureInfo['printFormat']

    # 3) Get the list of all the restrictions
    #-------------------------------------------
    extract.topics = DBSession.query(Topics).order_by(Topics.topicorder).all()

    #topiclist = DBSession.query(Topics).order_by(Topics.topicorder).all()

    # 4) Create the title page for the pdf extract
    #--------------------------------------------------

    # Get the community name and escape special chars to place the logo in the header of the title page
    commune = featureInfo['nomcom']
    
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
        [u'(NE)', '']
    ]

    for char in conversion:
        commune = commune.replace(char[0], char[1])
    
    pdf = getTitlePage(extract.featureInfo, crdppf_wms, featureInfo['nomcom'], commune, pdfconfig, translations)

    # 5) Create an empty pdf for the table of content
    #--------------------------------------------------
    toc = getTOC(commune, pdfconfig, translations)

    # 6) Create an empty pdf for the ?annexes?
    #-------------------------------------------------- 
    appendices = getAppendices(commune, pdfconfig, translations)

    # 7) Create the pages of the extract for each topic in the list
    #---------------------------------------------------
    # Thematic pages

    # Loop on each topic
    extract.restrictionList = []
    
    for topic in extract.topics:
        # if geographic layers are defined for the topic, get the information
        if topic.layers :
            if topic.topicid == '103':
                chdata = urllib2.urlopen('https://api.geo.admin.ch/feature/search?lang=en&layers=ch.bazl.projektierungszonen-flughafenanlagen&bbox=680585,255022,686695,259951&no_geom=true')
                json = chdata.read()
                features = sloads(json)
                if features['features'] :
                    for feature in features['features']:
                        feature['properties']['layerName'] = feature['properties']['layer_id'] 
                        feature['properties']['featureClass'] = 'intersects'
                    extract.restrictionList.append(features['features'])
            else:
                layers = []
                for layer in topic.layers:
                    layers.append(layer.layername)
                if isinstance(layers, list):
                    for sublayer in layers:
                        params = {
                            'id':featureInfo['idemai'],
                            'layerList':str(sublayer)
                            }
                        features = get_features_function(params)
                        if features :
                            extract.restrictionList.append(features)
                            features = None
                else:
                    params = {
                        'id':featureInfo['idemai'],
                        'layerList':str(layers)
                        }
                    extract.restrictionList = get_features_function(params)

        else : 
            extract.restrictionList = []

        if len(extract.restrictionList) > 0 :
            # Parameter to set to 'true' if restrictions in the neighborhood are to be mentioned also
            neighborhood = False

           # PAGE X !!! > à pousser plus loin ; d'abord remplir un tableau avec toutes les valeurs puis créer extrait en boucle page par page
            pdf.add_page(str(pdf_format['orientation'] + ',' + pdf_format['format']))
            pdf.set_margins(*pdfconfig.pdfmargins)

            # Thematic map/Carte thématique/Thematische Karte
            if topic.layers:

                #set the title for the restrictions
                pdf.add_toc_entry(topic.topicid, pdf.page_no(), str(topic.topicname.encode('iso-8859-1')), 1, '')

                # Get the map and the legend
                topic.mappath, topic.legendpath = getMap(topic.layers, topic.topicid, crdppf_wms, map_params, pdf_format)
                # Place the map
                map = pdf.image(topic.mappath, 65, pdfconfig.headermargin, pdf_format['width'], pdf_format['height'])
                pdf.rect(65, pdfconfig.headermargin, pdf_format['width'], pdf_format['height'], '')
                # Define the size of the legend container
                legendbox_width = 40
                legendbox_height = pdf_format['height'] 
                legendbox_proportion = float(legendbox_width-4) / float(legendbox_height-20)
                
                # draw the legend container
                pdf.rect(pdfconfig.leftmargin, pdfconfig.headermargin, legendbox_width, legendbox_height, '')
                
                # define cells with border for the legend and the map
                pdf.set_xy(28, pdfconfig.headermargin+3)
                pdf.set_font(*pdfconfig.textstyles['bold'])
                pdf.cell(50, 6, translations['legendlabel'], 0, 1, 'L')
                y= pdf.get_y()
                pdf.set_font(*pdfconfig.textstyles['normal'])
                if  len(topic.legendpath) > 0:
                    max_legend_width_px = 0
                    tot_legend_height_px = 0
                    sublegends = []

                    for graphic in topic.legendpath:
                        tempimage = Image.open(str(graphic)+'.png')
                        legend_width_px, legend_height_px = tempimage.size
                        sublegends.append([graphic,legend_width_px, legend_height_px])
                        if legend_width_px > max_legend_width_px :
                            max_legend_width_px = legend_width_px
                        tot_legend_height_px += legend_height_px

                    # number of px per mm of legend width = width proportion
                    width_proportion = float((max_legend_width_px)) / float(legendbox_width-4)
                    height_proportion = float(tot_legend_height_px) / float(legendbox_height-20)
                    
                    # check if using this proportion of px/mm the totol_legend_height fits in the available space else fit the height and adapt width
                    supposed_height_mm = float(tot_legend_height_px) / width_proportion
                    if supposed_height_mm < float(legendbox_height-20) : 
                        limit_proportion = width_proportion
                    else : 
                        limit_proportion = height_proportion
                        
                    if limit_proportion < 5:
                        limit_proportion = 5

                    for path, width, height in sublegends:
                        y = pdf.get_y()
                        legend = pdf.image(path+'.png',26, y, float(width)/limit_proportion)
                        pdf.set_y(y+(float(height)/limit_proportion))

            else : 
                if topic.layers :
                    pdf.add_toc_entry(topic.topicid,'', str(topic.topicname.encode('iso-8859-1')), 0,'')
                
                y = pdf.get_y()
                pdf.multi_cell(0, 6, translations['maperrorlabel'])
                pdf.ln()

            pdf.set_y(40)
            pdf.set_font(*pdfconfig.textstyles['title3'])
            pdf.multi_cell(0, 6, str(topic.topicname.encode('iso-8859-1')), 0, 1, 'L')
            y = pdf.get_y()
            pdf.set_y(y+110)

            for features in extract.restrictionList:
                for feature in features:
                    if feature['properties'] :

                        # Check if property is affected by the restriction otherwise just mention restrictions in neighborhood
                        if feature['properties']['featureClass'] == 'intersects' or feature['properties']['featureClass'] == 'within' :

                            # Description of the interaction of a restriction with the property
                            #~ if feature['properties']['featureClass']:
                                #~ pdf.set_font(*pdfconfig.textstyles['italic'])
                                #~ pdf.cell(100,6,unicode('Type d\'interaction : ','utf-8').encode('iso-8859-1') + feature['properties']['featureClass'].encode('iso-8859-1'),0,1,'L') 
 
                            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                            # !!! Hardcoding the returned attribute from our productive base for testing purposes !!! 
                            # !!! TO BE REPLACED BY THE TRANSFERT/EXTRACT MODEL MAPPING               !!!
                            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                            if feature['properties']['layerName'] == 'at14_zones_communales':
                                pdf.set_font(*pdfconfig.textstyles['bold'])
                                pdf.cell(55, 5, translations['contentlabel'].encode('iso-8859-1'), 0, 0, 'L')
                                pdf.set_font(*pdfconfig.textstyles['normal'])
                                pdf.multi_cell(0, 5, feature['properties']['nom_communal'] .encode('iso-8859-1').strip(), 0, 1, 'L')

                            elif feature['properties']['layerName'] == 'en05_degres_sensibilite_bruit':
                                pdf.set_font(*pdfconfig.textstyles['bold'])
                                pdf.cell(55, 5, translations['contentlabel'].encode('iso-8859-1'), 0, 0, 'L')
                                pdf.set_font(*pdfconfig.textstyles['normal'])
                                pdf.cell(60, 5, feature['properties']['type_ds'] .encode('iso-8859-1'), 0, 1, 'L')

                            elif feature['properties']['layerName'] == 'en01_zone_sect_protection_eaux':
                                pdf.set_font(*pdfconfig.textstyles['bold'])
                                pdf.cell(55, 5, translations['contentlabel'].encode('iso-8859-1'), 0, 0, 'L')
                                pdf.set_font(*pdfconfig.textstyles['normal'])
                                pdf.cell(60, 5, feature['properties']['categorie'] .encode('iso-8859-1'), 0, 1, 'L')

                            elif feature['properties']['layerName'] == 'clo_couloirs':
                                pdf.set_font(*pdfconfig.textstyles['bold'])
                                pdf.cell(55, 5, translations['contentlabel'].encode('iso-8859-1'), 0, 0, 'L')
                                pdf.set_font(*pdfconfig.textstyles['normal'])
                                pdf.cell(60, 5, feature['properties']['type'] .encode('iso-8859-1'), 0, 1, 'L')

                            elif feature['properties']['layerName'] == 'clo_cotes_altitude_surfaces':
                                pdf.set_font(*pdfconfig.textstyles['bold'])
                                pdf.cell(55, 5, translations['contentlabel'].encode('iso-8859-1'), 0, 0, 'L')
                                pdf.set_font(*pdfconfig.textstyles['normal'])
                                pdf.cell(60, 5, str(feature['properties']['cote_alt_obstacles_minimum'] ).encode('iso-8859-1'), 0, 1, 'L')

                            elif feature['properties']['layerName'] in ['en07_canepo_accidents','en07_canepo_decharges_points','en07_canepo_decharges_polygones','en07_canepo_entreprises_points']:
                                pdf.set_font(*pdfconfig.textstyles['bold'])
                                pdf.cell(55, 5, translations['contentlabel'].encode('iso-8859-1'), 0, 0, 'L')
                                pdf.set_font(*pdfconfig.textstyles['normal'])
                                pdf.cell(60, 5, unicode(feature['properties']['statut_osi'] ).encode('iso-8859-1'), 0, 1, 'L')

                            elif feature['properties']['layerName'] == 'ch.bazl.projektierungszonen-flughafenanlagen':
                                pdf.set_font(*pdfconfig.textstyles['bold'])
                                pdf.cell(55, 5, translations['contentlabel'].encode('iso-8859-1'), 0, 0, 'L')
                                pdf.set_font(*pdfconfig.textstyles['normal'])
                                pdf.cell(60, 5, unicode(feature['properties']['layer_id'] ).encode('iso-8859-1'), 0, 1, 'L')

                            else: 
                                # Attributes of topic layers intersection
                                for key, value in feature['properties'].iteritems():
                                    if value is not None :
                                        if key !='layerName' and key != 'featureClass':
                                            pdf.set_font(*pdfconfig.textstyles['bold'])
                                            pdf.cell(55, 5, translations['contentlabel'].encode('iso-8859-1'), 0, 0, 'L')
                                            pdf.set_font(*pdfconfig.textstyles['normal'])
                                            if isinstance(value, float) or isinstance(value, int):
                                                value = str(value)
                                            pdf.cell(60, 5, value.encode('iso-8859-1'), 0, 1, 'L')
                # it has been decided that only restrictions that interact with the selected parcel are mentionned -  otherwise other interactions could be displayed
                        #~ elif feature['properties']['featureClass'] == 'adjacent':
                            #~ neighborhood = 'true'
                #~ if neighborhood == 'true':
                    #~ pdf.set_font(*pdfconfig.textstyles['bold'])
                    #~ pdf.cell(100,6,unicode('Nom de la donnée : ','utf-8').encode('iso-8859-1') +feature['properties']['layerName'].encode('iso-8859-1'),0,1,'L') 
                    #~ pdf.set_font(*pdfconfig.textstyles['italic'])
                    #~ pdf.cell(100,6,unicode('Remarque: Il y a des immeubles voisins affectés par cette restriction.','utf-8').encode('iso-8859-1'),0,1,'L') 
                
                #~ y = pdf.get_y()
                #~ pdf.set_y(y+5)
                
                # Legal Provisions/Dispositions juridiques/Gesetzliche Bestimmungen
                y = pdf.get_y()
                pdf.set_y(y+5)
                pdf.set_font(*pdfconfig.textstyles['bold'])
                pdf.cell(55, 6, translations['legalprovisionslabel'], 0, 0, 'L')
                pdf.set_font(*pdfconfig.textstyles['normal'])
                if topic.legalprovisions:
                    count = 0 
                    for provision in topic.legalprovisions:
                        pdf.add_appendix(topic.topicid, 'A'+str(count+1), unicode(provision.officialtitle).encode('iso-8859-1'), unicode(provision.legalprovisionurl).encode('iso-8859-1'))
                        pdf.cell(0, 5, unicode(provision.officialtitle).encode('iso-8859-1'), 0, 1, 'L')
                        pdf.set_text_color(0, 0, 255)
                        pdf.set_x(80)
                        pdf.multi_cell(0, 6, unicode(provision.legalprovisionurl).encode('iso-8859-1'))
                        pdf.set_text_color(0, 0, 0)
                else:
                        pdf.multi_cell(0, 6, unicode('None').encode('iso-8859-1'))

            # References and complementary information/Informations et renvois supplémentaires/Verweise und Zusatzinformationen
            y = pdf.get_y()
            pdf.set_y(y+5)
            pdf.set_font(*pdfconfig.textstyles['bold'])
            pdf.cell(55, 6, translations['referenceslabel'], 0, 0, 'L')
            pdf.set_font(*pdfconfig.textstyles['normal'])
            if topic.references:
                for reference in topic.references:
                    pdf.multi_cell(0, 6, unicode(reference.officialtitle).encode('iso-8859-1'))
            else:
                    pdf.multi_cell(0, 6, unicode('None','utf-8').encode('iso-8859-1')) 

            # Ongoing amendments/Modifications en cours/Laufende Änderungen
            y = pdf.get_y()
            pdf.set_y(y+5)
            pdf.set_font(*pdfconfig.textstyles['bold'])
            pdf.cell(55, 6, translations['temporaryprovisionslabel'], 0, 0, 'L')
            pdf.set_font(*pdfconfig.textstyles['normal'])
            if topic.temporaryprovisions:
                for temp_provision in topic.temporaryprovisions:
                    pdf.multi_cell(0, 6, unicode(temp_provision.officialtitle).encode('iso-8859-1'), 0, 1, 'L')
                    if temp_provision.temporaryprovisionurl :
                        pdf.set_x(80)
                        pdf.multi_cell(0, 6, unicode(temp_provision.temporaryprovisionurl).encode('iso-8859-1'))
            else:
                    pdf.multi_cell(0, 6, unicode('None','utf-8').encode('iso-8859-1'), 0, 1, 'L')

            # Competent Authority/Service competent/Zuständige Behörde
            y = pdf.get_y()
            pdf.set_y(y+5)
            pdf.set_font(*pdfconfig.textstyles['bold'])
            pdf.cell(55, 3.9, translations['competentauthoritylabel'], 0, 0, 'L')
            pdf.set_font(*pdfconfig.textstyles['normal'])
            
            if topic.authority.authorityname is not None:
                pdf.cell(120, 3.9, topic.authority.authorityname.encode('iso-8859-1'), 0, 1, 'L')
            if topic.authority.authoritydepartment is not None:
                pdf.cell(55, 3.9, str(' '), 0, 0, 'L')
                pdf.cell(120, 3.9, topic.authority.authoritydepartment.encode('iso-8859-1'), 0, 1, 'L')
            if topic.authority.authorityphone1 is not None:
                pdf.cell(55, 3.9, str(' '), 0, 0, 'L')
                pdf.cell(120, 3.9, translations['phonelabel']+topic.authority.authorityphone1.encode('iso-8859-1'), 0, 1, 'L')
            if topic.authority.authoritywww is not None:
                pdf.cell(55, 3.9, str(' '), 0, 0, 'L')
                pdf.cell(120, 3.9, translations['webadresslabel']+topic.authority.authoritywww.encode('iso-8859-1'),0,1,'L')        
            
            # Legal bases/Bases légales/Gesetzliche Grundlagen
            y = pdf.get_y()
            pdf.set_y(y+5)
            pdf.set_font(*pdfconfig.textstyles['bold'])
            pdf.cell(55, 6, translations['legalbaseslabel'], 0, 0, 'L')
            pdf.set_font(*pdfconfig.textstyles['normal'])
            if topic.legalbases:
                for legalbase in topic.legalbases:
                    pdf.multi_cell(0, 6, legalbase.officialtitle)
            else:
                pdf.multi_cell(0, 6, translations['placeholderlabel'])

        # Set the titles
        if not topic.layers and not extract.restrictionList :
            pdf.add_toc_entry(topic.topicid,'', str(topic.topicname.encode('iso-8859-1')), 2,'')
    
    # Get the page count of all the chapters
    nb_pages_pdf =  len(pdf.pages)
    nb_pages_toc =  len(toc.pages)
    nb_pages_appendix =  len(appendices.pages)

    nb_pages_total = nb_pages_pdf + nb_pages_toc + nb_pages_appendix
    delta = nb_pages_toc + nb_pages_appendix

    # Add a new page with the table of content
    if pdf.toc_entries :
        pdf.add_page()
        pdf.set_margins(*pdfconfig.pdfmargins)

        # List of all topics with a restriction for the selected parcel 
        for entry, column in pdf.toc_entries.iteritems() :
            if column['categorie'] == 1 :
                toc.set_font(*pdfconfig.textstyles['bold'])
                toc.cell(12, 6, str(column['no_page']), 'B', 0, 'L')
                toc.cell(118, 6, str(column['title']), 'LB', 0, 'L')
                if len(column['appendices']) > 0:
                    appendices_list = set(column['appendices'])
                    toc.cell(15, 6, ', '.join(appendices_list), 'LB', 0, 'C')
                else:
                    toc.cell(15, 6, '', 'LB', 0, 'L')
                toc.cell(15, 6, '', 'LB', 1, 'L')

        toc.ln()
        toc.ln()
        toc.set_font(*pdfconfig.textstyles['tocbold'])
        toc.multi_cell(0, 5, translations['notconcerndbyrestrictionlabel'], 'B', 1, 'L')
        toc.ln()

        for entry, column in pdf.toc_entries.iteritems() :
            if column['categorie'] == 0 :
                toc.set_font(*pdfconfig.textstyles['tocbold'])
                toc.cell(118, 6, str(column['title']), '', 0, 'L')
                toc.cell(15, 6, '', '', 0, 'L')
                toc.cell(15, 6, '', '', 1, 'L')
                
        toc.ln()
        toc.set_font(*pdfconfig.textstyles['tocbold'])
        toc.multi_cell(0, 5, translations['restrictionnotavailablelabel'], 'B', 1, 'L')
        toc.ln()
        
        for entry, column in pdf.toc_entries.iteritems() :
            if column['categorie'] == 2 :
                toc.set_font(*pdfconfig.textstyles['tocbold'])
                toc.cell(118,6,str(column['title']),0,0,'L')
                toc.cell(15,6,'',0,0,'L')
                toc.cell(15,6,'',0,1,'L')

        toc.ln()
        toc.set_font(*pdfconfig.textstyles['tocbold'])
        toc.multi_cell(0, 5, translations['restrictionnotlegallybindinglabel'], 'B', 1, 'L')
        toc.ln()
        toc.set_font(*pdfconfig.textstyles['tocnormal'])
        toc.cell(118, 6, translations['norestrictionlabel'], 0, 0, 'L')
        toc.cell(15, 6, str(''), 0, 0, 'L')
        toc.cell(15, 6, str(''), 0, 1, 'L')

    tt = pdf.TOC()
    ttt = pdf.Appendices()

    if pdf.appendix_entries :
        pdf.add_page()
        pdf.set_margins(*pdfconfig.pdfmargins)
        index = 1
        for appendix in pdf.appendix_entries:
            appendices.set_font(*pdfconfig.textstyles['tocbold'])
            appendices.cell(15, 6, str('A'+str(index)), 0, 0, 'L')
            appendices.cell(120, 6, str(appendix['title']), 0, 1, 'L')
            appendices.set_x(40)
            appendices.set_font(*pdfconfig.textstyles['tocurl'])
            appendices.set_text_color(*pdfconfig.urlcolor)
            appendices.multi_cell(0, 5, str(appendix['url']))
            appendices.set_text_color(*pdfconfig.defaultcolor)
            index += index

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
    pdf.output(pdfconfig.pdfpath+pdfconfig.pdfname+'.pdf','F')

    response = FileResponse(
        pdfconfig.pdfpath + pdfconfig.pdfname + '.pdf',
        request,
        None,
        'application/pdf'
    )
    response. content_disposition='attachment; filename='+ pdfconfig.pdfname +'.pdf'
    return response
