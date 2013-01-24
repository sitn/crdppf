/*
 * @requires Crdppf/ressources/themesFr.js
 */

Ext.namespace('Crdppf');

/**
 * Constructor: Crdppf.Map
 * Creates a panel with an Openlayer.map object
 * a {GeoExt.MapPanel} in the center region
 *
 * Parameters:
 * options - {Object} Options to be passed to the main panel.
 */
 
Crdppf.Map = function(){
    var map;
    var malist = Crdppf.layerListFr;
    
   /**
     * Method: createMap
     * Create the OpenLayers map object
    */   
     var createMap = function() {
     // parameters will be hard-coded
        map = new OpenLayers.Map({
        projection: new OpenLayers.Projection("EPSG:21781"),
        units: "m",
        theme: null,
        resolutions: [250,100,50,20,10,5,2.5,2,1.5,1,0.5,0.25,0.125,0.0625],
        maxExtent: new OpenLayers.Bounds(515000, 180000, 580000, 230000),
        restrictedExtent: new OpenLayers.Bounds(420000,30000,900000,360000),
        center: new OpenLayers.LonLat(550000, 204000),
        controls: [
            new OpenLayers.Control.PanZoomBar({
                slideFactor: 300,
                zoomWorldIcon: true
            }),
            new OpenLayers.Control.Navigation(),
            new OpenLayers.Control.LayerSwitcher()
        ]
        });
        addBaseLayers();
     }
     /**
     * Method: addBaseLayers
     * Add the base layers
    *
    * Parameters:
    * none
    */   
    var addBaseLayers = function() {
        // check if map object is defined
        if(!map){
            alert('undefined map object. Use Crdppf.createMap first');
            return;
        }
        
        // wmts layers
        var wmts_url = "http://sitn.ne.ch/mapproxy/wmts/";

        var plan_ville = new OpenLayers.Layer.WMTS({
        name: "Plan de ville",
        url: wmts_url,
        layer: 'plan_ville_20121228',
        matrixSet: 'swiss_grid_new',
        format: 'image/png',
        isBaseLayer: true,
        style: "default",
        requestEncoding: 'REST',
        serverResolutions:[250, 100, 50, 20, 10, 5, 2.5, 2, 1.5, 1, 0.5 ,0.25, 0.125, 0.0625],
        });
        
        // wms layers
        var ortho = new OpenLayers.Layer.WMS(
            'Ortho SITN',
            'http://sitn.ne.ch/ogc-sitn-open/wms',
            {layers: 'ortho'}
        );
        map.addLayers([ortho]);   
     }
      createMap();  
    /**
     * Method: setOverlays
     * Set the layers to be added to the map depending on the crdppf thematic selected
    *
    * Parameters:
    * idTheme - {String} Unique ID of the selected theme
    */   
    var setOverlays = function(idTheme) {
        wmsURL = 'http://sitn.ne.ch/ogc-sitn-open/wms';
        // check if map object is defined
        if(!map){
            alert('undefined map object. Use Crdppf.createMap first');
            return;
        }
        // remove all layer from map
        for (var i = map.layers.length - 1; i >= 0; i--) {
            map.removeLayer(map.layers[i]);
        }
         // define overlays - assumed: wms layers
        var layerObject = {};
        console.log(layerListFr);
        var layerId = '';
        var layerName = '';
        for (var lKey in layerListFr[idTheme]){
            layerId = lKey;
            layerName = layerListFr[idTheme][lKey];
            layerObject[layerId] = new OpenLayers.Layer.WMS(layerName, wmsURL,{layers: layerId});
            console.log(layerObject[layerId]);
            map.addLayer(layerObject[layerId]);
        }        
     }
}

Crdppf.Map();