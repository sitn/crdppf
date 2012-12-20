# -*- coding: UTF-8 -*-
from pyramid.response import FileResponse
from pyramid.renderers import render_to_response
from pyramid.httpexceptions import HTTPForbidden
from pyramid.view import view_config

from fpdf import FPDF
from datetime import datetime
import httplib
from owslib.wms import WebMapService

import pkg_resources
from geojson import Feature, FeatureCollection, dumps, loads as gloads
from simplejson import loads as sloads,dumps as sdumps

class ObjectCreator:
    def __init__(self, dictionary):
    
        for k, v in dictionary.items():
            setattr(self, k, v)
            
def round_to(n, precission):
    correction = 0.5 if n >= 0 else -0.5
    return int(n/precission+correction)*precission

def round_to_05(n):
    return round_to(n, 0.05)

@view_config(route_name='create_extrait')
def create_extrait(request):
    pdf_name = 'extrait'
    id_order = 1493
    today= datetime.now()
    mylist = {'company_name':'SITN','username':'Voisard','firstname':'François','street':'Tivoli 22','postalcode':'2003','city':'Neuchatel','country':'Suisse'}
    bbox = {'minY':203560,'minX':559150,'maxY':203960,'maxX':559750,'width':600,'height':400}
    #http://nesitn3.ne.ch/ogc-sitn-geoshop/wms?SERVICE=WMS&VERSION=1.1.1&REQUEST=GetMap&SRS=EPSG:21781&LAYERS=parcellaire_officiel&BBOX=559150,203560,559750,203960&WIDTH=600&HEIGHT=400&FORMAT=image/jpeg

    conn = httplib.HTTPConnection("wms.geo.admin.ch")
    filter1 = '/?lang=fr&QUERY_LAYERS=ch.bazl.projektierungszonen-flughafenanlagen&LAYERS=ch.bazl.projektierungszonen-flughafenanlagen&VERSION=1.1.1&SERVICE=WMS&REQUEST=GetFeatureInfo&SRS=EPSG%3A21781&INFO_FORMAT=text/plain&BBOX=680153.65034247,256316,684977.65034247,257741&WIDTH=2412&HEIGHT=712&X=1206&Y=355'
    conn.request("GET",filter1)
    r1 = conn.getresponse()
    query = r1.read()

    # Create order PDF
    pdf=FPDF(format='A4')
    pdf.add_page()
    pdf.set_margins(20,25,25)
    path = pkg_resources.resource_filename('crdppf','utils\\')
    pdf.image(path+"ne.ch_RVB.png",11,10,55,17)
    pdf.set_y(33)
    pdf.set_font('Arial','B',8)
    
    pdf.multi_cell(0,3.9,unicode('DEPARTEMENT DE LA GESTION\nDU TERRITOIRE', 'utf-8').encode('iso-8859-1'))
    pdf.set_font('Arial','',8)
    pdf.multi_cell(0,3.9,unicode('SERVICE DE LA GÉOMATIQUE ET\nDU REGISTRE FONCIER', 'utf-8').encode('iso-8859-1'))

    pdf.ln()
    pdf.set_font('Arial','B',16)
    pdf.multi_cell(0,6,unicode('Extrait [officiel] du cadastre des restrictions de droit public à la propriété foncière', 'utf-8').encode('iso-8859-1'))
    pdf.ln()
    pdf.ln()
    pdf.set_font('Arial','B',10)
    pdf.multi_cell(0,3.9,unicode('Bien-fonds n° ', 'utf-8').encode('iso-8859-1'))
    pdf.multi_cell(0,3.9,unicode('Cadastre', 'utf-8').encode('iso-8859-1'))
    pdf.ln()

    # Create order sld
    sld = u"""<?xml version="1.0" encoding="UTF-8"?>
<sld:StyledLayerDescriptor version="1.0.0" xmlns="http://www.opengis.net/ogc" xmlns:sld="http://www.opengis.net/sld" xmlns:ogc="http://www.opengis.net/ogc" xmlns:gml="http://www.opengis.net/gml" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.opengis.net/sld http://schemas.opengis.net/sld/1.0.0/StyledLayerDescriptor.xsd">
<sld:NamedLayer>
<sld:Name>geoshop_orders</sld:Name>
<sld:UserStyle>
<sld:Name>propertyIsEqualTo</sld:Name>
<sld:Title>propertyIsEqualTo</sld:Title>
<sld:FeatureTypeStyle>
<sld:Rule>	
<ogc:Filter>
<ogc:PropertyIsEqualTo>
<ogc:PropertyName>id_order</ogc:PropertyName>
<ogc:Literal>"""
    sld += str(id_order)
    sld += u"""</ogc:Literal>
</ogc:PropertyIsEqualTo>
</ogc:Filter>					
<sld:PolygonSymbolizer>
<sld:Fill>
<sld:CssParameter name="fill">#ff0000</sld:CssParameter>
<sld:CssParameter name="fill-opacity">0.5</sld:CssParameter>
</sld:Fill>
<sld:Stroke>
<sld:CssParameter name="stroke">#ff0000</sld:CssParameter>
<sld:CssParameter name="stroke-opacity">1</sld:CssParameter>
<sld:CssParameter name="stroke-width">1</sld:CssParameter>
</sld:Stroke>
</sld:PolygonSymbolizer>
<sld:TextSymbolizer>
<sld:Label>
<ogc:PropertyName>mandat_title</ogc:PropertyName>							
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
    sldfile = open(sldpath+pdf_name+'.xml', 'w')
    sldfile.write(sld)
    sldfile.close()

    layers= [    
        'mnt25_situation_gris',
        'lacs_gris',
        'communes',
        'districts',
        'reseau_hydro_gris',
        'reseau_routier_gris',
        'couverture_du_sol_v25_gris',
        'cantons',
        'routes_v25_2',
        'routes_v25_1_gris',
        'batiments_v25_gris',
        'plan_ensemble_10000_gris',
        'plan_ensemble_5000_gris',
        'nomenclature_reseau_hydro_1',
        'nomenclature_reseau_hydro_2',
        'nomenclature_cantons',
        'nomenclature_communes',
        'nomenclature_villes',
        'nomenclature_lacs',
        'surfaces_tot',
        'surfaces_bois',
        'surfaces_vignes2',
        'batiments_provisoires',
        'batiments',
        'batiments_projet',
        'parcellaire_agricole',
        'parcellaire_officiel',
        'immeubles_txt_rappel',
        'immeubles_txt',
        'pts_limites',
        'obj_divers_couvert',
        'obj_divers_cordbois',
        'obj_divers_piscine',
        'obj_divers_lineaire',
        'pts_fixes',
        'lieux_dits_prov',
        'noms_locaux_canton',
        'point_adresse',
        'voie_adresse'
    ]
    
    wms = WebMapService('http://nesitn3.ne.ch/ogc-sitn-geoshop/wms', version='1.1.1')
    img = wms.getmap(   
        layers=layers,
        sld = request.static_url('crdppf:static/public/pdf')+'/sld'+ pdf_name+'.xml',
        srs='EPSG:21781',
        bbox=(bbox['minX'], bbox['minY'], bbox['maxX'], bbox['maxY']),
        size=(bbox['width'], bbox['height']),
        format='image/png',
        transparent=False
    )

    out = open(sldpath+pdf_name+'.png', 'wb')
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
    wms2 = WebMapService('http://sitn.ne.ch/ogc-sitn-poi/wms', version='1.1.1')
    img2 = wms2.getmap(   
        layers=layers2,
        srs='EPSG:21781',
        bbox=(bbox['minX'], bbox['minY'], bbox['maxX'], bbox['maxY']),
        size=(bbox['width'], bbox['height']),
        #bbox=(640000, 200000,750000,280000),
        #size=(800,582),
        format='image/jpeg',
        transparent=False
    )

    out2 = open(sldpath+ pdf_name+'2.jpg', 'wb')
    out2.write(img2.read())
    out2.close()

    pdf.set_y(260);
    pdf.set_font('Arial','',7);
    pdf.cell(0,10,'RUE DE TIVOLI 22, CH-2003 NEUCHATEL 3   TEL. 032 889 67 50   FAX 032 889 61 21   SGRF@NE.CH  WWW.NE.CH/SGRF',0,0,'C');

    # PAGE 2 
    pdf.add_page()
    pdf.set_y(25)
    pdf.set_font('Arial','B',16)
    pdf.multi_cell(0,6,'73 - Plan d\'affectation')
    pdf.image(sldpath+pdf_name+'.png',20,35,90,70)
    pdf.set_y(120)
    pdf.set_font('Arial','',10)
    pdf.multi_cell(0,3.9,query)
    pdf.ln()
    
    # PAGE 3
    pdf.add_page()
    pdf.set_font('Arial','B',16)
    pdf.multi_cell(0,6,unicode('116 Cadastre des sites pollués','utf-8').encode('iso-8859-1'))
    pdf.image(sldpath+pdf_name+'2.jpg',20,35,90,70)
    pdf.ln()
    
    # PAGE 4
    pdf.add_page()
    pdf.set_font('Arial','B',16)
    pdf.multi_cell(0,6,unicode('131 Zones de protection des eaux souterraines','utf-8').encode('iso-8859-1'))
    #pdf.image(pdf_name+'2.png',20,35,90,70)
    pdf.ln()
    
    # Creates the pdf file
    pdf_name='crdppf_'+pdf_name
    pdfpath = pkg_resources.resource_filename('crdppf','static\public\pdf\\')
    pdf.output(pdfpath+pdf_name+'.pdf','F')
    
    response = FileResponse(
        pdfpath + pdf_name + '.pdf',
        request,
        None,
        'application/pdf'
    )
    response. content_disposition='attachment; filename='+ pdf_name +'.pdf'
    return response