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
// Disable the existing infoControls
var disableInfoControl = function disableInfoControl(){ 
    root.removeAll(true);
    var selectionLayer = this.map.getLayer('selectionLayer');
    selectionLayer.removeAllFeatures();
    infoControl = this.map.getControl('infoControl001');
    if(infoControl){
        infoControl.destroy();
    }
}
// Create the infocontrols supporting the getFeatureInfo functionnalities
var setInfoControl = function setInfoControl(){
    root.removeAll(true);
    OpenLayers.ProxyHost= Crdppf.ogcproxyUrl;
    var protocol = new OpenLayers.Protocol.WFS({
        url: Crdppf.ogcproxyUrl,
        geometryName: this.geometryName,
        srsName: this.map.getProjection(),
            featureType: 'parcelles',
        formatOptions: {
            featureNS: 'http://mapserver.gis.umn.edu/mapserver',
            autoconfig: false
        }
    });
    control = new OpenLayers.Control.GetFeature({
        protocol: protocol,
        id: 'infoControl001',
        box: false,
        hover: false,
        single: false,
        maxFeatures: 1,
        clickTolerance: 10
    });
    control.events.register("featureselected", this, function(e) {
        select.addFeatures([e.feature]); 
        var parcelId = e.feature.attributes.idemai;
        if(overlaysList.length == 0){
            child =  new Ext.tree.TreeNode({
                text: 'parcelle n° ' + parcelId,
                draggable:false,
                leaf: false
            })
            subchild =  new Ext.tree.TreeNode({
                text: 'Aucune couche active !',
                draggable:false,
                id:'idSubChild',
                leaf: true
            })
            child.appendChild(subchild);
            root.appendChild(child); 
        }
        else {
            function handler(request) {
                console.log(request)
               var geojson_format = new OpenLayers.Format.GeoJSON();
               var intersectionLayer = this.MapO.map.getLayer('intersectLayer');
               intersectionLayer.removeAllFeatures();
               jsonData = geojson_format.read(request.responseText);
               intersectionLayer.addFeatures(jsonData);
               // for (features in jsonData) {
                    // child =  new Ext.tree.TreeNode({
                        // text: 'parcelle n° ' + e.feature.attributes.idemai,
                        // draggable:false,
                        // id: e.feature.id,
                        // leaf: false,
                    // });
               // }
               
            }
            var request = OpenLayers.Request.GET({
                url: Crdppf.getFeatureUrl,
                params: {
                    id: parcelId,
                    layerList: overlaysList
                },
                callback: handler,
                proxy: null
            });
        }
        // var attributes = e.feature.attributes;
        // keys = Object.keys(attributes);
        // child =  new Ext.tree.TreeNode({
            // text: 'parcelle n° ' + e.feature.attributes.nummai,
            // draggable:false,
            // id: e.feature.id,
            // leaf: false,
        // })
        // var html = '';
        // for (i=1; i < keys.length - 1; i++){
            // if(keys[i] != 'nummai')
            // {
                // html += keys[i] + ' : ' + e.feature.attributes[keys[i]] + '<br>';
            // }
        // }
        // subchild =  new Ext.tree.TreeNode({
            // text: html,
            // draggable:false,
            // id:'idSubChild',
            // leaf: true
        // })
        // child.appendChild(subchild);
        // root.appendChild(child);        
    });
    control.events.register("featureunselected", this, function(e) {
        select.removeFeatures([e.feature]);
        root.removeAll(true);
    });
    // control.events.register("hoverfeature", this, function(e) {
        // hover.addFeatures([e.feature]);
    // });
    // control.events.register("outfeature", this, function(e) {
        // hover.removeFeatures([e.feature]);
    // });
    this.map.addControl(control);
    control.activate();
}

// Create OL map object, add base layer & zoom to max extent
function makeMap(mapOptions){
    // base layer: topographic layer
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
    
    // selection layer: display selected features
    select = new OpenLayers.Layer.Vector(
        "Selection",
        {
            styleMap: new OpenLayers.Style(OpenLayers.Feature.Vector.style["select"]),
            fixedLayer: true, 
            displayInLayerSwitcher: false,
        });
        select.id = 'selectionLayer';
        var intersectStyle = new OpenLayers.Style({
            'strokeColor':'#ff0000',
            'fillOpacity': '0.0',
            'strokeWidth':'2',
            'pointRadius': '20'
            
        });
        intersect = new OpenLayers.Layer.Vector(
        "intersection result",
        {
            styleMap: intersectStyle,
            fixedLayer: true, 
            displayInLayerSwitcher: false,
        });
        intersect.id='intersectLayer';
    // THE OL map object
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
    // Event registering & Control setting on the Map Object
    map.events.register("mousemove", map, function(e) {
                var pixel = new OpenLayers.Pixel(e.xy.x,e.xy.y);
                var lonlat = map.getLonLatFromPixel(pixel);
                OpenLayers.Util.getElement(mapOptions.divMousePosition).innerHTML = 'Coordonnées (ch1903) - Y : ' + Math.round(lonlat.lon) + '  X : ' + Math.round(lonlat.lat) + 'm';
    });
    // add base layers & selection layers
    map.addLayers([layer,select, intersect]);
    // load all specifics layers
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
var setOverlays = function() {
    if(!this.map){
        console.log('error: undefined map object !');
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
    
    layerName = 'Themes'
    theLayer = this.map.getLayer('overlayLayer');
    if(theLayer){
        this.map.removeLayer(theLayer)
    }
    // add new overlays
    if(overlaysList.length > 0){
        overlays = new OpenLayers.Layer.WMS(
                layerName, 
                Crdppf.wmsUrl,
                {layers: overlaysList,
                format: 'image/png',
                singleTile: true,
                transparent: 'true'},
                {fixedLayer: false,
                singleTile: true}
                );
        overlays.id = 'overlayLayer';
        this.map.addLayer(overlays);
    }

    // toggle pan button
    var panButton= Ext.getCmp('panButton');
    panButton.toggle();
}

    
    