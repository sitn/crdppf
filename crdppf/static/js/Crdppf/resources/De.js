Ext.namespace('Crdppf');

// Themes structure and content definition
Crdppf.layerListDe = {
    "type": "ThemesCollection",
        'themes' :[  
                        {'id':'73','image':'amenagement.gif','name':'Raumplanung', 'layers':{'r73_affectations_primaires':'Grundnutzungszonen','r73_zones_superposees':'Überlagerte Nutzungszonen','r73_perimetres_superposes':'Überlagerte Perimeter','r73_contenus_lineaires':'Lineare Planungselemente','r73_contenus_ponctuels':'Punktförmige Planungselemente'}},
                        {'id':'88','image':'routes_nationales.gif','name':'Nationalstrassen','layers':{}},
                        {'id':'96','image':'chemin_fer.gif','name':'Eisenbahnen','layers':{}},
                        {'id':'108','image':'aeroports.gif','name':'Flughäfen', 'layers':{'r103_bazl_projektierungszonen_flughafenanlagen':'Projektierungszonen Flughafenanlagen','r108_bazl_sicherheitszonenplan':'Sicherheitszonenplan'}},
                        {'id':'116','image':'sites_pollues.gif','name':'Belastete Standorte','layers':{'r116_sites_pollues':'Belastete Standorte'}},
                        {'id':'997','image':'protection_eaux.gif','name':'Grundwasserschutz','layers':{'r131_zone_prot_eau':'Grundwasserschutzzonen','r132_perimetre_prot_eau':'Grundwasserschutzsektoren'}},
                        {'id':'996','image':'bruit.gif','name':'Lärm','layers':{'r145_sens_bruit':'Lärmepfindlichkeitsstufen'}},
                        {'id':'999','image':'foret.gif','name':'Wald','layers':{'r157_lim_foret':'Waldgrenzen','r159_dist_foret':'Waldabstandslinien'}}
        ]
    };
    
Crdppf.baseLayersDe = { 
        'baseLayers':[
            {'id': '1', 'image': 'plan_cadastral.png', 'name': 'Katasterplan', 'wmtsname': 'plan_cadastral_c2c'},
            {'id': '2', 'image': 'plan_cadastral.png', 'name': 'Orthophoto', 'wmtsname': 'ortho2011'},
            {'id': '3', 'image': 'plan_cadastral.png', 'name': 'Ortsplan', 'wmtsname': 'plan_ville_c2c'}
        ]
};
    
OpenLayers.Util.extend(OpenLayers.Lang.de, {
    'adresses_sitn':'Adressen',
    'axe_rue':'Strassennamen',
    'nom_local_lieu_dit':'Flurname, Geländename',
    'search_arrets_tp':'Haltestellen ÖV',
    'search_cours_eau':'Flüsse, Bäche',
    'search_axes_rtes':'Verkehrsachsen',
    'search_satac':'Baubewilligungen',
    'search_uap_publique':'Öffentliche Forsteinheiten',
    'search_fo_administrations':'Forstverwaltungen',
    'ImmeublesCanton':'Grundstücke',
    'ImmeublesCantonHistorique':'Historische Grundstücke',
    'batiments_ofs':'BFS-Gebäudenummern',
    'point_interet':'Öffentl. Gebäude, Sehenswürdigkeiten'
});