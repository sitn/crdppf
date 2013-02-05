//definition of layers associated to themes

Ext.namespace('Crdppf');

Crdppf.layerListFr = {'0': {'at14_zones_communales':'Zones communales','at08_zones_cantonales':'Zones cantonales','at39_itineraires_pedestres':'Intinéraires pédestres','clo_couloirs':'Couloirs d\'obstacles aériens','clo_cotes_altitude_surfaces':'Côtes d\'altitude des surfaces','en07_canepo_accidents':'Sites polluées : accidents','en07_canepo_decharges':'Sites pollués : décharges','en07_canepo_decharges_points':'Sites pollués : décharges (points)','en07_canepo_decharges_polygones':'Sites pollués : décharges (polygones)', 'en07_canepo_entreprises':'Sites pollués : entreprises', 'en07_canepo_entreprises_points':'Sites pollués : entreprises (points)', 'en07_canepo_entreprises_polygones':'Sites pollués : entreprises (polygones)'},  
                        '73': {'at14_zones_communales':'Zones communales','at08_zones_cantonales':'Zones cantonales'},
                        '79': {'at39_itineraires_pedestres':'Intinéraires pédestres'},
                        '87': {},
                        '88': {},
                        '96': {},
                        '97': {},
                        '103':{},
                        '104':{},
                        '108':{'clo_couloirs':'Couloirs d\'obstacles aériens','clo_cotes_altitude_surfaces':'Cotes d\'altitude des surfaces'},
                        '116':{'en07_canepo_accidents':'Sites polluées : accidents','en07_canepo_decharges':'Sites pollués : décharges','en07_canepo_decharges_points':'Sites pollués : décharges (points)','en07_canepo_decharges_polygones':'Sites pollués : décharges (polygones)', 'en07_canepo_entreprises':'Sites pollués : entreprises', 'en07_canepo_entreprises_points':'Sites pollués : entreprises (points)', 'en07_canepo_entreprises_polygones':'Sites pollués : entreprises (polygones)'},
                        '117':{},
                        '118':{},
                        '119':{},
                        '131':{},
                        '132':{},
                        '145':{},
                        '74-NE':{},
                        '159':{},
                        '50-NE':{}
                        };
                        
Crdppf.layerTreeListFr = [{'text':'Chemin pour piétons','id':'79', 'leaf':false,'checked':false, children: [{ 'text':'Itinéraires pédestres','id':'at39_itineraires_pedestres','leaf':true, 'checked':false}]},
                          {'text':'Aménagement', 'id':'73', 'leaf':false,'checked':false, children: 
                              [{'text':'Zones communales','id':'at14_zones_communales','leaf':true,'checked':false},
                               {'text':'Zones cantonales', 'id':'at08_zones_cantonales', 'leaf': true,'checked':false}]},
                          {'text':'Cadastre des sites pollués', 'id':'116', 'leaf':false,'checked':false, children: 
                              [{'text':'Accidents','id':'en07_canepo_accidents','leaf':true,'checked':false},
                               {'text':'Sites pollués : décharges', 'id':'en07_canepo_decharges', 'leaf': true,'checked':false},
                               {'text':'Sites pollués : décharges (points)', 'id':'en07_canepo_decharges_points', 'leaf': true,'checked':false},
                               {'text':'Sites pollués : décharges (polygones)', 'id':'en07_canepo_decharges_polygones', 'leaf': true,'checked':false},
                               {'text':'Sites pollués : entreprises', 'id':'en07_canepo_entreprises', 'leaf': true,'checked':false},
                               {'text':'Sites pollués : entreprises (points)', 'id':'en07_canepo_entreprises_points', 'leaf': true,'checked':false},
                               {'text':'Sites pollués : entreprises (polygones)', 'id':'en07_canepo_entreprises_polygones', 'leaf': true,'checked':false}]}
                        ];