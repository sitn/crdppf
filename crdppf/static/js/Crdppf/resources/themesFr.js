//definition of layers associated to themes

Ext.namespace('Crdppf');

Crdppf.layerListFr = {
    "type": "ThemesCollection",
        'themes' :[     {'id':'0','image':'osm.png','name':'Itinéraires pédestres', 'layers':{'at39_itineraires_pedestres':'Itinéraires pédestres'}},
                        {'id':'73','image':'amenagement.png','name':'Zones Affectation', 'layers':{'at14_zones_communales':'Zones communales','at08_zones_cantonales':'Zones cantonales'}},
                        {'id':'108','image':'trafic.png','name':'Carte et liste des obstacles à la navigation', 'layers':{'clo_couloirs':'Couloirs d\'obstacles aériens','clo_cotes_altitude_surfaces':'Cotes d\'altitude des surfaces'}},
                        {'id':'116','image':'sitespollues.png','name':'Cadastre des sites pollués','layers':{'en07_canepo_accidents':'Sites polluées : accidents','en07_canepo_decharges':'Sites pollués : décharges','en07_canepo_decharges_points':'Sites pollués : décharges (points)','en07_canepo_decharges_polygones':'Sites pollués : décharges (polygones)', 'en07_canepo_entreprises':'Sites pollués : entreprises', 'en07_canepo_entreprises_points':'Sites pollués : entreprises (points)', 'en07_canepo_entreprises_polygones':'Sites pollués : entreprises (polygones)'}},
        ]
    }