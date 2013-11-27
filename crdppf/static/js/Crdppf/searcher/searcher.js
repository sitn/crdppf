/*
- * @requires GeoExt/data/FeatureStore.js
- * @requires GeoExt/data/FeatureReader.js
- * @include Crdppf/searcher/GroupComboBox.js
- * @include Crdppf/searcher/GroupingView.js
- */

Ext.namespace('Crdppf');

Crdppf.SearchBox = function(options) {

    var baseParams = {};

    if (options.map) {
        var map = options.map;
        delete options.map;
    }

    if (options.callback) {
        var callback = options.callback;
        baseParams.hasCb = true;
        delete options.callback;
    }
    if (options.div) {
        var el = options.div;
        delete options.div;
    }
    if (options.url) {
        var url = options.url;
        delete options.url;
    }

    // extending GroupingStore with FeatureStoreMixin to get grouping/sorting
    // with a featureStore
    var FeatureGroupingStore = Ext.extend(
        Ext.data.GroupingStore, new GeoExt.data.FeatureStoreMixin);

    var store = new FeatureGroupingStore({
        proxy: new Ext.data.ScriptTagProxy({
            url: url,
            callbackParam: 'callback'
        }),
        reader: new Crdppf.FeatureReader({
            format: new OpenLayers.Format.GeoJSON()
        }, [
            { name: 'layer_name' },
            { name: 'label' }
        ]),
        fields: ['layer_name', 'label'],
        sortInfo: {field: 'layer_name', direction: 'ASC'},
        groupOnSort: true,
        groupField: 'layer_name',
        baseParams: baseParams
    }); 

    var search = new Ext.form.GroupComboBox({
        store: store,
        renderTo: el,
        hideTrigger: true,
        triggerAction: 'all',
        enableKeyEvents: true,
        minChars: 1,
        queryDelay: 50, 
        emptyText: OpenLayers.i18n('Rechercher...'),
        loadingText: OpenLayers.i18n('loadingText'),
        displayField: 'label',
        groupingField: 'layer_name'
    }); 

    var onBeforeLoadStore = function(store, options) {
        var coords = store.baseParams.query.match(
            /([\d\.']+)[\s,]+([\d\.']+)/
        );
        if (coords) {
            var left = parseFloat(coords[1].replace("'", ""));
            var right = parseFloat(coords[2].replace("'", ""));
            // for switzerland:
            // EPSG:21781: lon > lat
            // EPSG:4326 : lat > lon
            var position = new OpenLayers.LonLat(
                left > right ? left : right,
                right < left ? right : left);
            var valid = false;
            if (map.maxExtent.containsLonLat(position)) {
                // try with EPSG:21781
                valid = true;
            } else {
                // try with EPSG:4326
                position = new OpenLayers.LonLat(
                    left < right ? left : right,
                    right > left ? right : left);
                position.transform(
                    new OpenLayers.Projection("EPSG:4326"),
                    map.getProjectionObject());
                if (map.maxExtent.containsLonLat(position)) {
                    valid = true;
                }
            }
            if (valid) {
                map.setCenter(position, 5);
            }
        }
        return !coords;
    };

    // recenter the map when the selection change in the
    // grouping view
    var onSelectWithMap = function(combo, record, index) {
        // do nothing in case the user clic on the "fake" feature used to
        // display "too many results" in the list
        if (!record.get('feature')) {
            return false;
        }
        var bbox = record.get('feature').bounds;
        
        if (bbox) {
            map.zoomToExtent(bbox);
            if (map.getScale() < 400) {
                map.setCenter(bbox.getCenterLonLat(), 12);
            }
        }
    };

    var onSelectWithCallback = function(combo, record, index) {
        callback(record.data.feature);
    };

    var onKeyPress = function(el, ev) {
        if (ev.getKey() == 13) {
            el.getStore().reload();
        }
    };

    // Public
    Ext.apply(this, {

    });

    // Main

    search.on('keypress', onKeyPress);

    if (map) {

        store.on('beforeload', onBeforeLoadStore);
        search.on('select', onSelectWithMap);
    }
    if (callback) {
        search.on('select', onSelectWithCallback);
    }
    
    return search;
};

Crdppf.FeatureReader = Ext.extend(GeoExt.data.FeatureReader, {
    readRecords: function(features) {
        if (this.meta.format) {
            features = this.meta.format.read(features);
        }
        return Crdppf.FeatureReader.superclass.readRecords.call(
            this, features
        );
    }   
});
