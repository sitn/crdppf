# -*- coding: UTF-8 -*-

from fpdf import FPDF
import pkg_resources
from datetime import datetime

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

    def __init__(self, arg):
        FPDF.__init__(self)
        self.toc_entries = []
        self.appendix_entries = []
        self.commune = arg

    def alias_nomcom(self, alias='{nomcom}'):
        """Define an alias for the county name"""
        self.str_alias_nomcom = alias
        return alias
        
    def alias_no_page(self, alias='{no_pg}'):
        """Define an alias for total number of pages"""
        self.str_alias_no_page = alias
        return alias
        
    def header(self):
        """Creates the document header with the logos and vertical lines."""
        # path to the image files used in the header
        path = pkg_resources.resource_filename('crdppf','static\images\\')
        
        # no_page = self.page_no()
        # nb_pages = self.alias_nb_pages()
        nomcom = self.alias_nomcom()

        # Add the vertical lines
        self.set_line_width(0.3)
        self.line(105, 0, 105, 34)
        self.line(165, 0, 165, 34)
        # Add the logos if existing else put a placeholder
        self.image(path+"ecussons\logoCH.png", 10, 8, 55, 31.03)
        self.image(path+"ecussons\\06ne_ch_RVB.jpg", 108, 8, 43.4, 13.8)
        try:
            self.image(path+'ecussons\\'+self.commune+'.jpg', 170, 8, 10, 10.7)
        except:
            self.image(path+'ecussons\Placeholder.jpg', 170, 8, 10, 10.7)
        self.set_xy(170, 19.5)
        self.set_font('Arial', '', 7)
        self.cell(30, 3, unicode(nomcom,'utf-8').encode('iso-8859-1'), 0, 0, 'L')

    def footer(self):
        """Creates the document footer"""

        # position footer at 15mm from the bottom
        self.set_y(-20)
        self.set_font('Arial', '', 7)
        self.cell(0, 10, unicode('Date d\'établissement : ' \
            +datetime.now().strftime("%d.%m.%Y-%H:%M:%S")+'        ID Nr : 123456789           Page : ', \
            'utf-8').encode('iso-8859-1')+str(self.alias_no_page())+str('/')+ \
            str(self.alias_nb_pages()), 0, 0, 'C')

    def add_toc_entry(self,num,label,categorie):
        self.toc_entries.append({'no_page':num, 'title':label, 'categorie':int(categorie)})

    def add_appendix(self,num,label,url):
        self.appendix_entries.append({'no_page':num, 'title':label, 'url':url})
