Ext.namespace('Crdppf');

Crdppf.MeasureTool = function createMeasureTool () {
    this.makeMeasureTool = makeMeasureTool;
    this.toggleMeasureControl = toggleMeasureControl;
    this.disableMeasureControl = disableMeasureControl;
};

var makeMeasureTool = function makeMeasureTool(){
                
            // style the sketch fancy
            var sketchSymbolizers = {
                "Point": {
                    pointRadius: 4,
                    graphicName: "square",
                    fillColor: "white",
                    fillOpacity: 1,
                    strokeWidth: 1,
                    strokeOpacity: 1,
                    strokeColor: "#333333"
                },
                "Line": {
                    strokeWidth: 3,
                    strokeOpacity: 1,
                    strokeColor: "#666666",
                    strokeDashstyle: "dash"
                },
                "Polygon": {
                    strokeWidth: 2,
                    strokeOpacity: 1,
                    strokeColor: "#666666",
                    fillColor: "white",
                    fillOpacity: 0.3
                }
            };
            var style = new OpenLayers.Style();
            style.addRules([
                new OpenLayers.Rule({symbolizer: sketchSymbolizers})
            ]);
            var styleMap = new OpenLayers.StyleMap({"default": style});
            
            // allow testing of specific renderers via "?renderer=Canvas", etc
            var renderer = OpenLayers.Util.getParameters(window.location.href).renderer;
            renderer = (renderer) ? [renderer] : OpenLayers.Layer.Vector.prototype.renderers;

            measureControls = {
                line: new OpenLayers.Control.Measure(
                    OpenLayers.Handler.Path, {
                        persist: true,
                        handlerOptions: {
                            layerOptions: {
                                renderers: renderer,
                                styleMap: styleMap
                            }
                        }
                    }
                ),
                polygon: new OpenLayers.Control.Measure(
                    OpenLayers.Handler.Polygon, {
                        persist: true,
                        handlerOptions: {
                            layerOptions: {
                                renderers: renderer,
                                styleMap: styleMap
                            }
                        }
                    }
                )
            };
            
            var control;
            for(var key in measureControls) {
                control = measureControls[key];
                control.events.on({
                    "measure": handleMeasurements,
                    "measurepartial": handleMeasurements
                });
                MapO.map.addControl(control);
            }
        };

function handleMeasurements(event) {
    var geometry = event.geometry;
    var units = event.units;
    var order = event.order;
    var measure = event.measure;
    if (!Ext.getCmp('measureWindow')){
        createMeasureWindow();
    }
    var element = document.getElementById('measureOuput');
    var out = "";
    if(order == 1) {
        out += measure.toFixed(3) + " " + units;
    } else {
        out += measure.toFixed(3) + " " + units + "<sup>2</" + "sup>";
    }
    element.innerHTML = out;
}

var createMeasureWindow = function createMeasureWindow(){
    var measureWindow = new Ext.Window({
        title: 'Mesures',
        width: 100,
        height: 50,
        id: 'measureWindow',
        html: '<div id="measureOuput"></div>'
    });
    measureWindow.show();
}

var toggleMeasureControl = function toggleMeasureControl(type) {

    for(key in measureControls) {
        var control = measureControls[key];
        if(type == key) {
            control.activate();
            console.log('activated: ' + type);
        } else {
            control.deactivate();
            console.log('desactivated: ' + type);
        }
    }
};

var disableMeasureControl = function disableMeasureControl() {
    for(key in measureControls) {
        measureControls[key].deactivate();
    }
    Ext.getCmp('measureWindow').destroy();
}