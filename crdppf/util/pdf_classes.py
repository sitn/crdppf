# -*- coding: UTF-8 -*-

from fpdf import FPDF
import pkg_resources
from datetime import datetime
from owslib.wms import WebMapService
import urllib
from PIL import Image

from crdppf.models import *
from crdppf.views.get_features import get_features, get_features_function

class Restriction:
    """Representation of a restriction in the transfert model structure."""
    tenor = ''
    theme = ''
    typecode = 0
    typecodelist = []
    legalstate = ''
    publicationdate = ''

    def __init__(self, **kwds):
        self.__dict__.update(kwds)

class AppConfig:
    """Class holding the definition of the basic parameters
       To put in a table
    """
    # tempdir : Path to the working directory where the temporary files will be stored
    tempdir = pkg_resources.resource_filename('crdppf', 'static/public/temp_files/') 
    # pdfbasedir : Path to the directory where the generated pdf's will be stored
    pdfbasedir = pkg_resources.resource_filename('crdppf', 'static/public/pdf/') 
    # imagesbasedir : Path to the directory where the images resources are stored
    imagesbasedir = pkg_resources.resource_filename('crdppf','static\images\\')
    # municipalitylogodir : Path to the directory where the logos of the municipalities are stored
    municipalitylogodir = pkg_resources.resource_filename('crdppf','static/images/ecussons/')
    # legaldocsdir : Path to the folder where the legal documents are stored that may or may not be included
    legaldocsdir = pkg_resources.resource_filename('crdppf', 'static/public/reglements/') 
    # CHlogopath : Path to the header logo of the Swiss Confederation
    CHlogopath = 'ecussons\\Logo_Schweiz_Eidgen.png'
    # cantonlogopath : Path to the header logo of the canton
    cantonlogopath = 'ecussons\\06ne_ch_RVB.jpg'
    
    # defaultlanguage : Default language used for the userinterface and the report
    lang = 'fr'
    # defaultfont : Default font used for the extract printout
    defaultfontfamily = 'Arial'
    # defaultfitratio : Default ratio feature bboxsides to mapsides length

    appconfig = DBSession.query(AppConfig).order_by(AppConfig.idparam.asc()).all()

class PDFConfig:
    """A class to define the configuration of the PDF extract to simplify changes.
    """
  
    # PDF Configuration
    defaultlanguage = 'fr'
    pdfformat = 'A4'
    pdforientation = 'portrait'
    leftmargin = 25 # left margin
    rightmargin = 25 # right margin
    topmargin = 55 # top margin for text
    headermargin = 50 # margin from header for the map placement
    footermargin = 20
    pdfmargins = [leftmargin, topmargin, rightmargin]

    fontfamily = 'Arial'
    textstyles = {
        'title1':[fontfamily, 'B', 22],
        'title2':[fontfamily, 'B', 18],
        'title3':[fontfamily, 'B', 16],
        'normal':[fontfamily, '', 10],
        'bold':[fontfamily,'B',10],
        'small':[fontfamily, '', 7],
        'tocbold':[fontfamily, 'B', 11],
        'tocurl':[fontfamily, '', 9],
        'tocnormal':[fontfamily, '', 11]
        }
    urlcolor = [0, 0, 255]
    defaultcolor = [0, 0, 0]

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    pdfname = str(timestamp) + '_ExtraitCRDPPF'
    siteplanname = str(timestamp) + '_siteplan'
    fitratio = 0.9
    pdfpath = pkg_resources.resource_filename('crdppf', 'static/public/pdf/')


class Extract(FPDF):
    """The main class for the ectract object which collects all the data, then writes the pdf report."""
    # HINTS #
    # to get vars defined in the buildout  use : request.registry.settings['key']
    
    def __init__(self, request):
        FPDF.__init__(self)
        self.request = request
        self.crdppf_wms = request.registry.settings['crdppf_wms']
        self.sld_url = request.static_url('crdppf:static/public/temp_files/')
        self.creationdate = datetime.now().strftime("%d.%m.%Y-%H:%M:%S")
        self.timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        self.printformat = {}
        self.topicdata = {}
        self.filename = 'thefilename'
        self.topiclist = {}
        self.layerlist = {}
        self.legalbaselist = {}
        self.legalprovisionslist = {}
        self.referenceslist = {}
        self.toc_entries = {}
        self.appendix_entries = []
        self.reference_entries = []

    def alias_no_page(self, alias='{no_pg}'):
        """Define an alias for total number of pages"""
        self.str_alias_no_page = alias
        return alias
        
    def load_app_config(self):
        """Initialises the basic parameters of the application.
        """
        self.appconfig = AppConfig()


    def set_pdf_config(self):
        """Loads the initial configuration of the PDF page.
        """
        self.pdfconfig = PDFConfig()

    def set_filename(self):
        self.filename = str(self.timestamp) + self.featureid

    def header(self):
        """Creates the document header with the logos and vertical lines."""

        # Add the vertical lines
        self.set_line_width(0.3)
        self.line(105, 0, 105, 35)
        self.line(165, 0, 165, 35)
        # Add the logos if existing else put a placeholder
        self.image(self.appconfig.imagesbasedir + self.appconfig.CHlogopath, 10, 8, 55, 14.42)
        self.image(self.appconfig.imagesbasedir + self.appconfig.cantonlogopath, 110, 8, 43.4, 13.8)
        try:
            self.image(self.municipalitylogopath, 170, 8, 10, 10.7)
        except:
            self.image(self.appconfig.imagesbasedir + 'ecussons\Placeholder.jpg', 170, 8, 10, 10.7)
        # This lines are not necessary if the community name is already contained in the 
        self.set_xy(170, 19.5)
        self.set_font(*self.pdfconfig.textstyles['small'])
        self.cell(30, 3, self.municipality.encode('iso-8859-1'), 0, 0, 'L')

    def footer(self):
        """Creates the document footer"""

        # position footer at 15mm from the bottom
        self.set_y(-20)
        self.set_font(*self.pdfconfig.textstyles['small'])
        self.cell(55, 5, self.translations['creationdatelabel'] + str(' ')+self.creationdate, 0, 0, 'L')
        self.cell(60, 5, self.translations['signaturelabel'] + str(' ')+self.timestamp, 0, 0, 'C')
        self.cell(55, 5, self.translations['pagelabel'] + str(self.alias_no_page())+str('/')+ \
            str(self.alias_nb_pages()), 0, 0, 'R')

    def get_title_page(self):
        """Creates the title page of the PDF extract with the abstract and a situation map of the property.
        """
        today= datetime.now()
            
        # START TITLEPAGE
        self.add_page()
        self.set_margins(*self.pdfconfig.pdfmargins)

        # following 3 lines to replace - used for convenience only
        translations = self.translations
        pdfconfig = self.pdfconfig
        feature_info = self.featureInfo
        # PageTitle
        self.set_y(45)
        self.set_font(*self.pdfconfig.textstyles['title1'])
        if self.reportInfo['type'] =='certified':
            self.multi_cell(0, 9, self.translations["certifiedextracttitlelabel"])
        elif self.reportInfo['type'] =='reduced':
            self.multi_cell(0, 9, self.translations['reducedextracttitlelabel'])
        elif self.reportInfo['type'] =='reducedcertified':
            self.multi_cell(0, 9, self.translations['reducedcertifiedextracttitlelabel'])
        else:
            self.multi_cell(0, 9, self.translations['normalextracttitlelabel'])
        self.set_font(*self.pdfconfig.textstyles['title2'])
        #self.multi_cell(0, 7, translations['extractsubtitlelabel'])
        self.multi_cell(0, 7, self.translations['extractsubtitlelabel'])
        self.ln()
        
        map = self.image(self.sitemappath, 25, 80, 160, 90)

        y=self.get_y()
        self.rect(25, 80, 160, 90, '')
        self.set_y(y+105)
        # First infoline
        self.set_font(*self.pdfconfig.textstyles['bold'])
        self.cell(45, 5, self.translations['propertylabel'], 0, 0, 'L')

        self.set_font(*self.pdfconfig.textstyles['normal'])
        if feature_info['nomcad'] is not None:
            self.cell(50, 5, feature_info['nummai'].encode('iso-8859-1')+str(' (')+feature_info['nomcad'].encode('iso-8859-1')+str(') ')+str(' - ')+feature_info['type'].encode('iso-8859-1'), 0, 1, 'L')
        else : 
            self.cell(50, 5, feature_info['nummai'].encode('iso-8859-1'), 0, 1, 'L')
        
         # Second infoline : Area and EGRID
        self.set_font(*pdfconfig.textstyles['bold'])
        self.cell(45, 5, translations['propertyarealabel'], 0, 0, 'L')
        self.set_font(*pdfconfig.textstyles['normal'])
        self.cell(50, 5, str(feature_info['area'])+str(' m2').encode('iso-8859-1'), 0, 0, 'L')
        self.set_font(*pdfconfig.textstyles['bold'])
        self.cell(35, 5, translations['EGRIDlabel'], 0, 0, 'L')
        self.set_font(*pdfconfig.textstyles['normal'])
        self.cell(50, 5, feature_info['no_EGRID'].encode('iso-8859-1'), 0, 1, 'L')

        # Third infoline : Adresse/localisation
        self.set_font(*pdfconfig.textstyles['bold'])
        self.cell(45, 5, translations['addresslabel'], 0, 0, 'L')
        self.set_font(*pdfconfig.textstyles['normal'])
        self.cell(50, 5, str('Placeholder').encode('iso-8859-1'), 0, 1, 'L')

         # Fourth infoline : municipality and BFS number
        self.set_font(*pdfconfig.textstyles['bold'])
        self.cell(45, 5,  translations['municipalitylabel']+str(' (')+translations['federalmunicipalitynumberlabel']+str(')'), 0, 0, 'L')
        self.set_font(*pdfconfig.textstyles['normal'])
        self.cell(50, 5, feature_info['nomcom'].encode('iso-8859-1')+str(' (')+str(feature_info['nufeco']).encode('iso-8859-1')+str(')'), 0, 0, 'L')

        # Creation date and operator
        y= self.get_y()
        self.set_y(y+10)
        self.set_font(*pdfconfig.textstyles['bold'])
        self.cell(45, 5, translations['extractoperatorlabel'], 0, 0, 'L')
        self.set_font(*pdfconfig.textstyles['normal'])
        self.cell(70, 5, feature_info['operator'].encode('iso-8859-1'), 0, 1, 'L')

        y= self.get_y()
        self.set_y(y+5)
        self.set_font(*pdfconfig.textstyles['bold'])
        self.cell(0, 5, translations['signaturelabel'], 0, 0, 'L')

        self.set_y(250)
        self.set_font(*pdfconfig.textstyles['bold'])
        self.cell(0, 5, translations['disclaimerlabel'], 0, 1, 'L')
        self.set_font(*pdfconfig.textstyles['normal'])
        self.multi_cell(0, 5, translations['disclaimer'], 0, 1, 'L')

        # END TITLEPAGE


    def get_map_format(self):
        """ Define the center and the bounding box of the map request to the wms
        """
        self.mapconfig = {'width':self.printformat['mapWidth'], 'height':self.printformat['mapHeight']}
        self.mapconfig['bboxCenterX'] = (self.featureInfo['BBOX']['maxX']+self.featureInfo['BBOX']['minX'])/2
        self.mapconfig['bboxCenterY'] = (self.featureInfo['BBOX']['maxY']+self.featureInfo['BBOX']['minY'])/2


    def get_site_map(self):
        """Creates the situation map of the property.
           input : the property's id,
           output : mapimage, mappath
        """

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
        sld += str(self.featureid)
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


        sldfile = open(self.appconfig.tempdir +self.pdfconfig.siteplanname+'_sld.xml', 'w')
        sldfile.write(sld)
        sldfile.close()

        # Layers as defined in our WMS - to replace with an array from a table 
        layers = [
            #'mo6_couverture_sol_nb_1',
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
            'mo22_batiments',
            'r157_lim_foret'
        ]

        scale = self.printformat['scale']*2
        # SitePlan/Plan de situation/Situationsplan
        sitemapparams = {'width':self.printformat['mapWidth'],'height':self.printformat['mapHeight']}
        sitemapparams['bboxCenterX'] = (self.featureInfo['BBOX']['maxX']+self.featureInfo['BBOX']['minX'])/2
        sitemapparams['bboxCenterY'] = (self.featureInfo['BBOX']['maxY']+self.featureInfo['BBOX']['minY'])/2
        #to recenter the map on the bbox of the feature, with the right scale and add at least 10% of space we calculate a wmsBBOX
        wmsBBOX = {}
        wmsBBOX['centerY'] =  int(sitemapparams['bboxCenterY'])
        wmsBBOX['centerX'] =  int(sitemapparams['bboxCenterX'])
        wmsBBOX['minX'] = int(wmsBBOX['centerX'] - (160*scale/1000/2))
        wmsBBOX['maxX'] = int(wmsBBOX['centerX']+(160*scale/1000/2))
        wmsBBOX['minY'] = int(wmsBBOX['centerY']-(90*scale/1000/2))
        wmsBBOX['maxY'] = int(wmsBBOX['centerY']+(90*scale/1000/2))

        #wms = WebMapService('http://sitn.ne.ch/mapproxy/service', version='1.1.1')
        wms = WebMapService(self.wms, version='1.1.1')

        sitemap = wms.getmap(
            layers=layers,
            sld = self.sld_url + self.pdfconfig.siteplanname + '_sld.xml',
            srs='EPSG:21781',
            bbox=(wmsBBOX['minX'],wmsBBOX['minY'],wmsBBOX['maxX'],wmsBBOX['maxY']),
            size=(1600,900),
            format='image/png',
            transparent=False
        )

        out = open(self.appconfig.tempdir +self.pdfconfig.siteplanname+'.png', 'wb')
        out.write(sitemap.read())
        out.close()

        self.sitemappath = self.appconfig.tempdir +self.pdfconfig.siteplanname+'.png'

    def add_topic(self, topic):
        """Adds a new entry to the topic list
           categorie = 0 : restriction not available - no layers
           categorie = 1 : restriction not touching the feature - layers, but no features (check geo availability)
           categorie = 2 : restriction touching the feature - layers and features
           categorie = 3 : restriction not legally binding - layers and features and complementary inform
        """
        self.topiclist[str(topic.topicid)]={
            'categorie':0,
            'topicname':topic.topicname,
            'layers':{},
            'authority':topic.authority, 
            'topicorder':topic.topicorder,
            #'references':topic.references,
            'legalbases':[],
            'legalprovisions':[],
            #'legalprovisions':topic.legalprovisions, 
            #'temporaryprovisions':topic.temporaryprovisions, 
            'authorityfk':topic.authorityfk,
            'publicationdate':topic.publicationdate,
            }
 
        # if geographic layers are defined for the topic, get the list of all layers and then
        # check for each layer the information regarding the features touching the property
        if topic.layers:
            self.add_toc_entry(topic.topicid, '', str(topic.topicname.encode('iso-8859-1')), 1, '')
            for layer in topic.layers:
                self.topiclist[str(topic.topicid)]['layers'][layer.layerid]={
                    'layername':layer.layername,
                    'layerreference':None,
                    'features':None
                    }
                self.add_layer(layer)
            self.get_map(topic.layers,topic.topicid)
        else:
            self.topiclist[str(topic.topicid)]['layers'] = None
            self.topiclist[str(topic.topicid)]['categorie']=0

        # if legal bases are defined for a topic the attributes are compiled in a list
        if topic.legalbases:
            self.get_legalbases(topic.legalbases,topic.topicid)
        else:
            self.topiclist[str(topic.topicid)]['legalbases']=None

        # if legal povisions are defined for a topic the attributes are compiled in a list
        if topic.legalprovisions:
            self.get_legalprovisions(topic.legalprovisions,topic.topicid)
        else:
            self.topiclist[str(topic.topicid)]['legalprovisions']=None

        # if references are defined for a topic the attributes are compiled in a list
        if topic.references:
            self.get_references(topic.references,topic.topicid)
        else:
            self.topiclist[str(topic.topicid)]['references']=None

    def add_layer(self, layer):
        results = get_features_function({'layerList':layer.layername,'id':self.featureid})
        if results :
            self.layerlist[str(layer.layerid)]={'layername':layer.layername,'features':[]}
            for result in results:
                self.layerlist[str(layer.layerid)]['features'].append(result['properties'])
                #~ if result['properties']['url_regl']:
                    #~ self.topiclist[str(layer.topicfk)]['legalprovisions'].append(result['properties']['url_regl'])
            self.topiclist[str(layer.topicfk)]['categorie']=3
            self.topiclist[str(layer.topicfk)]['no_page']='tocpg_'+str(layer.topicfk)
            self.topiclist[str(layer.topicfk)]['layers'][layer.layerid]['features']=self.layerlist[str(layer.layerid)]['features']
        else:
            self.layerlist[str(layer.layerid)]={'layername':layer.layername,'features':None}
            if self.topiclist[str(layer.topicfk)]['categorie'] != 3:
                self.topiclist[str(layer.topicfk)]['categorie']=1

    def get_legalbases(self, legalbases, topicid):
        """Decomposes the object containing all legalbases related to a topic in a list
        """
        self.legalbaselist[str(topicid)]=[]
        for legalbase in legalbases:
            #self.add_appendix(topicid, 'A'+str(len(self.appendix_entries)+1), unicode(legalbase.officialtitle).encode('iso-8859-1'), unicode(legalbase.legalbaseurl).encode('iso-8859-1'))
            self.legalbaselist[str(topicid)].append({
                'officialtitle':legalbase.officialtitle,
                'title':legalbase.title,
                'abreviation':legalbase.abreviation,
                'officialnb':legalbase.officialnb,
                'legalbaseurl':legalbase.legalbaseurl,
                'canton':legalbase.canton,
                'commune':legalbase.commune,
                'legalstate':legalbase.legalstate,
                'publishedsince':legalbase.publishedsince,
                #'metadata':legalbase.metadata
                })
        self.topiclist[str(topicid)]['legalbases'] = self.legalbaselist[str(topicid)]

    def get_legalprovisions(self, legalprovisions, topicid):
        """Decomposes the object containing all legal provisions related to a topic in a list
        """
        self.legalprovisionslist[str(topicid)]=[]
        for provision in legalprovisions:
            self.add_appendix(topicid, 'A'+str(len(self.appendix_entries)+1), unicode(provision.officialtitle).encode('iso-8859-1'), unicode(provision.legalprovisionurl).encode('iso-8859-1'))
            self.legalprovisionslist[str(topicid)].append({
                'officialtitle':provision.officialtitle,
                'title':provision.title,
                'abreviation':provision.abreviation,
                'officialnb':provision.officialnb,
                'legalprovisionurl':provision.legalprovisionurl,
                'canton':provision.canton,
                'commune':provision.commune,
                'legalstate':provision.legalstate,
                'publishedsince':provision.publishedsince,
                'no_page':'A'+str(len(self.appendix_entries))
                #'metadata':provision.metadata
                })
        self.topiclist[str(topicid)]['legalprovisions'] = self.legalprovisionslist[str(topicid)]

    def get_references(self, references, topicid):
        """Decomposes the object containing all references related to a topic in a list
        """
        self.referenceslist[str(topicid)]=[]
        for reference in references:
            self.referenceslist[str(topicid)].append({
                'officialtitle':reference.officialtitle,
                'title':reference.title,
                'abreviation':reference.abreviation,
                'officialnb':reference.officialnb,
                'legalprovisionurl':reference.referenceurl,
                'canton':reference.canton,
                'commune':reference.commune,
                'legalstate':reference.legalstate,
                'publishedsince':reference.publishedsince,
                #'metadata':legalprovision.metadata
                })
        self.topiclist[str(topicid)]['references'] = self.referenceslist[str(topicid)]

    def get_map(self,restriction_layers, topicid):
        """Produces the map and the legend for each layer of an restriction theme
        """
        # API GEO ADMIN EXAMPLE:
        # https://api.geo.admin.ch/feature/search?lang=en&layers=ch.bazl.projektierungszonen-flughafenanlagen&bbox=680585,255022,686695,259952&cb=Ext.ux.JSONP.callback

        # Map scale
        scale = self.printformat['scale']

        # List with the base layers of the map - the restriction layers get added to the list
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

        # temp var to hold the parameters of the legend
        legend_layers = []
        # temp var for the path to the created legend
        legend_path = []

        
        if topicid == '103':
            dffg
            # store the cadastral plan WMS parameters to overlay with federal data further on
            baselayers = layers
            baseurl = crdppf_wms

            layers = [
                'ch.bazl.projektierungszonen-flughafenanlagen',
                'ch.bazl.sachplan-infrastruktur-luftfahrt_kraft'
            ]
            crdppf_wms = 'http://wms.geo.admin.ch/'

        # Adding each layer of the restriction to the WMS
        for layer in restriction_layers:
            # Compile the layer list for the wms
            layers.append(layer.layername)

            # in the same time create the legend graphic for each layer and write it to disk
            if topicid == '103':
                legend = open(self.appconfig.tempdir+self.filename+str('_legend_')+str('103')+'.png', 'wb')
            else:
                legend = open(self.appconfig.tempdir+self.filename+str('_legend_')+str(layer.layername)+'.png', 'wb')
            img = urllib.urlopen(self.wms+ \
                str('?TRANSPARENT=TRUE&SERVICE=WMS&VERSION=1.1.1&REQUEST=GetLegendGraphic&FORMAT=image%2Fpng; mode=8bit&LAYER=' \
                +str(layer.layername)))

            legend.write(img.read())
            legend.close()
            if topicid == '103':
                legend_path.append(self.appconfig.tempdir+self.filename+str('_legend_')+str('103'))
            else:
                legend_path.append(self.appconfig.tempdir+self.filename+str('_legend_')+str(layer.layername))

        # to recenter the map on the bbox of the feature, compute the best scale and add at least 10% of space we calculate a wmsBBOX
        wmsBBOX = {}
        wmsBBOX['centerY'] = int(self.mapconfig['bboxCenterY'])
        wmsBBOX['centerX'] = int(self.mapconfig['bboxCenterX'])
        # From the center point add and substract half the map distance in X and Y direction to get BBOX min/max coords
        wmsBBOX['minX'] = int(wmsBBOX['centerX']-(self.printformat['width']*scale/1000/2))
        wmsBBOX['maxX'] = int(wmsBBOX['centerX']+(self.printformat['width']*scale/1000/2))
        wmsBBOX['minY'] = int(wmsBBOX['centerY']-(self.printformat['height']*scale/1000/2))
        wmsBBOX['maxY'] = int(wmsBBOX['centerY']+(self.printformat['height']*scale/1000/2))
        wmsbbox = [wmsBBOX['minX'], wmsBBOX['minY'], wmsBBOX['maxX'], wmsBBOX['maxY']]

        # call the WMS and write the map to file
        wms = WebMapService(self.wms, version='1.1.1')
        imgformat = 'image/png; mode=24bit'

        if topicid == '103':
            basewms = WebMapService(baseurl, version='1.1.1')
            #~ # BBOX Airport ZH Kloten
            #~ wmsbbox = [680585, 255022, 686695, 259952]
            basemap = basewms.getmap(
                layers = baselayers,
                srs = 'EPSG:21781',
                bbox = (wmsBBOX['minX'], wmsBBOX['minY'], wmsBBOX['maxX'], wmsBBOX['maxY']),
                size = (self.mapconfig['width'], self.mapconfig['height']),
                format = 'image/png',
                transparent = False
            )
            out1 = open(self.appconfig.tempdir+self.filename+str('_baselayer')+'.png', 'wb')
            out1.write(basemap.read())
            out1.close()

            overlay = wms.getmap(
                layers = layers,
                srs = 'EPSG:21781',
                bbox = (wmsBBOX['minX'], wmsBBOX['minY'], wmsBBOX['maxX'], wmsBBOX['maxY']),
                size = (self.mapconfig['width'], self.mapconfig['height']),
                format = 'image/png; mode=24bit',
                transparent = True
            )
            out2 = open(self.appconfig.tempdir+self.filename+str('_overlay')+'.png', 'wb')
            out2.write(overlay.read())
            out2.close()

            background = Image.open(self.appconfig.tempdir+self.filename+str('_baselayer')+'.png')
            foreground = Image.open(self.appconfig.tempdir+self.filename+str('_overlay')+'.png')

            background.paste(foreground, (0, 0), foreground)
            background.convert('RGB').convert('P', colors=256, palette=Image.ADAPTIVE)
            background.save(self.appconfig.tempdir + self.filename + '_'+str(topicid) + '.png')

        else:
            map = wms.getmap(
                layers = layers,
                srs = 'EPSG:21781',
                bbox = (wmsBBOX['minX'], wmsBBOX['minY'], wmsBBOX['maxX'], wmsBBOX['maxY']),
                size = (self.mapconfig['width'], self.mapconfig['height']),
                format = imgformat,
                transparent = False
            )

            out = open(self.appconfig.tempdir+self.filename+'_'+str(topicid)+'.png', 'wb')
            out.write(map.read())
            out.close()

        mappath = self.appconfig.tempdir + self.filename +'_'+ str(topicid) + '.png'
        # Add the path to the thematic map and it's legendfile to the topiclist
        self.topiclist[topicid].update({'mappath':mappath,'legendpath':legend_path})
        #return mappath, legend_path

    def add_toc_entry(self, topicid, num, label, categorie, appendices):
        self.toc_entries[str(topicid)]={'no_page':num, 'title':label, 'categorie':int(categorie), 'appendices':set()}

    def get_toc(self):
        """Adding a table of content (TOC) to the document.
           categorie = 0 : restriction not available - no layers
           categorie = 1 : restriction not touching the feature - layers, but no features (check geo availability)
           categorie = 2 : restriction touching the feature - layers and features
           categorie = 3 : restriction not legally binding - layers and features and complementary inform
        """
        translations = self.translations
        pdfconfig = self.pdfconfig
        feature_info = self.featureInfo

        # START TOC
        self.add_page()
        self.set_margins(*pdfconfig.pdfmargins)
        self.set_y(40)
        self.set_font(*pdfconfig.textstyles['title3'])
        self.multi_cell(0, 12, translations['toclabel'])

        self.set_y(60)
        self.set_font(*pdfconfig.textstyles['bold'])
        self.cell(12, 15, '', '', 0, 'L')
        self.cell(118, 15, '', 'L', 0, 'L')
        self.cell(15, 15, '', 'L', 0, 'C')
        self.cell(15, 15, '', 'L', 1, 'C')

        self.cell(12, 5, translations['pagelabel'], 'B', 0, 'L')
        self.cell(118 ,5, translations['toclabel'], 'LB', 0, 'L')
        y = self.get_y()
        x = self.get_x()
        self.rotate(90)
        self.text(x-4, y+8, translations['legalprovisionslabel'])
        self.text(x-4, y+23, translations['referenceslabel'])
        self.rotate(0)
        self.cell(15, 5, '', 'LB', 0, 'L')
        self.cell(15, 5, '', 'LB', 1, 'L')

        # List of all topics with a restriction for the selected parcel 
        for entry, column in self.topiclist.iteritems() :
            if column['categorie'] == 3 :
                self.set_font(*pdfconfig.textstyles['bold'])
                if column['no_page'] is not None:
                    self.cell(12, 6, column['no_page'],'B', 0, 'L')
                else:
                    self.cell(12, 6, '', 'B', 0, 'C')
                self.cell(118, 6, column['topicname'], 'LB', 0, 'L')
                if column['legalprovisions'] is not None :
                    pageslist = []
                    for legalprovision in column['legalprovisions']:
                        pageslist.append(legalprovision['no_page'])
                    self.cell(15, 6, ', '.join(pageslist), 'LB', 0, 'C')
                else:
                    self.cell(15, 6, '', 'LB', 0, 'L')
                self.cell(15, 6, '', 'LB', 1, 'L')

        self.ln()
        self.ln()
        self.set_font(*pdfconfig.textstyles['tocbold'])
        self.multi_cell(0, 5, translations['notconcerndbyrestrictionlabel'], 'B', 1, 'L')
        self.ln()

        for entry, column in self.topiclist.iteritems() :
            if column['categorie'] == 1 :
                self.set_font(*pdfconfig.textstyles['tocbold'])
                self.cell(118, 6, column['topicname'], '', 0, 'L')
                self.cell(15, 6, '', '', 0, 'L')
                self.cell(15, 6, '', '', 1, 'L')

        self.ln()
        self.set_font(*pdfconfig.textstyles['tocbold'])
        self.multi_cell(0, 5, translations['restrictionnotavailablelabel'], 'B', 1, 'L')
        self.ln()
        
        for entry, column in self.topiclist.iteritems() :
            if column['categorie'] == 0 :
                self.set_font(*pdfconfig.textstyles['tocbold'])
                self.cell(118,6,column['topicname'],0,0,'L')
                self.cell(15,6,'',0,0,'L')
                self.cell(15,6,'',0,1,'L')
                
        self.ln()
        self.set_font(*pdfconfig.textstyles['tocbold'])
        self.multi_cell(0, 5, translations['restrictionnotlegallybindinglabel'], 'B', 1, 'L')
        self.ln()

        self.set_font(*pdfconfig.textstyles['tocbold'])
        self.cell(118, 6, translations['norestrictionlabel'], 0, 0, 'L')
        self.cell(15, 6, str(''), 0, 0, 'L')
        self.cell(15, 6, str(''), 0, 1, 'L')

    def write_thematic_page(self, topic):
        """Writes the page for the given topic
        """
        translations = self.translations
        pdfconfig = self.pdfconfig
        feature_info = self.featureInfo
        
        if self.topiclist[topic]['categorie'] > 2:
            self.add_page()
            self.set_margins(*pdfconfig.pdfmargins)
            tocpgalias = 'tocpg_'+str(topic)
            self.pages[2] = self.pages[2].replace(tocpgalias,str(self.page_no()))


            # Place the map
            self.image(self.topiclist[topic]['mappath'], 65, pdfconfig.headermargin, self.printformat['width'], self.printformat['height'])
            self.rect(65, pdfconfig.headermargin, self.printformat['width'], self.printformat['height'], '')
            # Define the size of the legend container
            legendbox_width = 40
            legendbox_height = self.printformat['height'] 
            legendbox_proportion = float(legendbox_width-4) / float(legendbox_height-20)

            # draw the legend container
            self.rect(pdfconfig.leftmargin, pdfconfig.headermargin, legendbox_width, legendbox_height, '')

            # define cells with border for the legend and the map
            self.set_xy(28, pdfconfig.headermargin+3)
            self.set_font(*pdfconfig.textstyles['bold'])
            self.cell(50, 6, translations['legendlabel'], 0, 1, 'L')
            y= self.get_y()
            self.set_font(*pdfconfig.textstyles['normal'])
            if  len(self.topiclist[topic]['legendpath']) > 0:
                max_legend_width_px = 0
                tot_legend_height_px = 0
                sublegends = []

                for graphic in self.topiclist[topic]['legendpath']:
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
                    y = self.get_y()
                    legend = self.image(path+'.png',26, y, float(width)/limit_proportion)
                    self.set_y(y+(float(height)/limit_proportion))

            self.set_y(40)
            self.set_font(*pdfconfig.textstyles['title3'])
            self.multi_cell(0, 6, str(self.topiclist[topic]['topicname'].encode('iso-8859-1')), 0, 1, 'L')
            y = self.get_y()
            self.set_y(y+110)
            
            if self.topiclist[topic]['layers']:
                for layer in self.topiclist[topic]['layers']:
                    if self.topiclist[topic]['layers'][layer]['features']:
                        for feature in self.topiclist[topic]['layers'][layer]['features']:
                            if 'teneur' in feature.keys():
                                self.set_font(*pdfconfig.textstyles['bold'])
                                self.cell(55, 5, translations['contentlabel'].encode('iso-8859-1'), 0, 0, 'L')
                                self.set_font(*pdfconfig.textstyles['normal'])
                                if feature['statutjuridique'] is None:
                                    feature['statutjuridique'] = 'None'
                                self.multi_cell(100, 5, feature['teneur'].encode('iso-8859-1') \
                                    +'\t('+feature['intersectionMeasure'].replace(' - ','').encode('iso-8859-1')+')', 0, 1, 'L')

                            elif self.topiclist[topic]['layers'][layer]['layername'] in ['en07_canepo_accidents','en07_canepo_decharges_points','en07_canepo_decharges_polygones','en07_canepo_entreprises_points']:
                                self.set_font(*pdfconfig.textstyles['bold'])
                                self.cell(55, 5, translations['contentlabel'].encode('iso-8859-1'), 0, 0, 'L')
                                self.set_font(*pdfconfig.textstyles['normal'])
                                self.multi_cell(100, 5, unicode(feature['statut_osi']).encode('iso-8859-1'), 0, 1, 'L')
                                
                            elif self.topiclist[topic]['layers'][layer]['layername'] == 'en01_zone_sect_protection_eaux':
                                self.set_font(*pdfconfig.textstyles['bold'])
                                self.cell(55, 5, translations['contentlabel'].encode('iso-8859-1'), 0, 0, 'L')
                                self.set_font(*pdfconfig.textstyles['normal'])
                                self.multi_cell(100, 5, feature['categorie'].encode('iso-8859-1'), 0, 1, 'L')

                            elif self.topiclist[topic]['layers'][layer]['layername'] == 'clo_couloirs':
                                self.set_font(*pdfconfig.textstyles['bold'])
                                self.cell(55, 5, translations['contentlabel'].encode('iso-8859-1'), 0, 0, 'L')
                                self.set_font(*pdfconfig.textstyles['normal'])
                                self.multi_cell(100, 5, feature['type'].encode('iso-8859-1'), 0, 1, 'L')

                            elif self.topiclist[topic]['layers'][layer]['layername'] == 'clo_cotes_altitude_surfaces':
                                self.set_font(*pdfconfig.textstyles['bold'])
                                self.cell(55, 5, translations['contentlabel'].encode('iso-8859-1'), 0, 0, 'L')
                                self.set_font(*pdfconfig.textstyles['normal'])
                                self.multi_cell(100, 5, str(feature['cote_alt_obstacles_minimum']).encode('iso-8859-1'), 0, 1, 'L')
                                
                            else:
                                for property,value in feature.iteritems():
                                    if value is not None and property != 'featureClass':
                                        self.set_font(*pdfconfig.textstyles['bold'])
                                        self.cell(55, 5, translations['contentlabel'].encode('iso-8859-1'), 0, 0, 'L')
                                        self.set_font(*pdfconfig.textstyles['normal'])
                                        if isinstance(value, float) or isinstance(value, int):
                                            value = str(value)
                                        self.multi_cell(100, 5, value.encode('iso-8859-1'), 0, 1, 'L')
            else:
                self.multi_cell(100, 5, 'Error in line 818', 0, 1, 'L')

                # Legal Provisions/Dispositions juridiques/Gesetzliche Bestimmungen
                y = self.get_y()
                self.set_y(y+5)
                self.set_font(*pdfconfig.textstyles['bold'])
                self.cell(55, 6, translations['legalprovisionslabel'], 0, 0, 'L')
                self.set_font(*pdfconfig.textstyles['normal'])
                if self.topiclist[topic]['legalprovisions']:
                    count = 0 
                    for provision in self.topiclist[topic]['legalprovisions']:
                        self.add_appendix(topic.topicid, 'A'+str(count+1), unicode(provision.officialtitle).encode('iso-8859-1'), unicode(provision.legalprovisionurl).encode('iso-8859-1'))
                        self.cell(0, 5, unicode(provision.officialtitle).encode('iso-8859-1'), 0, 1, 'L')
                        self.set_text_color(0, 0, 255)
                        self.set_x(80)
                        self.multi_cell(0, 6, unicode(provision.legalprovisionurl).encode('iso-8859-1'))
                        self.set_text_color(0, 0, 0)
                else:
                        self.multi_cell(0, 6, unicode('None').encode('iso-8859-1'))

            # References and complementary information/Informations et renvois supplémentaires/Verweise und Zusatzinformationen
            y = self.get_y()
            self.set_y(y+5)
            self.set_font(*pdfconfig.textstyles['bold'])
            self.cell(55, 6, translations['referenceslabel'], 0, 0, 'L')
            self.set_font(*pdfconfig.textstyles['normal'])
            if self.topiclist[topic]['references']:
                for reference in self.topiclist[topic]['references']:
                    self.multi_cell(0, 6, unicode(reference['officialtitle']).encode('iso-8859-1'))
            else:
                    self.multi_cell(0, 6, unicode('None','utf-8').encode('iso-8859-1')) 

            # -- KEEP FOR FURTHER USE
            
            # Ongoing amendments/Modifications en cours/Laufende Änderungen
            #~ y = self.get_y()
            #~ self.set_y(y+5)
            #~ self.set_font(*pdfconfig.textstyles['bold'])
            #~ self.cell(55, 6, translations['temporaryprovisionslabel'], 0, 0, 'L')
            #~ self.set_font(*pdfconfig.textstyles['normal'])
            #~ if self.topiclist[topic]['temporaryprovisions']:
                #~ for temp_provision in self.topiclist[topic]['temporaryprovisions']:
                    #~ self.multi_cell(0, 6, unicode(temp_provision.officialtitle).encode('iso-8859-1'), 0, 1, 'L')
                    #~ if temp_provision.temporaryprovisionurl :
                        #~ self.set_x(80)
                        #~ self.multi_cell(0, 6, unicode(temp_provision.temporaryprovisionurl).encode('iso-8859-1'))
            #~ else:
                    #~ self.multi_cell(0, 6, unicode('None','utf-8').encode('iso-8859-1'), 0, 1, 'L')

            # --  END KEEP

            # Competent Authority/Service competent/Zuständige Behörde
            y = self.get_y()
            self.set_y(y+5)
            self.set_font(*pdfconfig.textstyles['bold'])
            self.cell(55, 3.9, translations['competentauthoritylabel'], 0, 0, 'L')
            self.set_font(*pdfconfig.textstyles['normal'])
            
            if self.topiclist[topic]['authority'].authorityname is not None:
                self.cell(120, 3.9, self.topiclist[topic]['authority'].authorityname.encode('iso-8859-1'), 0, 1, 'L')
            if self.topiclist[topic]['authority'].authoritydepartment is not None:
                self.cell(55, 3.9, str(' '), 0, 0, 'L')
                self.cell(120, 3.9, self.topiclist[topic]['authority'].authoritydepartment.encode('iso-8859-1'), 0, 1, 'L')
            if self.topiclist[topic]['authority'].authorityphone1 is not None:
                self.cell(55, 3.9, str(' '), 0, 0, 'L')
                self.cell(120, 3.9, translations['phonelabel']+self.topiclist[topic]['authority'].authorityphone1.encode('iso-8859-1'), 0, 1, 'L')
            if self.topiclist[topic]['authority'].authoritywww is not None:
                self.cell(55, 3.9, str(' '), 0, 0, 'L')
                self.cell(120, 3.9, translations['webadresslabel']+self.topiclist[topic]['authority'].authoritywww.encode('iso-8859-1'),0,1,'L')

            # Legal bases/Bases légales/Gesetzliche Grundlagen
            y = self.get_y()
            self.set_y(y+5)
            self.set_font(*pdfconfig.textstyles['bold'])
            self.cell(55, 6, translations['legalbaseslabel'], 0, 0, 'L')
            self.set_font(*pdfconfig.textstyles['normal'])
            if self.topiclist[topic]['legalbases']:
                for legalbase in self.topiclist[topic]['legalbases']:
                    self.multi_cell(100, 5, legalbase['officialtitle'], 0, 1, 'L')
            else:
                self.multi_cell(0, 6, translations['placeholderlabel'])

    def add_appendix(self, topicid, num, label,url):
        self.appendix_entries.append({'topicid':topicid, 'no_page':num, 'title':label, 'url':url})
        if self.toc_entries[str(topicid)] :
            self.toc_entries[topicid]['appendices'].add(num)
        else:
            pass

    def add_reference(self, topicid, num, label,url):
        self.reference_entries.append({'topicid':topicid, 'no_page':num, 'title':label, 'url':url})
        if self.toc_entries[str(topicid)] :
            self.toc_entries[topicid]['reference'].add(num)
        else:
            pass

    def get_appendices(self):
        """Adding a list of appendix to the document."""
        translations = self.translations
        pdfconfig = self.pdfconfig
        feature_info = self.featureInfo

        # START APPENDIX
        self.add_page()
        self.set_margins(*pdfconfig.pdfmargins)
        self.set_y(40)
        self.set_font(*pdfconfig.textstyles['title3'])
        self.multi_cell(0, 12, translations['appendiceslistlabel'])

        self.set_y(60)
        self.set_font(*pdfconfig.textstyles['bold'])
        self.cell(15, 6, translations['pagelabel'], 0, 0, 'L')
        self.cell(135, 6, translations['appendicestitlelabel'], 0, 1, 'L')


    def Appendices(self):

        self.add_page()
        self.set_margins(*self.pdfconfig.pdfmargins)
        self.set_y(40)
        self.set_font(*self.pdfconfig.textstyles['title3'])
        self.multi_cell(0, 12, self.translations['appendiceslistlabel'])

        self.set_y(60)
        self.set_font(*self.pdfconfig.textstyles['bold'])
        self.cell(15, 6, self.translations['pagelabel'], 0, 0, 'L')
        self.cell(135, 6, self.translations['appendicestitlelabel'], 0, 1, 'L')
        
        index = 1
        for appendix in self.appendix_entries:
            self.set_font(*self.pdfconfig.textstyles['tocbold'])
            self.cell(15, 6, str('A'+str(index)), 0, 0, 'L')
            self.cell(120, 6, str(appendix['title']), 0, 1, 'L')
            self.set_x(40)
            self.set_font(*self.pdfconfig.textstyles['tocurl'])
            self.set_text_color(*self.pdfconfig.urlcolor)
            self.multi_cell(0, 5, str(appendix['url']))
            self.set_text_color(*self.pdfconfig.defaultcolor)
            index = index+1
