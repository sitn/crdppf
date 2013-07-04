# -*- coding: UTF-8 -*-

from fpdf import FPDF
import pkg_resources
from datetime import datetime

class PDFConfig:
    """A class to define the configuration of the PDF extract to simplify changes.
    """
    def __init__(self, request):
            self.sld_url = request.static_url('crdppf:static/public/temp_files/')

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
    textstyles = {'title1':[fontfamily, 'B', 22],
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
    pdfpath = pkg_resources.resource_filename('crdppf', 'static/public/pdf/')

class Objectify:
    """A helper class to create an object from a dict for lazy programmers 
    who do not like dict in dict in dict...
    """
    def __init__(self, **kwds):
        self.__dict__.update(kwds)

class ExtractPDF(FPDF):
    # =============================
    # VARIABLES :
    # extract  = principal array holding all the data needed to create the pdf extract converted to an object to simplify the acces to the nested data
    # extract.featureInfo
    # extract.topicList
    # extract.pdfFormat
    # extract.mapFormat
    # =============================
    
    # GENERAL CONFIG VARS
    # ALL this vars may be called by a method of the class using self.varname
    # ==================================================================
    imagebasepath = pkg_resources.resource_filename('crdppf','static\images\\')
    CHlogopath = 'ecussons\\logoCH.png'
    cantonlogopath = 'ecussons\\06ne_ch_RVB.jpg'
    creationdate = datetime.now().strftime("%d.%m.%Y-%H:%M:%S")
    signatureid = datetime.now().strftime("%Y%m%d%H%M%S")
    signaturelabel = 'ID Nr : '
    pagelabel = 'Page : '

    def __init__(self, nomcom, pdfconfig, translations):
        FPDF.__init__(self)
        self.toc_entries = []
        self.appendix_entries = []
        self.commune = nomcom
        self.translations = translations
        self.pdfconfig = pdfconfig
        self.communelogopath = 'ecussons\\' + str(self.commune) + '.jpg'

    def alias_nomcom(self, alias='{nomcom}'):
        """Define an alias for the municipality name"""
        self.str_alias_nomcom = alias
        return alias
        
    def alias_no_page(self, alias='{no_pg}'):
        """Define an alias for total number of pages"""
        self.str_alias_no_page = alias
        return alias
        
    def header(self):
        """Creates the document header with the logos and vertical lines."""
        
        # no_page = self.page_no()
        # nb_pages = self.alias_nb_pages()
        nomcom = self.alias_nomcom()

        # Add the vertical lines
        self.set_line_width(0.3)
        self.line(105, 0, 105, 35)
        self.line(165, 0, 165, 35)
        # Add the logos if existing else put a placeholder
        self.image(self.imagebasepath+self.CHlogopath, 10, 8, 55, 31.03)
        self.image(self.imagebasepath+self.cantonlogopath, 110, 8, 43.4, 13.8)
        try:
            self.image(self.imagebasepath+self.communelogopath, 170, 8, 10, 10.7)
        except:
            self.image(self.imagebasepath+'ecussons\Placeholder.jpg', 170, 8, 10, 10.7)
        # This lines are not necessary if the community name is already contained in the 
        # logo
        self.set_xy(170, 19.5)
        self.set_font(*self.pdfconfig.textstyles['small'])
        self.cell(30, 3, unicode(nomcom,'utf-8').encode('iso-8859-1'), 0, 0, 'L')

    def footer(self):
        """Creates the document footer"""

        # position footer at 15mm from the bottom
        self.set_y(-20)
        self.set_font(*self.pdfconfig.textstyles['small'])
        self.cell(55, 5, self.translations['creationdatelabel']+str(' ')+self.creationdate, 0, 0, 'L')
        self.cell(60, 5, self.translations['signaturelabel']+str(' ')+self.signatureid, 0, 0, 'C')
        self.cell(55, 5, self.translations['pagelabel']+str(self.alias_no_page())+str('/')+ \
            str(self.alias_nb_pages()), 0, 0, 'R')

    def add_toc_entry(self,topicid,num,label,categorie,appendices):
        self.toc_entries.append({'topicid':topicid,'no_page':num, 'title':label, 'categorie':int(categorie), 'appendices':[]})

    def TOC(self):
        """Adding a table of content (TOC) to the document."""
        toc_pages.add_page()
        toc_pages.set_margins(*pdfconfig.pdfmargins)
        toc_pages.set_y(40)
        toc_pages.set_font(*pdfconfig.textstyles['title3'])
        toc_pages.multi_cell(0, 12, translations['toclabel'])

        toc_pages.set_y(60)
        toc_pages.set_font(*pdfconfig.textstyles['bold'])
        toc_pages.cell(12, 15, str(''), '', 0, 'L')
        toc_pages.cell(118, 15, str(''), 'L', 0, 'L')
        toc_pages.cell(15, 15, str(''), 'L', 0, 'C')
        toc_pages.cell(15, 15, str(''), 'L', 1, 'C')

        toc_pages.cell(12, 5, translations['pagelabel'], 'B', 0, 'L')
        toc_pages.cell(118 ,5, translations['toclabel'], 'LB', 0, 'L')
        toc_pages.cell(15, 5, translations['legalprovisionslabel'], 'LB', 0, 'C')
        toc_pages.cell(15, 5, translations['referenceslabel'], 'LB', 1, 'C')

    def add_appendix(self,topicid,num,label,url):
        self.appendix_entries.append({'topicid':topicid, 'no_page':num, 'title':label, 'url':url})
