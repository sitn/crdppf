# -*- coding: UTF-8 -*-
from pyramid.response import FileResponse, Response
from pyramid.renderers import render_to_response
from pyramid.httpexceptions import HTTPForbidden, HTTPBadRequest
from pyramid.view import view_config



from datetime import datetime
import httplib
import pkg_resources
from geojson import Feature, FeatureCollection, dumps, loads as gloads
from simplejson import loads as sloads,dumps as sdumps
from geoalchemy import *
from PIL import Image

from crdppf.models import *
from crdppf.util.pdf_functions import getBBOX, getPrintFormat, getFeatureInfo
from crdppf.util.pdf_functions import getRestrictions, getMap, getAppendices
from crdppf.util.pdf_functions import getTOC, getTitlePage

from crdppf.util.pdf_classes import Objectify
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
    # to get vars defined in the buildout  use : request.registry.settings['key']
    crdppf_wms = request.registry.settings['crdppf_wms']
    sld_url = request.registry.settings['sld_url']

    # other basic parameters
    extract = Objectify()
    pdf_name = 'extract'
    pdf_name = 'crdppf_' + pdf_name
    pdfpath = pkg_resources.resource_filename('crdppf', 'static\public\pdf\\')
    extract.today = datetime.now()

    # PDF Margins
    leftopmargin = 25 # left margin
    rightopmargin = 25 # right margin
    topmargin = 55 # top margin for text
    headermargin = 50 # margin from header for the map placement
    
# *************************
# MAIN PROGRAM PART
#=========================

    # 1) If the ID of the parcel is set get the basic attributs 
    # else get the ID (idemai) of the selected parcel first using X/Y coordinates of the center 
    #----------------------------------------------------------------------------------------------------
    extract.featureInfo = getFeatureInfo(request) # '1_14127' # test parcel or '1_11340'
    featureInfo = extract.featureInfo
    
    # As we do not want to modify the fpdf.header() function from the FPDF library neither add an image on each page seperately 
    # this global var seems the simplest way to insert the logo of the community in the header of each page - maby not the most
    # elegant way but it definitly works

    commune = extract.featureInfo['nomcom']
    
    # AS does the german language, the french contains a few accents we have to replace to fetch the banner which has no accents in its pathname...
    conversion = [
        [u'â','a'],
        [u'ä','a'],
        [u'à','a'],
        [u'ô','o'],
        [u'ö','o'],
        [u'ò','o'],
        [u'û','u'],
        [u'ü','u'],
        [u'ù','u'],
        [u'î','i'],
        [u'ï','i'],
        [u'ì','i'],
        [u'ê','e'],
        [u'ë','e'],
        [u'è','e'],
        [u'é','e'],
        [u' (NE)','']
    ]

    for char in conversion:
        commune = commune.replace(char[0], char[1])

    # 2) Get the parameters for the paper format and the map based on the feature's geometry
    #---------------------------------------------------------------------------------------------------
    map_params = {'width':featureInfo['printFormat']['mapWidth'], 'height':featureInfo['printFormat']['mapHeight']}
    map_params['bboxCenterX'] = (featureInfo['BBOX']['maxX']+featureInfo['BBOX']['minX'])/2
    map_params['bboxCenterY'] = (featureInfo['BBOX']['maxY']+featureInfo['BBOX']['minY'])/2

    pdf_format = extract.featureInfo['printFormat']

    # 3) Get the list of all the restrictions
    #-------------------------------------------
    extract.topicList = DBSession.query(Topics).order_by(Topics.topicorder).all()

    # 4) Create the title page for the pdf extract
    #--------------------------------------------------
    pdf = getTitlePage(extract.featureInfo, crdppf_wms, sld_url, pdfpath, featureInfo['nomcom'], commune)

    # 5) Create an empty pdf for the table of content
    #--------------------------------------------------
    #pdf.add_page()
    toc = getTOC(commune)

    # 6) Create an empty pdf for the ?annexes?
    #-------------------------------------------------- 
    appendices = getAppendices(commune)

    # 7) Create the pages of the extract for each topic in the list
    #---------------------------------------------------
    # Thematic pages

    # Loop on each topic
    extract.restrictionList = []

    for crdppfTopic in extract.topicList:
        # if geographic layers are defined for the topic, get the information
        if crdppfTopic.layers :
            layers = []
            for layer in crdppfTopic.layers:
                layers.append(layer.layername)
            if isinstance(layers, list):
                for sublayer in layers:
                    params = {'id':featureInfo['idemai'], 'layerList':str(sublayer)}
                    features = get_features_function(params)
                    if features :
                        extract.restrictionList.append(features)
                        features = None
            else:
                params = {'id':featureInfo['idemai'], 'layerList':str(layers)}
                extract.restrictionList = get_features_function(params)

        else : 
            extract.restrictionList = []

        if len(extract.restrictionList) > 0 :

            # Parameter to set to 'true' if restrictions in the neighborhood are to be mentioned also
            neighborhood = False

           # PAGE X 
            pdf.add_page(str(pdf_format['orientation']+','+pdf_format['format']))
            pdf.set_margins(leftopmargin, topmargin, rightopmargin)

            # Thematic map/Carte thématique/Thematische Karte
            if crdppfTopic.layers:
                # Get the map and the legend
                crdppfTopic.mappath, crdppfTopic.legendpath = getMap(crdppfTopic.layers, crdppfTopic.topicid, crdppf_wms, map_params, pdf_format)

                # Place the map
                map = pdf.image(crdppfTopic.mappath, 65, headermargin, pdf_format['width'], pdf_format['height'])
                pdf.rect(65, headermargin, pdf_format['width'], pdf_format['height'], '')
                # Define the size of the legend container
                legendbox_width = 40
                legendbox_height = pdf_format['height'] 
                legendbox_proportion = float(legendbox_width-4) / float(legendbox_height-20)
                
                # draw the legend container
                pdf.rect(leftopmargin, headermargin, legendbox_width, legendbox_height, '')
                
                # define cells with border for the legend and the map
                pdf.set_xy(28, headermargin+3)
                pdf.set_font('Arial', 'B', 10)
                pdf.cell(50, 6, unicode('Légende', 'utf-8').encode('iso-8859-1'), 0, 1, 'L')
                y= pdf.get_y()
                pdf.set_font('Arial', '', 10)
                if  len(crdppfTopic.legendpath) > 0:
                    max_legend_width_px = 0
                    tot_legend_height_px = 0
                    sublegends = []

                    for graphic in crdppfTopic.legendpath:
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
                y = pdf.get_y()
                pdf.multi_cell(0, 6, 'Pas de carte.')
                pdf.ln()

            pdf.set_y(40)
            pdf.set_font('Arial', 'B', 16)
            pdf.multi_cell(0, 6, str(crdppfTopic.topicname.encode('iso-8859-1')), 0, 1, 'L')
            y = pdf.get_y()
            pdf.set_y(y+110)

            for features in extract.restrictionList:
                for feature in features:
                    if feature['properties'] :

                        # Check if property is affected by the restriction otherwise just mention restrictions in neighborhood
                        if feature['properties']['featureClass'] == 'intersects' or feature['properties']['featureClass'] == 'within' :

                            # Description of the interaction of a restriction with the property
                            #~ if feature['properties']['featureClass']:
                                #~ pdf.set_font('Arial','I',10)
                                #~ pdf.cell(100,6,unicode('Type d\'interaction : ','utf-8').encode('iso-8859-1') + feature['properties']['featureClass'].encode('iso-8859-1'),0,1,'L') 
 
                            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                            # !!! Hardcoding the returned attribute from our productive base for testing purposes !!! 
                            # !!! TO BE REPLACED BY THE TRANSFERT/EXTRACT MODEL MAPPING               !!!
                            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                            if feature['properties']['layerName'] == 'at14_zones_communales':
                                pdf.set_font('Arial', 'B', 10)
                                pdf.cell(55, 5, unicode('Caractéristique :','utf-8').encode('iso-8859-1'),0,0,'L')
                                pdf.set_font('Arial','',10)
                                pdf.multi_cell(0,5,feature['properties']['nom_communal'] .encode('iso-8859-1').strip(),0,1,'L')
                                
                            elif feature['properties']['layerName'] == 'en05_degres_sensibilite_bruit':
                                pdf.set_font('Arial','B',10)
                                pdf.cell(55,5,unicode('Teneur :','utf-8').encode('iso-8859-1'),0,0,'L')
                                pdf.set_font('Arial','',10)
                                pdf.cell(60,5,feature['properties']['type_ds'] .encode('iso-8859-1'),0,1,'L')
                           
                            elif feature['properties']['layerName'] == 'en01_zone_sect_protection_eaux':
                                pdf.set_font('Arial','B',10)
                                pdf.cell(55,5,unicode('Teneur :','utf-8').encode('iso-8859-1'),0,0,'L')
                                pdf.set_font('Arial','',10)
                                pdf.cell(60,5,feature['properties']['categorie'] .encode('iso-8859-1'),0,1,'L')
                                
                            elif feature['properties']['layerName'] == 'clo_couloirs':
                                pdf.set_font('Arial','B',10)
                                pdf.cell(55,5,unicode('Teneur :','utf-8').encode('iso-8859-1'),0,0,'L')
                                pdf.set_font('Arial','',10)
                                pdf.cell(60,5,feature['properties']['type'] .encode('iso-8859-1'),0,1,'L')
                                
                            elif feature['properties']['layerName'] == 'clo_cotes_altitude_surfaces':
                                pdf.set_font('Arial','B',10)
                                pdf.cell(55,5,unicode('Teneur :','utf-8').encode('iso-8859-1'),0,0,'L')
                                pdf.set_font('Arial','',10)
                                pdf.cell(60,5,str(feature['properties']['cote_alt_obstacles_minimum'] ).encode('iso-8859-1'),0,1,'L')
                                
                            elif feature['properties']['layerName'] in ['en07_canepo_accidents','en07_canepo_decharges_points','en07_canepo_decharges_polygones','en07_canepo_entreprises_points']:
                                pdf.set_font('Arial','B',10)
                                pdf.cell(55,5,unicode('Teneur :','utf-8').encode('iso-8859-1'),0,0,'L')
                                pdf.set_font('Arial','',10)
                                pdf.cell(60,5,str(feature['properties']['statut_osi'] ).encode('iso-8859-1'),0,1,'L')
                                
                            else: 
                                # Attributes of topic layers intersection
                                for key,value in feature['properties'].iteritems():
                                    if value is not None :
                                        if key !='layerName' and key != 'featureClass':
                                            pdf.set_font('Arial','B',10)
                                            pdf.cell(55,5,unicode('Teneur :','utf-8').encode('iso-8859-1'),0,0,'L')
                                            pdf.set_font('Arial','',10)
                                            if isinstance(value, float) or isinstance(value, int):
                                                value = str(value)
                                            pdf.cell(60,5,value.encode('iso-8859-1'),0,1,'L')
                # it has been decided that only restrictions that interact with the selected parcel are mentionned -  otherwise other interactions could be displayed
                        #~ elif feature['properties']['featureClass'] == 'adjacent':
                            #~ neighborhood = 'true'
                #~ if neighborhood == 'true':
                    #~ pdf.set_font('Arial','B',11)
                    #~ pdf.cell(100,6,unicode('Nom de la donnée : ','utf-8').encode('iso-8859-1') +feature['properties']['layerName'].encode('iso-8859-1'),0,1,'L') 
                    #~ pdf.set_font('Arial','I',10)
                    #~ pdf.cell(100,6,unicode('Remarque: Il y a des immeubles voisins affectés par cette restriction.','utf-8').encode('iso-8859-1'),0,1,'L') 
                
                #~ y = pdf.get_y()
                #~ pdf.set_y(y+5)
                
                # Legal Provisions/Dispositions juridiques/Gesetzliche Bestimmungen
                y = pdf.get_y()
                pdf.set_y(y+5)
                pdf.set_font('Arial', 'B', 10)
                pdf.cell(55, 6, unicode('Dispositions juridiques', 'utf-8').encode('iso-8859-1'), 0, 0, 'L')
                pdf.set_font('Arial', '', 10)
                if crdppfTopic.legalprovisions:
                    for provision in crdppfTopic.legalprovisions:
                        pdf.add_appendix('A', unicode(provision.officialtitle).encode('iso-8859-1'),unicode(provision.legalprovisionurl).encode('iso-8859-1'))
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
            pdf.set_font('Arial', 'B', 10)
            pdf.cell(55, 6, unicode('Informations et renvois suppl.', 'utf-8').encode('iso-8859-1'), 0, 0, 'L')
            pdf.set_font('Arial', '', 10)
            if crdppfTopic.references:
                for reference in crdppfTopic.references:
                    pdf.multi_cell(0,6,unicode(reference.officialtitle).encode('iso-8859-1'))
            else:
                    pdf.multi_cell(0,6,unicode('None','utf-8').encode('iso-8859-1')) 

            # Temporary provisions/Modifications en cours/Laufende Änderungen
            y = pdf.get_y()
            pdf.set_y(y+5)
            pdf.set_font('Arial','B',10)
            pdf.cell(55,6,unicode('Modifications en cours', 'utf-8').encode('iso-8859-1'),0,0,'L')
            pdf.set_font('Arial','',10)
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
            pdf.set_font('Arial','B',10)
            pdf.cell(55,3.9,unicode('Service compétent', 'utf-8').encode('iso-8859-1'),0,0,'L')
            pdf.set_font('Arial','',10)
            
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
            pdf.set_font('Arial','B',10)
            pdf.cell(55,6,unicode('Base(s) légale(s)', 'utf-8').encode('iso-8859-1'),0,0,'L')
            pdf.set_font('Arial','',10)
            if crdppfTopic.legalbases:
                for legalbase in crdppfTopic.legalbases:
                    pdf.multi_cell(0,6,str(crdppfTopic.legalbases).encode('iso-8859-1'))
            else:
                pdf.multi_cell(0,6,unicode('Legal base(s) placeholder','utf-8').encode('iso-8859-1'))
            
            #~ # TemporaryProvisions/Dispositions transitoires/Übergangsbestimmungen
            #~ y = pdf.get_y()
            #~ pdf.set_y(y+5)
            #~ pdf.set_font('Arial','B',10)
            #~ pdf.cell(47,6,unicode('Dispositions transitoires', 'utf-8').encode('iso-8859-1'),0,0,'L')
            #~ pdf.cell(3,6,unicode(': ', 'utf-8').encode('iso-8859-1'),0,0,'L')
            #~ pdf.set_font('Arial','',10)
            #~ pdf.multi_cell(0,3.9,unicode('Plan d\'affectation Quartier Nord du 21 décembre 1975\nValable jusqu\'au 31.12.2013','utf-8').encode('iso-8859-1'),0,1,'L')

        # Set the titles
        if crdppfTopic.layers :
            if extract.restrictionList :
                pdf.add_toc_entry(pdf.page_no(),str(crdppfTopic.topicname.encode('iso-8859-1')),1)
            else : 
                pdf.add_toc_entry('',str(crdppfTopic.topicname.encode('iso-8859-1')),0)
        else:
            pdf.add_toc_entry('',str(crdppfTopic.topicname.encode('iso-8859-1')),2)
    
    # Get the page count of all the chapters
    nb_pages_pdf =  len(pdf.pages)
    nb_pages_toc =  len(toc.pages)
    nb_pages_appendix =  len(appendices.pages)

    nb_pages_total = nb_pages_pdf + nb_pages_toc + nb_pages_appendix
    delta = nb_pages_toc + nb_pages_appendix

    # Add a new page with the table of content
    if pdf.toc_entries :
        pdf.add_page()
        pdf.set_margins(25,55,25)
        
        # List of all topics with a restriction for the selected parcel 
        for entry in pdf.toc_entries :
            if entry['categorie'] == 1 :
                toc.set_font('Arial','B',11)
                toc.cell(12,6,str(entry['no_page']),'B',0,'L')
                toc.cell(118,6,str(entry['title']),'LB',0,'L')
                toc.cell(15,6,str(''),'LB',0,'L')
                toc.cell(15,6,str(''),'LB',1,'L')
                
        toc.ln()
        toc.ln()
        toc.set_font('Arial','B',11)
        toc.multi_cell(0,5,unicode('Les restrictions suivantes ne touchent pas l\'immeuble : ', 'utf-8').encode('iso-8859-1'),'B',1,'L')
        toc.ln()
        
        for entry in pdf.toc_entries :
            if entry['categorie'] == 0 :
                toc.set_font('Arial','',11)
                toc.cell(118,6,str(entry['title']),'',0,'L')
                toc.cell(15,6,str(''),'',0,'L')
                toc.cell(15,6,str(''),'',1,'L')
                
        toc.ln()
        toc.set_font('Arial','B',11)
        toc.multi_cell(0,5,unicode('Les restrictions suivantes ne sont pas disponibles :', 'utf-8').encode('iso-8859-1'),'B',1,'L')
        toc.ln()
        
        for entry in pdf.toc_entries :
            if entry['categorie'] == 2 :
                toc.set_font('Arial','',11)
                toc.cell(118,6,str(entry['title']),0,0,'L')
                toc.cell(15,6,str(''),0,0,'L')
                toc.cell(15,6,str(''),0,1,'L')

        toc.ln()
        toc.set_font('Arial','B',11)
        toc.multi_cell(0,5,unicode('L\'information des restrictions suivantes n\'est pas contraignante :', 'utf-8').encode('iso-8859-1'),'B',1,'L')
        toc.ln()
        toc.set_font('Arial','',11)
        toc.cell(118,6,str('Aucune'),0,0,'L')
        toc.cell(15,6,str(''),0,0,'L')
        toc.cell(15,6,str(''),0,1,'L')
        #toc.cell(120,5,unicode('1 Les indications font référence à la position des annexes.', 'utf-8').encode('iso-8859-1'),0,1,'L')

    if pdf.appendix_entries :
        pdf.add_page()
        pdf.set_margins(25,55,25)
        index = 1
        for appendix in pdf.appendix_entries:
            appendices.set_font('Arial','B',11)
            appendices.cell(15,6,str('A'+str(index)),0,0,'L')
            appendices.cell(120,6,str(appendix['title']),0,1,'L')
            appendices.set_x(40)
            appendices.set_font('Arial','',9)
            appendices.set_text_color(0,0,255)
            appendices.multi_cell(0,6,str(appendix['url']))
            appendices.set_text_color(0,0,0)
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
    pdf.output(pdfpath+pdf_name+'.pdf','F')

    response = FileResponse(
        pdfpath + pdf_name + '.pdf',
        request,
        None,
        'application/pdf'
    )
    response. content_disposition='attachment; filename='+ pdf_name +'.pdf'
    return response
