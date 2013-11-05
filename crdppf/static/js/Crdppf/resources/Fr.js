Ext.namespace('Crdppf');

// Themes structure and content definition
Crdppf.layerListFr = {
    "type": "ThemesCollection",
        'themes' :[  
                        {'id':'73','image':'amenagement.gif','name':'Zones Affectation', 'layers':{'at14_zones_communales':'Zones communales','at08_zones_cantonales':'Zones cantonales','at39_itineraires_pedestres':'Itinéraires pédestres', 'at28_limites_constructions':'Limites constructions'}},
                        {'id':'998','image':'routes_nationales.gif','name':'Routes nationales','layers':{'at39_itineraires_pedestres':'Itinéraires pédestres'}},   
                        {'id':'500','image':'chemin_fer.gif','name':'Chemin de fer','layers':{'at39_itineraires_pedestres':'Itinéraires pédestres'}},   
                        {'id':'108','image':'aeroports.gif','name':'Aéroports', 'layers':{'clo_couloirs':'Couloirs d\'obstacles aériens','clo_cotes_altitude_surfaces':'Cotes d\'altitude des surfaces'}},
                        {'id':'116','image':'sites_pollues.gif','name':'Cadastre des sites pollués','layers':{'en07_canepo_accidents':'Sites polluées : accidents','en07_canepo_decharges':'Sites pollués : décharges','en07_canepo_decharges_points':'Sites pollués : décharges (points)','en07_canepo_decharges_polygones':'Sites pollués : décharges (polygones)', 'en07_canepo_entreprises':'Sites pollués : entreprises', 'en07_canepo_entreprises_points':'Sites pollués : entreprises (points)', 'en07_canepo_entreprises_polygones':'Sites pollués : entreprises (polygones)'}},
                        {'id':'997','image':'protection_eaux.gif','name':'Protection des eaux','layers':{'en01_zone_sect_protection_eaux':'Secteurs de protection des eaux'}},
                        {'id':'996','image':'bruit.gif','name':'Bruit','layers':{'en05_degres_sensibilite_bruit':'Degrés de sensibilité au bruit'}},
                        {'id':'999','image':'foret.gif','name':'Forêts','layers':{'at39_itineraires_pedestres':'Itinéraires pédestres'}}
        ]
    };
    
Crdppf.baseLayersFr = { 
        'baseLayers':[
            {'id': '1', 'image': 'plan_cadastral.png', 'name': 'Plan cadastral', 'wmtsname': 'plan_cadastral_c2c'},
            {'id': '2', 'image': 'plan_cadastral.png', 'name': 'Orthophoto', 'wmtsname': 'ortho2011'},
            {'id': '3', 'image': 'plan_cadastral.png', 'name': 'Plan de ville', 'wmtsname': 'plan_ville_c2c'}
        ]
};
 
// Application labels text values for french  
Crdppf.labelsFr  ={
    'navPanelLabel':'Navigation',
    'infoMsgTitle': 'Info',
    'searchBoxTxt':'Rechercher...',
    'themeSelectorLabel':'Thématique CRDPFF',
    'waitMessage': 'Chargement des données...',
    'mapContainerTab':'Carte',
    'legalBasisTab':'Bases légales',
    'layerTreeTitle':'Arbre des couches',
    'selectAllLayerLabel':'Restrictions',
    'lawTabLabel':'Dispositions juridiques',
    'additionnalInfoTab':'Informations et renvois supplémentaires',
    'infoTabLabel':'Informations',
    'legendPanelTitle':'Légende',
    'searchBoxEmptyTxt':'Rechercher...',
    'olCoordinates':'Coordonnées',
    'restrictionPanelTitle':'Restrictions',
    'restrictionPanelTxt':'Restrictions affectant la parcelle n° ',
    'noActiveLayertxt':'Aucune couche active',
    'restrictionFoundTxt':'Restriction n° ',
    'disclaimerTxt':'Mise en garde : Le canton de Neuchâtel n\'engage pas sa responsabilité sur l\'exactitude ou la fiabilité des documents législatifs dans leur version électronique. <br>Ces documents ne créent aucun autre droit ou obligation que ceux qui découlent des textes légalement adoptés et publiés, qui font seuls foi.',
    'mapBottomTxt':'<b>Informations dépourvues de foi publique, <a style="color:#660000;" href="http://sitn.ne.ch/web/conditions_utilisation/contrat_SITN_MO.htm" target="_new">&copy; SITN</a></b>',
    'maxTitleOverviewMap':'Afficher la carte de situation',
    'minTitleOverviewMap':'Masquer la carte de situation',
    'intersectToolTipMessage':'Relation spatiale: intersection',
    'withinToolTipMessage':'Relation spatiale: à l\'intérieur de',
    'adjacentToolTipMessage':'Relation spatiale: touche',
    'printPdfWindowsTitle': 'Extraction au format pdf',
    'noSelectedParcelMessage': 'Sélectionnez d\'abord une parcelle !',
    'printButtonTlp':'Générer l\'extrait',
    'infoButtonTlp':'Interroger les restrictions',
    'panButtonTlp':'Déplacement de la carte',
    'zoomInButtonTlp':'Zoom avant',
    'zoomOutButtonTlp':'Zoom arrière',
    'infoButtonTlp': 'Effacer la sélection actuelle',
    'baseLayerGroup': 'Fonds de plan',
    'chooseExtractMsg': 'Quel type d\'extrait souhaitez-vous imprimer ?',
    'chooseExtractMsgTitle': 'Choix du type d\'extrait',
    'reducedExtract': 'Extrait réduit',
    'extendedExtract': 'Extrait complet',
    'cancelExtract': 'Annuler'
    };
   

OpenLayers.Util.extend(OpenLayers.Lang.fr, {
    'adresses_sitn':'Adresses',
    'axe_rue':'Axes et rues',
    'nom_local_lieu_dit':'Noms locaux et lieux-dits',
    'search_arrets_tp':'Arrêts transports publics',
    'search_cours_eau':'Cours d\'eau',
    'search_axes_rtes':'Routes et axes',
    'search_satac':'N° SATAC',
    'search_uap_publique':'Unité d\'aménagement publique',
    'search_fo_administrations':'Administrations forestières',
    'ImmeublesCanton':'Biens-fonds',
    'ImmeublesCantonHistorique':'Biens-fonds historiques',
    'batiments_ofs':'Bâtiments regBL et n° egid',
    'point_interet':'Points d\'intérêt'
});