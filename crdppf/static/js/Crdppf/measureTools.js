Ext.namespace('Crdppf');

Crdppf.MeasureTool = function(map, measureLabelBox) {

    // Write measurement to Ext Window html
    this.handleMeasurements = function(event) {
        var geometry = event.geometry;
        var units = event.units;
        var order = event.order;
        var measure = event.measure;
        var out = "";
        if(order == 1) {
            out += measure.toFixed(3) + " " + units;
        } else {
            out += measure.toFixed(3) + " " + units + "<sup>2</" + "sup>";
        }
        measureLabelBox.setText(out, false);
    };

    this.toggleMeasureControl = function toggleMeasureControl(type) {
        for(key in measureControls) {
            var control = measureControls[key];
            if(type == key) {
                control.activate();
            } else {
                control.deactivate();
            }
        }
    };

    this.makeMeasureTool = function makeMeasureTool(){
        // custom style
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

        var renderer = OpenLayers.Util.getParameters(window.location.href).renderer;
        renderer = (renderer) ? [renderer] : OpenLayers.Layer.Vector.prototype.renderers;

        // Define the controls
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
                "measure": this.handleMeasurements,
                "measurepartial": this.handleMeasurements
            });
            map.addControl(control);
        }
    };

    this.disableMeasureControl = function disableMeasureControl() {
        for(key in measureControls) {
            measureControls[key].deactivate();
        }
        measureLabelBox.setText('');
    };
};
