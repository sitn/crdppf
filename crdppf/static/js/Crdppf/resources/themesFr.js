//definition of layers associated to themes

Ext.namespace('Crdppf');

Crdppf.layerListFr = {
    "type": "ThemesCollection",
        'themes' :[  
                        {'id':'73','image':'amenagement.gif','name':'Zones Affectation', 'layers':{'at14_zones_communales':'Zones communales','at08_zones_cantonales':'Zones cantonales','at39_itineraires_pedestres':'Itinéraires pédestres'}},
                        {'id':'108','image':'aeroports.gif','name':'Carte et liste des obstacles à la navigation', 'layers':{'clo_couloirs':'Couloirs d\'obstacles aériens','clo_cotes_altitude_surfaces':'Cotes d\'altitude des surfaces'}},
                        {'id':'116','image':'sites_pollues.gif','name':'Cadastre des sites pollués','layers':{'en07_canepo_accidents':'Sites polluées : accidents','en07_canepo_decharges':'Sites pollués : décharges','en07_canepo_decharges_points':'Sites pollués : décharges (points)','en07_canepo_decharges_polygones':'Sites pollués : décharges (polygones)', 'en07_canepo_entreprises':'Sites pollués : entreprises', 'en07_canepo_entreprises_points':'Sites pollués : entreprises (points)', 'en07_canepo_entreprises_polygones':'Sites pollués : entreprises (polygones)'}},
                        {'id':'999','image':'foret.gif','name':'Forêts','layers':{'at39_itineraires_pedestres':'Itinéraires pédestres'}},
                        {'id':'998','image':'routes_nationales.gif','name':'Routes nationales','layers':{'at39_itineraires_pedestres':'Itinéraires pédestres'}},                        
                        {'id':'997','image':'protection_eaux.gif','name':'Protection des eaux','layers':{'at39_itineraires_pedestres':'Itinéraires pédestres'}},
                        {'id':'996','image':'bruit.gif','name':'Protection des eaux','layers':{'at39_itineraires_pedestres':'Itinéraires pédestres'}},
        ]
    }
Crdppf.layerListDe = {
    "type": "ThemesCollection",
        'themes' :[     {'id':'0','image':'osm.png','name':'Fusswege', 'layers':{'at39_itineraires_pedestres':'Fusswege'}},
                        {'id':'73','image':'amenagement.gif','name':'Zones Affectation', 'layers':{'at14_zones_communales':'Zones communales','at08_zones_cantonales':'Zones cantonales'}},
                        {'id':'108','image':'aeroports.gif','name':'Carte et liste des obstacles à la navigation aérienne', 'layers':{'clo_couloirs':'Couloirs d\'obstacles aériens','clo_cotes_altitude_surfaces':'Cotes d\'altitude des surfaces'}},
                        {'id':'116','image':'sites_pollues.gif','name':'Cadastre des sites pollués','layers':{'en07_canepo_accidents':'Sites polluées : accidents','en07_canepo_decharges':'Sites pollués : décharges','en07_canepo_decharges_points':'Sites pollués : décharges (points)','en07_canepo_decharges_polygones':'Sites pollués : décharges (polygones)', 'en07_canepo_entreprises':'Sites pollués : entreprises', 'en07_canepo_entreprises_points':'Sites pollués : entreprises (points)', 'en07_canepo_entreprises_polygones':'Sites pollués : entreprises (polygones)'}},
        ]
    }

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
    'mapBottomTxt':'<b>Informations dépourvues de foi publique, <a style="color:#660000;" href="http://sitn.ne.ch/web/conditions_utilisation/contrat_SITN_MO.htm" target="_new">&copy; SITN</a>, <a style="color:#660000;" href="http://sitn.ne.ch/web/conditions_utilisation/contratdv5741.htm" target="_new">swisstopo DV 571.4</a>, <a style="color:#660000;" href="http://www.openstreetmap.org/copyright" target="_new">OpenStreetMap</a></b>',
}
Crdppf.labelsDe  ={
    'navPanelLabel':'Navigation',
    'searchBoxTxt':'Suche...',
    'themeSelectorLabel':'Themenwahl',
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
    'mapBottomTxt':'<b>Daten sind nicht rechtsverbindlich, <a style="color:#660000;" href="http://sitn.ne.ch/web/conditions_utilisation/contrat_SITN_MO.htm" target="_new">&copy; SITN</a>, <a style="color:#660000;" href="http://sitn.ne.ch/web/conditions_utilisation/contratdv5741.htm" target="_new">swisstopo DV 571.4</a>, <a style="color:#660000;" href="http://www.openstreetmap.org/copyright" target="_new">OpenStreetMap</a></b>',


}

