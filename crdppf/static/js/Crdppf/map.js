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
    // avoid doubling infoControls
    MapO.disableInfoControl();
    
    // remove all 
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
                leaf: false,
                expanded: true,
                id: guid(),

            })
            subchild =  new Ext.tree.TreeNode({
                text: 'Aucune couche active !',
                draggable:false,
                id:guid(),
                leaf: true
            })
            child.appendChild(subchild);
            root.appendChild(child); 
        }
        else { // send intersection request and process results
                function handler(request) {
                var geojson_format = new OpenLayers.Format.GeoJSON();
                var jsonData = geojson_format.read(request.responseText);
                var child =  new Ext.tree.TreeNode({
                    text: 'parcelle n° ' + parcelId,
                    draggable:false,
                    leaf: false,
                    expanded: true
                })
                lList = [];
                // iterate over the features
                for (i=0; i<jsonData.length; i++) {
                    lName = jsonData[i].attributes['layerName'];
                    // create child for layer if not already created
                    if(!contains(lName,lList)){
                        var fullName = '';
                        var ll = Crdppf.layerListFr.themes;
                        for (l=0;l<ll.length;l++){
                            for (key in ll[l].layers){
                                if(lName==key){
                                    fullName = ll[l].layers[key]; 
                                }
                            }
                        }
                        
                        var layerChild =  new Ext.tree.TreeNode({
                            text: fullName,
                            draggable:false,
                            id:guid(),
                            leaf: false,
                            expanded: false
                        })
                        // iterate over all features
                        for (j=0; j<jsonData.length; j++) {
                            if(jsonData[j].attributes['layerName']==lName){
                                html = '';
                                for (value in jsonData[j].attributes){
                                    html += '' + value + ' : ' + jsonData[j].attributes[value] +'<br>' ;
                                }
                                html += '';
                                var sameLayerNode = new Ext.tree.TreeNode({
                                    attributes: jsonData[j],
                                    text: 'Restriction n°' + j,
                                    draggable:false,
                                    leaf: false,
                                    expanded: false,
                                    id: guid(),
                                    listeners: {
                                        'click': function(node,e) {
                                            intersect.removeAllFeatures();
                                            feature = node.attributes.attributes;
                                            intersect.addFeatures(feature);
                                            MapO.map.zoomToExtent(feature.geometry.bounds);
                                        }
                                    }
                                })
                                // sameLayerNode.addEvents(Ext.Element.mouseover);
                                //sameLayerNode.on('mouseover':this.onMouseOver)
                                var contentNode = new Ext.tree.TreeNode({
                                    text: html,
                                    draggable:false,
                                    leaf: false,
                                    expanded: false,
                                    id: guid()
                                })
                                sameLayerNode.appendChild(contentNode);
                                layerChild.appendChild(sameLayerNode);
                            }
                        }
                        child.appendChild(layerChild);
                        root.appendChild(child);
                        lList.push(lName);
                    }
                }               
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

var contains = function contains(element,list){
        for (item in list) {
            if(list[item]==element){
                return true
            }
        }
    return false;
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
            'fillOpacity': '0.5',
            'fillColor': '#ff0000',
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
    map.addLayers([intersect,select, layer]);
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

// helping functions
function s4() {
  return Math.floor((1 + Math.random()) * 0x10000)
             .toString(16)
             .substring(1);
};

function guid() {
  return s4() + s4() + '-' + s4() + '-' + s4() + '-' +
         s4() + '-' + s4() + s4() + s4();
}
    