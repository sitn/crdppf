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
        
        
def plans_wms(restriction_layers,crdppf_wms,bbox):
 
    # Creates the pdf file
    pdf_name = 'extrait'
    pdf_name='crdppf_'+pdf_name
    pdfpath = pkg_resources.resource_filename('crdppf','static\public\pdf\\')
    
    layers= [    
        'etat_mo',
        'la3_limites_communales',
        'mo22_batiments'
    ]
    
    i = 0
    wms = WebMapService(crdppf_wms, version='1.1.1')
    
    for layer in restriction_layers:
        img = wms.getmap(   
            layers=layers,
            srs='EPSG:21781',
            bbox=(bbox['minX'], bbox['minY'], bbox['maxX'], bbox['maxY']),
            size=(bbox['width'], bbox['height']),
            format='image/png',
            transparent=False
        )
        
        out = open(pdfpath+pdf_name+str(i)+'.png', 'wb')
        out.write(img.read())
        out.close()
        
    return i
    
class ExtraitPDF(FPDF):

    def header(self):

        path = pkg_resources.resource_filename('crdppf','utils\\')
        
        no_page = self.page_no()

        if no_page == 1:
            self.image(path+"Canepo2.jpg",0,0,210,30)
            self.set_y(45)
            self.set_x(149)
            self.image(path+"06ne_ch_RVB.jpg",150,30,43.4,13.8)
            self.set_font('Arial','B',8)
            self.multi_cell(0,3.9,unicode('DEPARTEMENT DE LA GESTION\nDU TERRITOIRE', 'utf-8').encode('iso-8859-1'))
            self.set_font('Arial','',8)
            self.set_x(149)
            self.multi_cell(0,3.9,unicode('SERVICE DE LA GÉOMATIQUE ET\nDU REGISTRE FONCIER', 'utf-8').encode('iso-8859-1'))
            
    def footer(self):
        # position footer at 15mm from the bottom
        self.set_y(-20)
        self.set_font('Arial','',7);
        self.cell(0,10,'RUE DE TIVOLI 22, CH-2003 NEUCHATEL 3   TEL. 032 889 67 50   FAX 032 889 61 21   SGRF@NE.CH  WWW.NE.CH/SGRF',0,0,'C');



@view_config(route_name='create_extrait')
def create_extrait(request):
    # to get vars defined in the buildout  use : request.registry.settings['key']
    crdppf_wms = request.registry.settings['crdppf_wms']
    sld_url = request.registry.settings['sld_url']
    restriction_layers = ['affectation','canepo','foret']
    bbox = {'minY':203560,'minX':559150,'maxY':203960,'maxX':559750,'width':600,'height':400}


    i = plans_wms(restriction_layers,crdppf_wms,bbox)
    
    
    # Creates the pdf file
    pdf_name = 'extrait'
    pdf_name='crdppf_'+pdf_name
    pdfpath = pkg_resources.resource_filename('crdppf','static\public\pdf\\')
    
    today= datetime.now()
    mylist = {'company_name':'SITN','username':'Voisard','firstname':'François','street':'Tivoli 22','postalcode':'2003','city':'Neuchatel','country':'Suisse'}
  
    #~ conn = httplib.HTTPConnection("wms.geo.admin.ch")
    #~ filter1 = '/?lang=fr&QUERY_LAYERS=ch.bazl.projektierungszonen-flughafenanlagen&LAYERS=ch.bazl.projektierungszonen-flughafenanlagen&VERSION=1.1.1&SERVICE=WMS&REQUEST=GetFeatureInfo&SRS=EPSG%3A21781&INFO_FORMAT=text/plain&BBOX=680153.65034247,256316,684977.65034247,257741&WIDTH=2412&HEIGHT=712&X=1206&Y=355'
    #~ conn.request("GET",filter1)
    #~ r1 = conn.getresponse()
    #~ query = r1.read()

    # Create order PDF
    pdf = ExtraitPDF()
    #pdf=FPDF(format='A4')
    pdf.add_page()
    pdf.set_margins(25,25,25)
    path = pkg_resources.resource_filename('crdppf','utils\\')


    pdf.set_y(70)
    pdf.set_font('Arial','B',28)
    pdf.multi_cell(0,12,unicode('Extrait [officiel]', 'utf-8').encode('iso-8859-1'))
    pdf.set_font('Arial','B',22)
    pdf.multi_cell(0,12,unicode('du cadastre des restrictions de\ndroit public à la propriété foncière', 'utf-8').encode('iso-8859-1'))
    pdf.ln()
    pdf.ln()
    pdf.set_font('Arial','B',12)
    pdf.cell(37,5,unicode("Bien-fonds n°", 'utf-8').encode('iso-8859-1'),0,0,'L')
    pdf.cell(3,5,unicode(": ", 'utf-8').encode('iso-8859-1'),0,0,'L')
    pdf.cell(50,5,unicode("14127", 'utf-8').encode('iso-8859-1'),0,0,'L')
    pdf.cell(37,5,unicode("N° EGRID", 'utf-8').encode('iso-8859-1'),0,0,'L')
    pdf.cell(3,5,unicode(": ", 'utf-8').encode('iso-8859-1'),0,0,'L')
    pdf.cell(50,5,unicode("xxxxx", 'utf-8').encode('iso-8859-1'),0,1,'L')
    
    pdf.cell(37,5,unicode("Cadastre", 'utf-8').encode('iso-8859-1'),0,0,'L')
    pdf.cell(3,5,unicode(": ", 'utf-8').encode('iso-8859-1'),0,0,'L')
    pdf.cell(50,5,unicode("Neuchâtel", 'utf-8').encode('iso-8859-1'),0,1,'L')
    
    pdf.cell(37,5,unicode('Commune', 'utf-8').encode('iso-8859-1'),0,0,'L')
    pdf.cell(3,5,unicode(": ", 'utf-8').encode('iso-8859-1'),0,0,'L')
    pdf.cell(50,5,unicode('Neuchâtel', 'utf-8').encode('iso-8859-1'),0,0,'L')
    pdf.cell(37,5,unicode('N° OFS', 'utf-8').encode('iso-8859-1'),0,0,'L')
    pdf.cell(3,5,unicode(": ", 'utf-8').encode('iso-8859-1'),0,0,'L')
    pdf.cell(50,5,unicode("6458", 'utf-8').encode('iso-8859-1'),0,1,'L')

    pdf.set_y(165)
    pdf.set_font('Arial','B',10)
    pdf.cell(65,5,unicode('Extrait établi le', 'utf-8').encode('iso-8859-1'),0,0,'L')
    pdf.cell(40,5,unicode(': 31.01.2013', 'utf-8').encode('iso-8859-1'),0,1,'L')
    pdf.cell(65,5,unicode('Dernière mise à jour des données', 'utf-8').encode('iso-8859-1'),0,0,'L')
    pdf.cell(40,5,unicode(': 30.01.2013', 'utf-8').encode('iso-8859-1'),0,1,'L')
    pdf.cell(65,5,unicode('Editeur de l\'extrait', 'utf-8').encode('iso-8859-1'),0,0,'L')
    pdf.cell(40,5,unicode(': FV-SITN', 'utf-8').encode('iso-8859-1'),0,1,'L')

    pdf.set_y(190)
    pdf.cell(65,5,unicode('Etat des données de la MO', 'utf-8').encode('iso-8859-1'),0,0,'L')
    pdf.cell(40,5,unicode(':', 'utf-8').encode('iso-8859-1'),0,1,'L')
    pdf.cell(65,5,unicode('Cadre de référence', 'utf-8').encode('iso-8859-1'),0,0,'L')
    pdf.cell(40,5,unicode(': MN03', 'utf-8').encode('iso-8859-1'),0,1,'L')


    pdf.image(path+"Neuchatel.jpg",180,180,20,22)


    pdf.set_y(215)
    pdf.set_font('Arial','',10)
    pdf.cell(0,5,unicode('Signature', 'utf-8').encode('iso-8859-1'),0,0,'L')

    pdf.set_y(240)
    pdf.set_font('Arial','B',10)
    pdf.cell(0,5,unicode('Indications générales', 'utf-8').encode('iso-8859-1'),0,1,'J')
    pdf.set_font('Arial','',10)
    pdf.multi_cell(0,5,unicode('Mise en garde : Le canton de Neuchâtel n\'engage pas sa responsabilité sur l\'exactitude ou la fiabilité des documents législatifs dans leur version électronique. Ces documents ne créent aucun autre droit ou obligation que ceux qui découlent des textes légalement adoptés et publiés, qui font seuls foi.', 'utf-8').encode('iso-8859-1'),0,1,'L')


    layers= [    
        'la3_limites_communales',
        'at14_zones_communales',
        'at08_zones_cantonales',
        'mo22_batiments',
        'mo21_batiments_provisoires',
        'mo9_immeubles',
        'ag1_parcellaire_provisoire'
    ]

    wms = WebMapService(crdppf_wms, version='1.1.1')
    img = wms.getmap(   
        layers=layers,
        srs='EPSG:21781',
        bbox=(bbox['minX'], bbox['minY'], bbox['maxX'], bbox['maxY']),
        size=(bbox['width'], bbox['height']),
        format='image/jpeg',
        transparent=False
    )

    out = open(pdfpath+pdf_name+'.jpg', 'wb')
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
    wms2 = WebMapService(crdppf_wms, version='1.1.1')
    img2 = wms2.getmap(   
        layers=layers2,
        srs='EPSG:21781',
        bbox=(bbox['minX'], bbox['minY'], bbox['maxX'], bbox['maxY']),
        size=(bbox['width'], bbox['height']),
        #bbox=(640000, 200000,750000,280000),
        #size=(800,582),
        format='image/png',
        transparent=False
    )

    out2 = open(pdfpath+ pdf_name+'2.png', 'wb')
    out2.write(img2.read())
    out2.close()

    #~ layers3= [
        #~ 'ch.bazl.segelflugkarte',
        #~ 'ch.bazl.projektierungszonen-flughafenanlage'
    #~ ]
    
    #~ #http://sitn.ne.ch/ogc-sitn-poi/wms?SERVICE=WMS&VERSION=1.1.1&REQUEST=GetMap&SRS=EPSG:21781&LAYERS=en07_canepo_accidents,en07_canepo_entreprises,en07_canepo_decharges&BBOX=559150,203560,559750,203960&WIDTH=600&HEIGHT=400&FORMAT=image/png
    #~ wms3 = WebMapService('http://wms.geo.admin.ch/', version='1.1.1')
    #~ img3 = wms3.getmap(   
        #~ layers=layers3,
        #~ srs='EPSG:21781',
        #~ bbox=(640000, 200000,750000,280000),
        #~ size=(800,582),
        #~ format='image/png',
        #~ transparent=False
    #~ )

    #~ out3 = open(pdfpath+ pdf_name+'3.png', 'wb')
    #~ out3.write(img3.read())
    #~ out3.close()
    
    # PAGE 2 
    pdf.add_page()
    pdf.set_y(25)
    pdf.set_font('Arial','B',16)
    pdf.multi_cell(0,6,'73 - Plan d\'affectation')
    
    # Attributes of topic layers intersection
    pdf.set_y(35)
    pdf.set_font('Arial','B',10)
    pdf.cell(50,6,unicode('Nom de la zone', 'utf-8').encode('iso-8859-1'),0,0,'L')
    pdf.set_font('Arial','',10)
    pdf.multi_cell(0,3.9,unicode(':  Zone d\'habitation / secteur d\'ordre non-contigu 1.2','utf-8').encode('iso-8859-1'),0,1,'L')
    pdf.set_font('Arial','B',10)
    pdf.cell(50,6,unicode('Surface', 'utf-8').encode('iso-8859-1'),0,0,'L')
    pdf.set_font('Arial','',10)
    pdf.multi_cell(0,6,unicode(':  712 m2','utf-8').encode('iso-8859-1'),0,1,'L')
    
    pdf.set_draw_color(200,200,200)
    pdf.set_line_width(0.4)
    y = pdf.get_y()
    pdf.line(25,y+1,185,y+1)
    
    # Legal Provisions
    pdf.set_y(y+5)
    pdf.set_font('Arial','B',10)
    pdf.cell(50,6,unicode('Dispositions juridiques', 'utf-8').encode('iso-8859-1'),0,0,'L')
    pdf.set_font('Arial','',10)
    pdf.multi_cell(0,6,unicode(':  Le règlement de construction est donné à l\'annexe 1','utf-8').encode('iso-8859-1'),0,1,'L')


    pdf.set_draw_color(200,200,200)
    pdf.set_line_width(0.4)
    y = pdf.get_y()
    pdf.line(25,y+1,185,y+1)

    # Assent date
    pdf.set_y(y+5)
    pdf.set_font('Arial','B',10)
    pdf.cell(47,6,unicode('Sanction par le Conseil d\'Etat', 'utf-8').encode('iso-8859-1'),0,0,'L')
    pdf.cell(3,6,unicode(':', 'utf-8').encode('iso-8859-1'),0,0,'L')
    pdf.set_font('Arial','',10)
    pdf.cell(3,6,unicode('5 juillet 1999 et 13 juin 2001', 'utf-8').encode('iso-8859-1'),0,1,'L')

    pdf.set_draw_color(200,200,200)
    y = pdf.get_y()
    pdf.line(25,y+1,185,y+1)

    # Complementary provisions and information
    pdf.set_y(y+5)
    pdf.set_font('Arial','B',10)
    pdf.cell(0,6,unicode('Infos et renvois supplémentaires', 'utf-8').encode('iso-8859-1'),0,1,'L')
    pdf.set_font('Arial','',10)
    pdf.set_x(35)
    pdf.multi_cell(0,6,unicode('-  Plan spécial \"Gare Nord\"\n-  Plan de quartier \"Les Fahys\"','utf-8').encode('iso-8859-1'),0,1,'L')

    pdf.set_draw_color(200,200,200)
    y = pdf.get_y()
    pdf.line(25,y+1,185,y+1)

    # Competent Authority
    y = pdf.get_y()
    pdf.set_y(y+5)
    pdf.set_font('Arial','B',10)
    pdf.cell(47,3.9,unicode('Service compétent', 'utf-8').encode('iso-8859-1'),0,0,'L')
    pdf.cell(3,3.9,unicode(': ', 'utf-8').encode('iso-8859-1'),0,0,'L')
    pdf.set_font('Arial','',10)
    pdf.multi_cell(120,3.9,unicode('Commune de Neuchâtel\nENVIRONNEMENT - Service de l\'aménagement urbain\nFbg du Lac 3\n2000 Neuchâtel\nTél: 032 717\'76\'61\nE-Mail: urbanisme.neuchatel@ne.ch', 'utf-8').encode('iso-8859-1'),0,1,'L')
    pdf.set_font('Arial','B',10)
    pdf.cell(47,6,unicode('Personne de contact', 'utf-8').encode('iso-8859-1'),0,0,'L')
    pdf.cell(3,6,unicode(': ', 'utf-8').encode('iso-8859-1'),0,0,'L')
    pdf.set_font('Arial','',10)
    pdf.cell(120,6,unicode('Fabien Coquillat', 'utf-8').encode('iso-8859-1'),0,1,'L')
    
    pdf.set_draw_color(200,200,200)
    y = pdf.get_y()
    pdf.line(25,y+1,185,y+1)

    # Legal bases
    pdf.set_y(y+5)
    pdf.set_font('Arial','B',10)
    pdf.cell(47,6,unicode('Base(s) légale(s)', 'utf-8').encode('iso-8859-1'),0,0,'L')
    pdf.cell(3,6,unicode(': ', 'utf-8').encode('iso-8859-1'),0,0,'L')
    pdf.set_font('Arial','',10)
    pdf.multi_cell(0,3.9,unicode('RS 700 Loi fédérale sur l\'aménagement du territoire (art. 14, 26)\nRSN 701.0 Loi cantonale sur l\'aménagement du territoire (art. 43 al. 2 lit a, 45-64a)','utf-8').encode('iso-8859-1'),0,1,'L')
    
    pdf.set_draw_color(200,200,200)
    pdf.set_line_width(0.4)
    y = pdf.get_y()
    pdf.line(25,y+1,185,y+1)

    pdf.image(pdfpath+pdf_name+'.jpg',25,y+5,90,70)

    pdf.set_y(y+80)
    y = pdf.get_y()
    pdf.line(25,y+1,185,y+1)

    pdf.set_y(y+5)
    pdf.set_font('Arial','B',10)
    pdf.cell(47,6,unicode('Dispositions transitoires', 'utf-8').encode('iso-8859-1'),0,0,'L')
    pdf.cell(3,6,unicode(': ', 'utf-8').encode('iso-8859-1'),0,0,'L')
    pdf.set_font('Arial','',10)
    pdf.multi_cell(0,3.9,unicode('Plan d\'affectation Quartier Nord du 21 décembre 1975\nValable jusqu\'au 31.12.2013','utf-8').encode('iso-8859-1'),0,1,'L')
    
    
    # PAGE 3
    pdf.add_page()
    pdf.set_font('Arial','B',16)
    pdf.multi_cell(0,6,unicode('116 Cadastre des sites pollués','utf-8').encode('iso-8859-1'))
    pdf.image(pdfpath+pdf_name+'2.png',20,35,90,70)
    pdf.ln()
    
    # PAGE 4
    pdf.add_page()
    pdf.set_font('Arial','B',16)
    pdf.multi_cell(0,6,unicode('131 Zones de protection des eaux souterraines','utf-8').encode('iso-8859-1'))
    #pdf.image(pdf_name+'2.png',20,35,90,70)
    pdf.ln()
    
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