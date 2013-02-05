if(!window.Crdppf) Crdppf = {};

Crdppf.baseUrl = "${request.route_url('home')}";
Crdppf.wmsUrl = "${request.registry.settings['crdppf_wms']}";
Crdppf.ogcproxyUrl = "${request.route_url('ogcproxy')}";

