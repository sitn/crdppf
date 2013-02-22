//definition of layers associated to themes

Ext.namespace('Crdppf');

// Crdppf.layerListFrOld = [{  '0': {'at14_zones_communales':'Zones communales','at08_zones_cantonales':'Zones cantonales','at39_itineraires_pedestres':'Intinéraires pédestres','clo_couloirs':'Couloirs d\'obstacles aériens','clo_cotes_altitude_surfaces':'Côtes d\'altitude des surfaces','en07_canepo_accidents':'Sites polluées : accidents','en07_canepo_decharges':'Sites pollués : décharges','en07_canepo_decharges_points':'Sites pollués : décharges (points)','en07_canepo_decharges_polygones':'Sites pollués : décharges (polygones)', 'en07_canepo_entreprises':'Sites pollués : entreprises', 'en07_canepo_entreprises_points':'Sites pollués : entreprises (points)', 'en07_canepo_entreprises_polygones':'Sites pollués : entreprises (polygones)'},  
                        // '73': {'at14_zones_communales':'Zones communales','at08_zones_cantonales':'Zones cantonales'},
                        // '79': {'at39_itineraires_pedestres':'Intinéraires pédestres'},
                        // '87': {},
                        // '88': {},
                        // '96': {},
                        // '97': {},
                        // '103':{},
                        // '104':{},
                        // '108':{'clo_couloirs':'Couloirs d\'obstacles aériens','clo_cotes_altitude_surfaces':'Cotes d\'altitude des surfaces'},
                        // '116':{'en07_canepo_accidents':'Sites polluées : accidents','en07_canepo_decharges':'Sites pollués : décharges','en07_canepo_decharges_points':'Sites pollués : décharges (points)','en07_canepo_decharges_polygones':'Sites pollués : décharges (polygones)', 'en07_canepo_entreprises':'Sites pollués : entreprises', 'en07_canepo_entreprises_points':'Sites pollués : entreprises (points)', 'en07_canepo_entreprises_polygones':'Sites pollués : entreprises (polygones)'},
                        // '117':{},
                        // '118':{},
                        // '119':{},
                        // '131':{},
                        // '132':{},
                        // '145':{},
                        // '74-NE':{},
                        // '159':{},
                        // '50-NE':{}
                        // }];
// 'at14_zones_communales':'Zones communales','at08_zones_cantonales':'Zones cantonales',

Crdppf.layerListFr = {
    "type": "ThemesCollection", 
        'themes' :[     {'id':'0','name':'Itinéraires pédestres', 'layers':{'at39_itineraires_pedestres':'Intinéraires pédestres'}},
                        {'id':'73','name':'Zones Affectation', 'layers':{'at14_zones_communales':'Zones communales','at08_zones_cantonales':'Zones cantonales'}},
                        {'id':'108','name':'Carte et liste des obstacles à la navigation', 'layers':{'clo_couloirs':'Couloirs d\'obstacles aériens','clo_cotes_altitude_surfaces':'Cotes d\'altitude des surfaces'}},
                        {'id':'116','name':'Cadastre des sites pollués','layers':{'en07_canepo_accidents':'Sites polluées : accidents','en07_canepo_decharges':'Sites pollués : décharges','en07_canepo_decharges_points':'Sites pollués : décharges (points)','en07_canepo_decharges_polygones':'Sites pollués : décharges (polygones)', 'en07_canepo_entreprises':'Sites pollués : entreprises', 'en07_canepo_entreprises_points':'Sites pollués : entreprises (points)', 'en07_canepo_entreprises_polygones':'Sites pollués : entreprises (polygones)'}},
        ]
    }