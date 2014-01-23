if(!window.Crdppf) Crdppf = {};

Crdppf.baseUrl = "${request.route_url('home')}";
Crdppf.imagesDir = "${request.route_url('images')}";  
Crdppf.getFeatureUrl = "${request.route_url('get_features')}";
Crdppf.setLanguageUrl = "${request.route_url('set_language')}";
Crdppf.getLanguageUrl = "${request.route_url('get_language')}";
Crdppf.getTranslationDictionaryUrl = "${request.route_url('get_translation_dictionary')}";
Crdppf.getInterfaceConfigUrl = "${request.route_url('get_interface_config')}";
Crdppf.getBaselayerConfigUrl = "${request.route_url('get_baselayers_config')}";
Crdppf.wmsUrl = "${request.route_url('ogcproxy')}";
Crdppf.ogcproxyUrl  = "${request.route_url('ogcproxy')}";
Crdppf.printUrl = "${request.route_url('create_extract')}";
Crdppf.fulltextsearchUrl = "${request.registry.settings['fulltextsearch_url']}";
Crdppf.mapproxyUrl = [${request.registry.settings['mapproxyurl']|n}];

Crdppf.tileNames = {
    'plan_ville_name': 'plan_ville_${request.tile_date[1]}',
    'plan_cadastral_name': 'plan_cadastral_${request.tile_date[0]}'
};
