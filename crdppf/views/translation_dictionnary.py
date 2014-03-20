# -*- coding: UTF-8 -*-
from pyramid.view import view_config

from crdppf.util.pdf_functions import get_translations

@view_config(route_name='get_translation_dictionary', renderer='json')
def get_translation_dictionary(request):
    """Return a JSON file including all translations stored in the database
    """    
    
    # Get the session
    session = request.session
    
    # Define language to get multilingual labels for the selected language
    # defaults to 'fr': french - this may be changed in the appconfig
    if 'lang' not in session:
        lang = request.registry.settings['default_language'].lower()
    else : 
        lang = session['lang'].lower()
    translationDico = get_translations(lang)
    # get the translation dictionnary
    langDico = get_translations(lang)
    
    return langDico
    

