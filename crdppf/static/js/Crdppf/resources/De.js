Ext.namespace('Crdppf');

// Themes structure and content definition
Crdppf.layerListDe = {
    "type": "ThemesCollection",
        'themes' :[  
                        {'id':'73','image':'amenagement.gif','name':'Raumplanung', 'layers':{'at14_zones_communales':'Gemeindes Zone','at08_zones_cantonales':'Kantonalen Zone','at39_itineraires_pedestres':'Fusswege','at28_limites_constructions':'Limites constructions'}},
                        {'id':'998','image':'routes_nationales.gif','name':'Nationalstrassen','layers':{'at39_itineraires_pedestres':'Fusswege'}},                        
                        {'id':'500','image':'chemin_fer.gif','name':'Eisenbahnen','layers':{'at39_itineraires_pedestres':'Fusswege'}},                        
                        {'id':'108','image':'aeroports.gif','name':'Flughäfen', 'layers':{'clo_couloirs':'Couloirs d\'obstacles aériens','clo_cotes_altitude_surfaces':'Cotes d\'altitude des surfaces'}},
                        {'id':'116','image':'sites_pollues.gif','name':'Belastete Standorte','layers':{'en07_canepo_accidents':'Belastete Standorte: Unfälle','en07_canepo_decharges':'Belastete Standorte: Deponien','en07_canepo_decharges_points':'Belastete Standorte: Deponien (punkte)','en07_canepo_decharges_polygones':'Belastete Standorte: Deponien (polygon)', 'en07_canepo_entreprises':'Belastete Standorte: Deponien', 'en07_canepo_entreprises_points':'Belastete Standorte: Unternehmen (Punkte)', 'en07_canepo_entreprises_polygones':'Belastete Standorte: Unternehmen (Polygon)'}},
                        {'id':'997','image':'protection_eaux.gif','name':'Grundwasserschutz','layers':{'en01_zone_sect_protection_eaux':'Grundwasserschutz'}},
                        {'id':'996','image':'bruit.gif','name':'Lärm','layers':{'en05_degres_sensibilite_bruit':'Lärm'}},
                        {'id':'999','image':'foret.gif','name':'Wald','layers':{'at39_itineraires_pedestres':'Fusswege'}}
        ]
    };
    
Crdppf.baseLayersDe = { 
        'baseLayers':[
            {'id': '1', 'image': 'plan_cadastral.png', 'name': 'Plan cadastral', 'wmtsname': 'plan_cadastral_c2c'},
            {'id': '2', 'image': 'plan_cadastral.png', 'name': 'Orthophoto', 'wmtsname': 'ortho2011'},
            {'id': '3', 'image': 'plan_cadastral.png', 'name': 'Plan de ville', 'wmtsname': 'plan_ville_c2c'}
        ]
};
    
// Application labels text values for french
Crdppf.labelsDe  ={
    'navPanelLabel':'Navigation',
    'infoMsgTitle': 'Info',
    'searchBoxTxt':'Suche...',
    'themeSelectorLabel':'Themenwahl',
    'waitMessage': 'Daten werden geladen...',
    'mapContainerTab':'Karte',
    'legalBasisTab':'Gesetzliche Grundlagen',
    'layerTreeTitle':'Daten',
    'selectAllLayerLabel':'Alle Ebenen auswählen',
    'lawTabLabel':'Rechtsvorschriften',
    'additionnalInfoTab':'Verweise und Zusatzinformationen',
    'infoTabLabel':'Informationen',
    'legendPanelTitle':'Legende',
    'searchBoxEmptyTxt':'Suchen...',
    'olCoordinates':'Koordinaten',
    'restrictionPanelTitle':'Eigentumsbeschränkungen',
    'restrictionPanelTxt':'Eigentumsbeschränkungen der Parzelle Nr. ',
    'noActiveLayertxt':'Keine Ebene aktiv',
    'restrictionFoundTxt':'Eigentumsbeschränkung Nr. ',
    'disclaimerTxt':'Haftungsausschluss : Der Kanton Neuenburg übernimmt keine Garantie für die Exaktheit und Vollständigkeit der Gesetzestexte in ihrer elektronischen Form. Diese Dokumente ...',
    'mapBottomTxt':'<b>Daten sind nicht rechtsverbindlich, <a style="color:#660000;" href="http://sitn.ne.ch/web/conditions_utilisation/contrat_SITN_MO.htm" target="_new">&copy; SITN</a></b>',
    'intersectToolTipMessage':'Räumliche Beziehung: Schnittpunkt',
    'withinToolTipMessage':'Räumliche Beziehung: innerhalb',
    'adjacentToolTipMessage':'Räumliche Beziehungen: benachbarte',
    'printPdfWindowsTitle': 'PDF',
    'noSelectedParcelMessage': 'Wählen Sie zuerst ein Grundstück !',
    'printButtonTlp':'Générer l\'extrait',
    'infoButtonTlp':'Sélectionner une parcelle et ses restrictions',
    'panButtonTlp':'Déplacement de la carte',
    'zoomInButtonTlp':'Zoom avant',
    'zoomOutButtonTlp':'Zoom arrière',
    'infoButtonTlp': 'Auswahl löschen',
    'baseLayerGroup': 'Grundkarte'
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