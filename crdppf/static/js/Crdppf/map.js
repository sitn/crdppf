/*
 * @include OpenLayers/Projection.js
 * @include OpenLayers/Map.js
 * @requires Crdppf/resources/themesFr.js 
 * @requires OpenLayers/Request.js 
 * @requires OpenLayers/Layer/WMTS.js 
 * @requires OpenLayers/Control/LayerSwitcher.js
 * @requires OpenLayers/Control/PanZoomBar.js
 * @requires OpenLayers/Control/GetFeature.js
 * @requires OpenLayers/Util.js 
 * @requires OpenLayers/Control/Navigation.js
 * @include OpenLayers/Layer/WMS.js
 * @include OpenLayers/Layer/Vector.js
 * @include OpenLayers/Format/GML.js
 * @include OpenLayers/Format/GeoJSON.js
 * @include OpenLayers/Renderer/Canvas.js
 * @include OpenLayers/Renderer/Elements.js
 * @include OpenLayers/Renderer/SVG.js
 * @include OpenLayers/Renderer/VML.js
 * @include OpenLayers/Protocol/WFS/v1_0_0.js
 * @include OpenLayers/Protocol/WFS.js
 */

 /*
 Ext.getCmp('mon_id')
 */
 
Ext.namespace('Crdppf');
OpenLayers.ImgPath = OLImgPath;  

// Constructor
Crdppf.Map = function Map(mapOptions) {
    this.title = 'Crdppf OpenLayers custom map object';
    this.description = 'Manages all cartographic parameters and actions';       
    this.map = makeMap(mapOptions);
    this.setOverlays = setOverlays;
    this.removeOverlays = removeOverlays;
    this.layerList;
    this.setInfoControl = setInfoControl;
    this.disableInfoControl = disableInfoControl;
}

var removeOverlays = function(idTheme){
 
}
var disableInfoControl = function disableInfoControl(){ 
    root.removeAll(true);
    var selectionLayer = this.map.getLayer('selectionLayer');
    selectionLayer.removeAllFeatures();
    infoControl = this.map.getControl('infoControl001');
    if(infoControl){
        infoControl.destroy();
    }
}
var setInfoControl = function setInfoControl(){
    root.removeAll(true);
    OpenLayers.ProxyHost= Crdppf.ogcproxyUrl;
    var protocol = new OpenLayers.Protocol.WFS({
    url: Crdppf.ogcproxyUrl,
    geometryName: this.geometryName,
    srsName: this.map.getProjection(),
    formatOptions: {
        featureType: 'parcelles',
        featureNS: 'http://mapserver.gis.umn.edu/mapserver',
        autoconfig: false
    }
    });
    control = new OpenLayers.Control.GetFeature({
        protocol: protocol,
        id: 'infoControl001',
        box: true,
        hover: false,
        single: true,
        maxFeatures: 1,
        clickTolerance: 10
        // multipleKey: "shiftKey",
        // toggleKey: "ctrlKey"
    });
    control.events.register("featureselected", this, function(e) {
        select.addFeatures([e.feature]); 
        var attributes = e.feature.attributes;
        keys = Object.keys(attributes);
        child =  new Ext.tree.TreeNode({
            text: 'parcelle : ' + e.feature.attributes.nummai,
            draggable:false,
            id:'idChild',
            leaf: false,
        })
        var html = '';
        for (i=1; i < keys.length - 1; i++){
            html += keys[i] + ' : ' + e.feature.attributes[keys[i]] + '<br>';
        }
        subchild =  new Ext.tree.TreeNode({
            text: html,
            draggable:false,
            id:'idSubChild',
            leaf: true
        })
        child.appendChild(subchild);
        root.appendChild(child);        
    });
    control.events.register("featureunselected", this, function(e) {
        select.removeFeatures([e.feature]);
        root.removeAll(true);
    });
    control.events.register("hoverfeature", this, function(e) {
        hover.addFeatures([e.feature]);
    });
    control.events.register("outfeature", this, function(e) {
        hover.removeFeatures([e.feature]);
    });
    this.map.addControl(control);
    control.activate();
    
    
  
}

// Create OL map object, add base layer & zoom to max extent
function makeMap(mapOptions){
    var layer = new OpenLayers.Layer.WMTS({
        name: "Plan cadastral",
        url: 'http://sitn.ne.ch/mapproxy/wmts',
        layer: 'plan_cadastral_c2c',
        matrixSet: 'swiss_grid_new',
        format: 'image/png',
        isBaseLayer: true,
        style: 'default',
        fixedLayer: true,
        requestEncoding: 'REST'
    });
    select = new OpenLayers.Layer.Vector(
        "Selection",
        {
            styleMap: new OpenLayers.Style(OpenLayers.Feature.Vector.style["select"]),
            fixedLayer: true, 
            displayInLayerSwitcher: false,
        });
    select.id = 'selectionLayer';
    var map = new OpenLayers.Map({
        projection: new OpenLayers.Projection('EPSG:21781'),
        resolutions: [250, 100, 50, 20, 10, 5, 2.5, 2, 1.5, 1, 0.5, 0.25, 0.125, 0.0625],
        units: 'm',
        theme: null,
        maxExtent: new OpenLayers.Bounds(420000.0, 30000.0, 900000.0, 360000.0),
        restrictedExtent: new OpenLayers.Bounds(515000,180000,580000,230000),
        controls: [
            new OpenLayers.Control.PanZoomBar({
                slideFactor: 300,
                zoomWorldIcon: true,
                panIcons: false
            }),
            new OpenLayers.Control.Navigation()   
        ]
    });
    map.events.register("mousemove", map, function(e) {
                var pixel = new OpenLayers.Pixel(e.xy.x,e.xy.y);
                var lonlat = map.getLonLatFromPixel(pixel);
                OpenLayers.Util.getElement(mapOptions.divMousePosition).innerHTML = 'Coordonnées (ch1903) - Y : ' + Math.round(lonlat.lon) + '  X : ' + Math.round(lonlat.lat) + 'm';
    });
    map.addLayers([layer,select]);
    var ls= new OpenLayers.Control.LayerSwitcher(); 
    map.addControl(ls); 
    ls.minimizeControl(); 
    map.zoomToMaxExtent();      
    return map;
}

/**
* Method: setOverlays
* Set the layers to be added to the map depending on the crdppf thematic selected
*
* Parameters:
* idTheme - {String} Unique ID of the selected theme
*/ 
var setOverlays = function(idTheme) {
        if(!this.map){
            console.log('error: undefined map object. Use Crdppf.createMap first');
            return;
        }
        // remove existing infoControl
        infoControl = this.map.getControl('infoControl001');
        if(infoControl){
            infoControl.destroy();
        }
        // empty selection layer
        var selectionLayer = this.map.getLayer('selectionLayer');
        selectionLayer.removeAllFeatures();
        // remove existing overlays
        for (var i = this.map.layers.length - 1; i >= 0; i--) {
            if(this.map.layers[i].fixedLayer == false){
                this.map.removeLayer(this.map.layers[i]);
            }
        }
        // add new overlays
        var layerObject = {};
        var layerName = '';
        var layerList = [];
        // for (var lKey in Crdppf.layerListFr[idTheme]){
            // layerName = Crdppf.layerListFr[idTheme][lKey];
            // layerObject[lKey] = new OpenLayers.Layer.WMS(
                // layerName, 
                // Crdppf.wmsUrl,
                // {layers: lKey,
                // format: 'image/png',
                // singleTile: true,
                // transparent: 'true'},
                // {fixedLayer: false}
                // );
            // this.map.addLayer(layerObject[lKey]);
            // layerList.push(lKey);
        // }
        for (var lKey in Crdppf.layerListFr[idTheme]){
            layerList.push(lKey);
        }
            layerName = 'Thèmes',
            layerObject[lKey] = new OpenLayers.Layer.WMS(
                layerName, 
                Crdppf.wmsUrl,
                {layers: layerList,
                format: 'image/png',
                singleTile: true,
                transparent: 'true'},
                {fixedLayer: false,
                singleTile: true}
                );
        this.map.addLayer(layerObject[lKey]);
        this.layerList = layerList;
        // toggle pan button
        var panButton= Ext.getCmp('panButton');
        panButton.toggle();
    }
    
    