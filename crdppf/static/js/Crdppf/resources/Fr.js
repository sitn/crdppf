Ext.namespace('Crdppf');

// Themes structure and content definition
Crdppf.layerListFr = {
    "type": "ThemesCollection",
        'themes' :[  
                        {'id':'73','image':'amenagement.gif','name':'Plans d\'affectation', 'layers':{'r73_affectations_primaires':'Zones d\'affectation primaire','r73_zones_superposees':'Zones d\'affectation superposées','r73_perimetres_superposes':'Périmètres superposées','r73_contenus_lineaires':'Restrictions linéaires','r73_contenus_ponctuels':'Restrictions ponctuelles'}},
                        {'id':'88','image':'routes_nationales.gif','name':'Routes nationales','layers':{}},
                        {'id':'96','image':'chemin_fer.gif','name':'Chemin de fer','layers':{}},
                        {'id':'108','image':'aeroports.gif','name':'Aéroports', 'layers':{'r103_bazl_projektierungszonen_flughafenanlagen':'Zones réservées des installations aéroportuaires','r108_bazl_sicherheitszonenplan':'Zones de sécurité des aéroports'}},
                        {'id':'116','image':'sites_pollues.gif','name':'Cadastre des sites pollués','layers':{'r116_sites_pollues':'Sites polluées'}},
                        {'id':'997','image':'protection_eaux.gif','name':'Protection des eaux','layers':{'r131_zone_prot_eau':'Zones de protection des eaux','r132_perimetre_prot_eau':'Périmètres de protection des eaux'}},
                        {'id':'996','image':'bruit.gif','name':'Bruit','layers':{'r145_sens_bruit':'Degrés de sensibilité au bruit'}},
                        {'id':'999','image':'foret.gif','name':'Forêts','layers':{'r157_lim_foret':'Limites légales de la forêt','r159_dist_foret':'Distances légales à la forêt'}}
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
    'legalBasisTab':'Documents légaux',
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
    'chooseExtractTypeMsg': 'Choix du type d\'extrait',
    'reducedExtract': 'Extrait réduit',
    'extendedExtract': 'Extrait complet',
    'cancelExtract': 'Annuler',
    'generateExtract': 'Générer l\'extrait',
    'restrictionLoadingMsg': 'Calcul...',
    'measureToolTxt': 'Mesure',
    'measureToolDistanceTxt': 'Distance',
    'measureToolSurfaceTxt': 'Surface'
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