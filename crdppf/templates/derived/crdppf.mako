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
    <script type="text/javascript" src="${request.static_url('crdppf:static/js/Crdppf/resources/Fr.js')}"></script>
    <script type="text/javascript" src="${request.static_url('crdppf:static/js/Crdppf/resources/De.js')}"></script>
    <script type="text/javascript" src="${request.static_url('crdppf:static/js/Crdppf/map.js')}"></script>
    <script type="text/javascript" src="${request.static_url('crdppf:static/js/Crdppf/layerTree.js')}"></script>
    <script type="text/javascript" src="${request.static_url('crdppf:static/js/Crdppf/themeSelector.js')}"></script>
    <script type="text/javascript" src="${request.static_url('crdppf:static/js/Crdppf/main.js')}"></script>
    <script type="text/javascript" src="${request.static_url('crdppf:static/js/Crdppf/searcher/searcher.js')}"></script>
    <script type="text/javascript" src="${request.static_url('crdppf:static/js/Crdppf/searcher/GroupComboBox.js')}"></script>
    <script type="text/javascript" src="${request.static_url('crdppf:static/js/Crdppf/searcher/GroupingView.js')}"></script>
    <script type="text/javascript" src="${request.static_url('crdppf:static/lib/openlayers.addins/lib/OpenLayers/Control/ScaleBar.js')}"></script>
% else:
    <script type="text/javascript" src="${request.static_url('crdppf:static/build/crdppf.js')}"></script>
% endif

    <script type="text/javascript">
        OpenLayers.Util.extend(OpenLayers.Lang.fr, {
            'plan_ville_${request.tile_date[1]}': 'Plan de ville',
            'plan_cadastral_${request.tile_date[0]}': 'Plan cadastral'
        });
    </script>
    
<div id="main"></div>
