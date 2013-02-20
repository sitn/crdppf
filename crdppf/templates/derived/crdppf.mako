<%inherit file="/base/index.mako"/>

    <script type="text/javascript">
        var OLImgPath = "${request.static_url('crdppf:static/images/ol/')}";
    </script>

% if debug:
    <!-- GENERAL LIBRARIES -->
    <script type="text/javascript" src="${request.static_url('crdppf:static/lib/openlayers/lib/OpenLayers.js')}"></script>
    <script type="text/javascript" src="${request.static_url('crdppf:static/lib/openlayers/lib/Openlayers/Lang/fr.js')}"></script>
    <script type="text/javascript" src="${request.static_url('crdppf:static/lib/geoext/lib/GeoExt.js')}"></script>
    <script type="text/javascript" src="${request.static_url('crdppf:static/lib/ext/resources/ux/statusbar/StatusBar.js')}"></script>
    
    <!-- CUSTOM CRDPPF STUFF -->
    <script type="text/javascript" src="${request.static_url('crdppf:static/js/Crdppf/resources/themesFr.js')}"></script>
    <script type="text/javascript" src="${request.static_url('crdppf:static/js/Crdppf/map.js')}"></script>
    <script type="text/javascript" src="${request.static_url('crdppf:static/js/Crdppf/layerTree.js')}"></script>
    <script type="text/javascript" src="${request.static_url('crdppf:static/js/Crdppf/main.js')}"></script>
    <script type="text/javascript" src="${request.static_url('crdppf:static/js/Crdppf/searcher/searcher.js')}"></script>
    <script type="text/javascript" src="${request.static_url('crdppf:static/js/Crdppf/searcher/GroupComboBox.js')}"></script>
    <script type="text/javascript" src="${request.static_url('crdppf:static/js/Crdppf/searcher/GroupingView.js')}"></script>
% else:
    <script type="text/javascript" src="${request.static_url('crdppf:static/build/crdppf.js')}"></script>
% endif

    
    
<div id="main"></div>
