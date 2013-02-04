/*
 * @requires Crdppf/resources/themesFr.js
 */

Ext.namespace('Crdppf');

// test svn olivier

/**
 * Constructor: Crdppf.Map
 * Creates a panel with an Openlayer.map object
 * a {GeoExt.MapPanel} in the center region
 *
 * Parameters:
 * options - {Object} Options to be passed to the main panel.
 */
var mapOptions = {
        projection: new OpenLayers.Projection('EPSG:21781'),
        resolutions: [250, 100, 50, 20, 10, 5, 2.5, 2, 1.5, 1, 0.5, 0.25, 0.125, 0.0625],
        units: 'm',
        maxExtent: new OpenLayers.Bounds(420000.0, 30000.0, 900000.0, 360000.0)
    };
Crdppf.map = new OpenLayers.Map(mapOptions);
var layer = new OpenLayers.Layer.WMTS({
            name: "WMTS plan_cadastral_c2c",
            url: 'http://sitn.ne.ch/mapproxy/wmts',
            layer: 'plan_cadastral_c2c',
            matrixSet: 'swiss_grid_new',
            format: 'image/png',
            isBaseLayer: true,
            style: 'default',
            requestEncoding: 'REST'
        });
Crdppf.map.addLayer(layer);
 var ls= new OpenLayers.Control.LayerSwitcher(); 
 Crdppf.map.addControl(ls); 
 ls.maximizeControl(); 
Crdppf.map.zoomToMaxExtent();
    /**
     * Method: setOverlays
     * Set the layers to be added to the map depending on the crdppf thematic selected
    *
    * Parameters:
    * idTheme - {String} Unique ID of the selected theme
    */   
Crdppf.setOverlays = function(idTheme) {
    wmsURL = 'http://sitn.ne.ch/ogc-sitn-poi/wms';
    // check if map object is defined
    if(!Crdppf.map){
        alert('undefined map object. Use Crdppf.createMap first');
        return;
    }
    // remove all layer from map that are not base layers
    for (var i = Crdppf.map.layers.length - 1; i >= 0; i--) {
        if(Crdppf.map.layers.isBaseLayer == false){
            Crdppf.map.removeLayer(Crdppf.map.layers[i]);
        }
    }
    // define overlays - assumed: wms layers
    var layerObject = {};
    var layerId = '';
    var layerName = '';
    for (var lKey in Crdppf.layerListFr[idTheme]){
        layerId = lKey;
        layerName = Crdppf.layerListFr[idTheme][lKey];
        layerObject[layerId] = new OpenLayers.Layer.WMS(
            layerName, 
            wmsURL,
            {layers: layerId,
            format: 'image/png',
            transparent: 'true'}
            );
        console.log(layerObject[layerId]);
        Crdppf.map.addLayer(layerObject[layerId]);
    }        
 }