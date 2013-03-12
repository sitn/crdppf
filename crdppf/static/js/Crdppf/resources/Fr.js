Ext.namespace('Crdppf');

// Themes structure and content definition
Crdppf.layerListFr = {
    "type": "ThemesCollection",
        'themes' :[  
                        {'id':'73','image':'amenagement.gif','name':'Zones Affectation', 'layers':{'at14_zones_communales':'Zones communales','at08_zones_cantonales':'Zones cantonales','at39_itineraires_pedestres':'Itinéraires pédestres', 'at28_limites_constructions':'Limites constructions'}},
                        {'id':'108','image':'aeroports.gif','name':'Aéroports', 'layers':{'clo_couloirs':'Couloirs d\'obstacles aériens','clo_cotes_altitude_surfaces':'Cotes d\'altitude des surfaces'}},
                        {'id':'116','image':'sites_pollues.gif','name':'Cadastre des sites pollués','layers':{'en07_canepo_accidents':'Sites polluées : accidents','en07_canepo_decharges':'Sites pollués : décharges','en07_canepo_decharges_points':'Sites pollués : décharges (points)','en07_canepo_decharges_polygones':'Sites pollués : décharges (polygones)', 'en07_canepo_entreprises':'Sites pollués : entreprises', 'en07_canepo_entreprises_points':'Sites pollués : entreprises (points)', 'en07_canepo_entreprises_polygones':'Sites pollués : entreprises (polygones)'}},
                        {'id':'999','image':'foret.gif','name':'Forêts','layers':{'at39_itineraires_pedestres':'Itinéraires pédestres'}},
                        {'id':'998','image':'routes_nationales.gif','name':'Routes nationales','layers':{'at39_itineraires_pedestres':'Itinéraires pédestres'}},                        
                        {'id':'997','image':'protection_eaux.gif','name':'Protection des eaux','layers':{'en01_zone_sect_protection_eaux':'Secteurs de protection des eaux'}},
                        {'id':'996','image':'bruit.gif','name':'Bruit','layers':{'en05_degres_sensibilite_bruit':'Degrés de sensibilité au bruit'}}
        ]
    };
    
// Application labels text values for french  
Crdppf.labelsFr  ={
    'navPanelLabel':'Navigation',
    'searchBoxTxt':'Rechercher...',
    'themeSelectorLabel':'Sélection des thèmes',
    'mapContainerTab':'Carte',
    'legalBasisTab':'Bases légales',
    'layerTreeTitle':'Arbre des couches',
    'selectAllLayerLabel':'Sélectionner toutes les couches',
    'lawTabLabel':'Dispositions légales',
    'additionnalInfoTab':'Informations et renvois supplémentaires',
    'infoTabLabel':'Informations',
    'legendPanelTitle':'Légende',
    'searchBoxEmptyTxt':'Rechercher...',
    'olCoordinates':'Coordonnées',
    'restrictionPanelTitle':'Restrictions',
    'restrictionPanelTxt':'Restrictions affectant la parcelle n° ',
    'noActiveLayertxt':'Aucune couche active',
    'restrictionFoundTxt':'Restriction n° ',
    'disclaimerTxt':'Mise en garde : Le canton de Neuchâtel n\'engage pas sa responsabilité sur l\'exactitude ou la fiabilité des documents législatifs dans leur version électronique. Ces documents ne créent aucun autre droit ou obligation que ceux qui découlent des textes légalement adoptés et publiés, qui font seuls foi.',
    'mapBottomTxt':'<b>Informations dépourvues de foi publique, <a style="color:#660000;" href="http://sitn.ne.ch/web/conditions_utilisation/contrat_SITN_MO.htm" target="_new">&copy; SITN</a></b>',
    'maxTitleOverviewMap':'Afficher la carte de situation',
    'minTitleOverviewMap':'Masquer la carte de situation',
    'intersectToolTipMessage':'Relation spatiale: intersection',
    'withinToolTipMessage':'Relation spatiale: à l\'intérieur de',
    'adjacentToolTipMessage':'Relation spatiale: touche',
    };