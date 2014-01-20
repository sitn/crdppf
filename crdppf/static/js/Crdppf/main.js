/*
 * @requires GeoExt/widgets/MapPanel.js
 * @requires GeoExt/widgets/LegendPanel.js 
 * @requires GeoExt/widgets/WMSLegend.js
 * @include Crdppf/map.js
 * @include Crdppf/layerTree.js
 * @include OpenLayers/Control/MousePosition.js
 * @include Crdppf/searcher/searcher.js
 * @include Crdppf/themeSelector.js
 * @include Crdppf/legalDocuments.js
 * @include Crdppf/measureTools.js
 */

// VARIABLES
var mapPanel;
var winWait;
var layerList;
// MAIN USER INTERFACE

Ext.onReady(function() {
    // set the application language to the user session settings
    var lang = ''; // The current session language
    var translations = {}; // The interface translations
    var baseLayers = {};
    var parameters = {};
    
    // We need to ensure all json data are recieved by the client before starting the application
    var loadingCounter = 0;
    
    var triggerFunction = function(counter) {
        if (counter == 4) {
            Ext.MessageBox.buttonText.yes = translations.disclaimerAcceptance;
            Ext.MessageBox.buttonText.no = translations.diclaimerRefusal;
            Ext.Msg.show({
               title: translations.disclaimerWindowTitle,
               msg: translations.disclaimerMsg,
               buttons: Ext.Msg.YESNO,
               fn: redirectAfterDisclaimer,
               animEl: 'elId',
               icon: Ext.MessageBox.WARNING
            });
        }
    };
    
    var redirectAfterDisclaimer = function(userChoice){
        if (userChoice == 'yes'){
            Crdppf.init_main(lang, parameters, baseLayers, translations);
        } else {
            window.open(translations.disclaimerRedirectUrl, "_self");
        }  
    };

    // Get the current session language
    Ext.Ajax.request({
        url: Crdppf.getLanguageUrl,
        success: function(response) {
            var lang_json = Ext.decode(response.responseText);
            lang = lang_json['lang'];
            OpenLayers.Lang.setCode(lang); 
            loadingCounter += 1;
            triggerFunction(loadingCounter);            
        },
        method: 'POST',
        failure: function () {
            Ext.Msg.alert('Error', 'The request failed, please contact the administrator!');
        }
    }); 
    
    // Load the interface's translations
    Ext.Ajax.request({
        url: Crdppf.getTranslationDictionaryUrl,
        success: function(response) {
            translations = Ext.decode(response.responseText);
            loadingCounter += 1; 
            triggerFunction(loadingCounter);            
        },
        method: 'POST',
        failure: function () {
            Ext.Msg.alert('Error', 'The request failed, please contact the administrator!');
        }
    });

    Ext.Ajax.request({
        url: Crdppf.getBaselayerConfigUrl,
        success: function(response) {
            baseLayers = Ext.decode(response.responseText);
            loadingCounter += 1; 
            triggerFunction(loadingCounter);            
        },
        method: 'POST',
        failure: function () {
            Ext.Msg.alert('Error', 'The request failed, please contact the administrator!');
        }
    });     
    
    // Load the interface's parameters
    Ext.Ajax.request({
        url: Crdppf.getInterfaceConfigUrl,
        success: function(response) {
            parameters = Ext.decode(response.responseText);
            // init the interface
            OpenLayers.Util.extend(OpenLayers.Lang.fr,translations);
            loadingCounter += 1;
            triggerFunction(loadingCounter);        
        },
        method: 'POST',
        failure: function () {
            Ext.Msg.alert('Error', 'The request failed, please contact the administrator!');
        }
    }); 
});

Ext.namespace('Crdppf');

Crdppf.init_main = function(lang, parameters, baseLayers, translations) {
    layerList = parameters;
    labels = translations;
    baseLayersList = baseLayers;

    Ext.QuickTips.init();

    // add onclick event to the Fr/De links
    Ext.get('frLink').on('click',function() {
        setLanguage('Fr');
    });
    Ext.get('deLink').on('click',function() {
        setLanguage('De');
    });

    // create map
    var mapOptions = {
        divMousePosition: 'mousepos'
    };
    MapO = new Crdppf.Map(mapOptions);
    var map = MapO.map;

    // getFeatureInfo button: activates the Openlayers infoControl
    var infoButton = new Ext.Button({
        xtype: 'button',
        tooltip: labels.infoButtonTlp,
        margins: '0 0 0 20',
        id: 'infoButton',
        width: 40,
        enableToggle: true,
        toggleGroup: 'mapTools',
        iconCls: 'crdppf_infobutton',
        listeners:{
            toggle: function (me, pressed){
                if (pressed) {
                    MapO.setInfoControl();
                }
            }                  
        }
    });

    // clearSelection button: empty the current selection
    var clearSelectionButton = new Ext.Button({
        xtype: 'button',
        tooltip: labels.clearSelectionButtonTlp,
        margins: '0 0 0 20',
        id: 'clearSelectionButton',
        width: 40,
        enableToggle: false,
        iconCls: 'crdppf_clearselectionbutton',
        listeners:{
            click: function (){
                var selectionLayer = MapO.map.getLayer('selectionLayer');
                selectionLayer.removeAllFeatures();
                MapO.disableInfoControl();
                infoButton.toggle(false);
            }                  
        }
    });

    var measureControlO = new Crdppf.MeasureTool();
    measureControlO.makeMeasureTool();
    
    var lineMeasureButton = new Ext.Button({
        xtype: 'button',
        tooltip: labels.infoButtonTlp,
        text: labels.measureToolDistanceTxt,
        margins: '0 0 0 20',
        id: 'distanceButton',
        width: 40,
        enableToggle: true,
        toggleGroup: 'mapTools',
        iconCls: 'crdppf_distancebutton',
        listeners:{
            toggle: function (me, pressed){
                if (pressed){
                    measureControlO.toggleMeasureControl('line');
                } else if( !pressed && !polygonMeasureButton.pressed) {
                    measureControlO.disableMeasureControl();
                    infoButton.toggle(true);
                }
            }
        }
    });    
    
    var polygonMeasureButton = new Ext.Button({
        xtype: 'button',
        tooltip: labels.infoButtonTlp,
        text: labels.measureToolSurfaceTxt,
        margins: '0 0 0 20',
        id: 'polygonButton',
        width: 40,
        enableToggle: true,
        toggleGroup: 'mapTools',
        iconCls: 'crdppf_polygonbutton',
        listeners:{
            toggle: function (me, pressed){
                if (pressed) {
                    measureControlO.toggleMeasureControl('polygon');
                } else if( !pressed && !lineMeasureButton.pressed) {
                    measureControlO.disableMeasureControl();
                    infoButton.toggle(true);
                }
            }                  
        }
    });

    var measureToolsMenu = new Ext.SplitButton({
        text: labels.measureToolTxt,
        showText: true,
        menu: new Ext.menu.Menu({
            items: [
                lineMeasureButton,
                polygonMeasureButton
            ]
        })
    });
    
    // generate the pdf file of the current map
    var printButton = new Ext.Button({
        xtype: 'button',
        tooltip: labels.printButtonTlp,
        width: 40,
        enableToggle: true,
        iconCls: 'crdppf_printbutton',
        listeners:{
            click: function (){
                if(select.features.length == 1){
                    var chooseExtract = new Ext.Window({
                        title: labels.chooseExtractTypeMsg,
                        width: 300,
                        height: 110,
                        items: [
                            {
                                xtype: 'spacer',
                                height: 5
                            },{
                                xtype: 'label',
                                text: labels.chooseExtractMsg,
                                cls: 'textExtractCls'
                            },{
                                xtype: 'spacer',
                                height: 5
                            },{
                                xtype: 'radiogroup',
                                id: 'extractRadioGroup',
                                fieldLabel: 'Auto Layout',
                                items: [
                                    {boxLabel: labels.reducedExtract, name: 'rb-auto', inputValue: 'reduced',  cls: 'radioExtractCls', checked: true},
                                    {boxLabel: labels.extendedExtract, name: 'rb-auto', inputValue: 'certified',  cls: 'radioExtractCls'}
                                ]
                            },{
                                xtype: 'buttongroup',
                                cls: 'extractButtonCls',
                                fieldLabel: 'Auto Layout',
                                items: [
                                    {
                                        xtype: 'button',
                                        text: labels.generateExtract,                                        
                                        listeners: {
                                            click: function(){
                                                urlToOpen = Crdppf.printUrl + '?id=' + select.features[0].attributes.idemai;
                                                selectedRadio = Ext.getCmp('extractRadioGroup').getValue();
                                                urlToOpen += '&type=' + selectedRadio.inputValue;
                                                window.open(urlToOpen);
                                            }
                                        }
                                    },{
                                        xtype: 'button',
                                        text: labels.cancelExtract,
                                        listeners: {
                                            click: function(){
                                                chooseExtract.destroy();
                                            }
                                            
                                        }
                                    }
                                ]
                            }
                            
                        ]
                        
                    });
                    chooseExtract.show();
                }
                else {
                    Ext.Msg.alert(labels.infoMsgTitle, labels.noSelectedParcelMessage);
                    infoButton.toggle(true);
                }
            }
        }
    });

    // activate the standard pan button
    var panButton = new Ext.Button({
        pressed: true,
        tooltip: labels.panButtonTlp,
        xtype: 'button',
        margins: '0 0 0 20',
        width: 40,
        id: 'panButton',
        enableToggle: true,
        toggleGroup: 'mapTools',
        iconCls: 'crdppf_panbutton',
        listeners:{
            click: function (){
                MapO.disableInfoControl();
            }  
        }
    });

    // zoom in button
    var zoomInButton = new Ext.Button({
        pressed: false,
        tooltip: labels.zoomInButtonTlp,
        xtype: 'button',
        margins: '0 0 0 20',
        width: 40,
        id: 'zoomInButton',
        iconCls: 'crdppf_zoominbutton',
        listeners:{
            click: function (){
                MapO.map.zoomIn();
            }  
        }
    });

    // zoom out Button
        var zoomOutButton = new Ext.Button({
        pressed: false,
        tooltip: labels.zoomOutButtonTlp,
        xtype: 'button',
        margins: '0 0 0 20',
        width: 40,
        id: 'zoomOutButton',
        iconCls: 'crdppf_zoomoutbutton',
        listeners:{
            click: function (){
                MapO.map.zoomOut();
            }  
        }
    });

    // Create the buttons used to switch language
    var isPressedFr = false;
    var isPressedDe = false;
    if(lang=='Fr'){
        isPressedFr = true;
        isPressedDe = false;
    }
    else if(lang=='De'){
        isPressedFr = false;
        isPressedDe = true;
    }

    // button for french
    var frButton = new Ext.Button({
        pressed: isPressedFr,
        text:'Fr',
        xtype: 'button',
        margins: '0 0 0 0',
        width: 40,
        id: 'frButton',
        toggleGroup: 'langButton',
        iconCls: 'crdppf_frButton',
        listeners:{
            click: function(){setLanguage('Fr');
            }
        }
    });

    // button for german
    var deButton = new Ext.Button({
        pressed: isPressedDe,
        text:'De',
        xtype: 'button',
        margins: '0 0 0 0',
        width: 40,
        id: 'deButton',
        iconCls: 'crdppf_deButton',
        toggleGroup: 'langButton',
        listeners:{
            click: function(){setLanguage('De');
            }
        }
    });

    // set the lang parameter in session when selected through the language buttons
    function setLanguage(value){
        var request = OpenLayers.Request.GET({
            url: Crdppf.setLanguageUrl,
            params: {
                lang:value,
                randomkey: Math.random()
            },
            proxy: null,
            async: false
        });
        window.location.reload();
    }

    // create the mapPanel toolbar
    var mapToolbar = new Ext.Toolbar({
    autoWidth: true,
    height: 20,
    cls: 'map-toolbar',
    items: [
        panButton,
        infoButton,
        clearSelectionButton,
        printButton,
        zoomInButton,
        zoomOutButton,
        measureToolsMenu,
        {
            xtype: 'label',
            html: '<div id="measureOuput"></div>'
        }
        ]
   });

   // create the mapPanel
    var mapPanel = new GeoExt.MapPanel({
        id:'mapPanel',
        stateId: "map",
        region: 'center',
        theme: null,
        extent: new OpenLayers.Bounds(420000,30000,900000,360000),
        prettyStateKeys: true,
        center: new OpenLayers.LonLat(550000, 204000),
        zoom: 1,
        map: map,
        tbar: mapToolbar
    });

    // Status & disclaimer bar visible at the bottom of the map panel
    var bottomToolBarHtml = '<span style="padding: 0 20px;">' + labels.mapBottomTxt + '</span>';
    bottomToolBarHtml += '<span id="mousepos" style="padding: 0 20px;"></span>';
    bottomToolBarHtml += '<div style="padding: 0 20px; margin-top: 3px;">'+ labels.disclaimerTxt + '</div>';
    
    var bottomToolBar = new Ext.Toolbar({
        autoWidth: true,
        height: 50,
        html: bottomToolBarHtml
    });

    // create the mapContainer: one Ext.Panel with a map & a toolbar
   var mapContainer = new Ext.Panel({
        region: "center",
        title: labels.mapContainerTab,
        margins: '5 5 0 0',
        layout: 'border',
        items: [
            mapPanel   
        ],
        bbar: bottomToolBar
    }); 

    // create the header panel containing the page banner
    var headerPanel = new Ext.Panel({
        region: 'north',
        height: 55,
        border: false,
        contentEl: 'header'
    });

    layerTreeO = new Crdppf.LayerTree();
    layerTree = layerTreeO.makeLayerTree();
    themeSelectorO = new Crdppf.ThemeSelector();
    themeSelector = themeSelectorO.makeThemeSelector();

    // create the CGPX searchbox
    var searcher = new Crdppf.SearchBox({
        map: mapPanel.map,
        url: Crdppf.fulltextsearchUrl
    });

    // Create the navigation panel
    var navigationPanel = new Ext.Panel({
        region: 'west',
        title: labels.navPanelLabel,
        layout:'vbox',
        flex: 1.0,
        split: true,
        collapseMode: 'mini',
        width: 250,
        boxMinWidth: 225,
        items:[searcher,themeSelector,layerTree],
        layoutConfig: {
            align: 'stretch'
        }
      });

   // featureTree displayed in infoPanel as a global view 
    featureTree = new Ext.tree.TreePanel({
        title: labels.restrictionPanelTitle,
        cls: 'featureTreeCls',
        collapsed: false,
        useArrows:false,
        collapside: false,
        animate:true,
        lines: false,
        enableDD:false,
        rootVisible: false,
        frame: false,
        id: 'featureTree',
        height:300,
        autoScroll: true
    });

    root = new Ext.tree.TreeNode({
        text: 'Thèmes',
        draggable:false,
        id:'rootNode'
    });

    featureTree.setRootNode(root);

    var layerStore = new GeoExt.data.LayerStore({
        map: MapO.map
    });

    var legendPanel = new GeoExt.LegendPanel({
        collapsible:true, 
        map: MapO.map,
        cls:'legendPanelCls',
        title: labels.legendPanelTitle,
        height: 400,
        autoScroll: true,
        defaults: {
            style: 'padding:5px',
            baseParams: {
                FORMAT: 'image/png',
                LEGEND_OPTIONS: 'forceLabels:on'
            }
        }
    });

    infoPanel = new Ext.Panel({
        header: false,
        width: 250,
        region: 'east',
        title: labels.infoTabLabel,
        collapseMode: 'mini',
        id: 'infoPanel',
        cls: 'infoPanelCls',
        collapsible: true,
        split: true,
        items:[featureTree, legendPanel]
    });

    centerPanel = new Ext.TabPanel({
        region: 'center',
        activeTab: 0, // index or id
        autoScroll: true,
        items:[
            mapContainer,
            Crdppf.legalDocuments()
        ]
    });

    var crdppf = new Ext.Viewport({
        layout: 'border',
        renderTo:'main',
        id:'viewPort',
        border:true,
        items: [headerPanel,
            navigationPanel,
            infoPanel, 
            centerPanel]
    });
    mapPanel = Ext.getCmp('mappanel');    
	// Refait la mise en page si la fenêtre change de taille
	//pass along browser window resize events to the panel
	Ext.EventManager.onWindowResize(crdppf.doLayout,crdppf);

};
