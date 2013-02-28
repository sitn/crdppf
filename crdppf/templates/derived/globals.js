if(!window.Crdppf) Crdppf = {};

Crdppf.baseUrl = "${request.route_url('home')}";
Crdppf.imagesDir = "${request.route_url('images')}";
Crdppf.wmsUrl = "${request.registry.settings['crdppf_wms']}";
Crdppf.getFeatureUrl = "${request.route_url('get_features')}";
Crdppf.ogcproxyUrl = "${request.route_url('ogcproxy')}";

