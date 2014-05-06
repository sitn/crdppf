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

var layerList;

// MAIN USER INTERFACE
Ext.onReady(function() {
    
    Ext.namespace('Crdppf');
    Crdppf.layerList = '';
    Crdppf.labels = '' ;
    Crdppf.baseLayersList = '';
    
    // set the application language to the user session settings
    var lang = ''; // The current session language
    // We need to ensure all json data are recieved by the client before starting the application
    var loadingCounter = 0;
    
    var triggerFunction = function(counter) {
        if (counter == 4) {
            Ext.MessageBox.buttonText.yes = Crdppf.labels.disclaimerAcceptance;
            Ext.MessageBox.buttonText.no = Crdppf.labels.diclaimerRefusal;
            var dlg = Ext.MessageBox.getDialog();
            var buttons = dlg.buttons;
            for (var i = 0; i < buttons.length; i++){
                 buttons[i].addClass('msgButtonStyle'); 
            }
            
            Ext.Msg.show({
               title: Crdppf.labels.disclaimerWindowTitle,
               msg: Crdppf.labels.disclaimerMsg,
               buttons: Ext.Msg.YESNO,
               fn: redirectAfterDisclaimer,
               animEl: 'elId',
               icon: Ext.MessageBox.WARNING
            });
        }
    };
    
    var redirectAfterDisclaimer = function(userChoice){
        if (userChoice == 'yes'){
            Crdppf.init_main(lang);
        } else {
            window.open(Crdppf.labels.disclaimerRedirectUrl, "_self");
        }  
    };

    // Get the current session language
    Ext.Ajax.request({
        url: Crdppf.getLanguageUrl,
        success: function(response) {
            var lang_json = Ext.decode(response.responseText);
            lang = lang_json['lang'];
            OpenLayers.Lang.setCode(lang);
            if (lang !== '' && lang == 'Fr'){
                OpenLayers.Util.extend(OpenLayers.Lang.fr, Crdppf.labels);
            } else if (lang !== '' && lang == 'De') {
                OpenLayers.Util.extend(OpenLayers.Lang.de, Crdppf.labels);
            } else if (lang !== '' && lang == 'en') {
                OpenLayers.Util.extend(OpenLayers.Lang.en, Crdppf.labels);
            } else if (lang !== '') {
                OpenLayers.Util.extend(OpenLayers.Lang.fr, Crdppf.labels);
            }
            loadingCounter += 1;
            triggerFunction(loadingCounter);            
        },
        method: 'POST',
        failure: function () {
            Ext.Msg.alert(Crdppf.labels.serverErrorMessage);
        }
    }); 
    
    // Load the interface's Crdppf.labels
    Ext.Ajax.request({
        url: Crdppf.getTranslationDictionaryUrl,
        success: function(response) {
            Crdppf.labels = Ext.decode(response.responseText);
            loadingCounter += 1; 
            triggerFunction(loadingCounter);            
        },
        method: 'POST',
        failure: function () {
            Ext.Msg.alert(Crdppf.labels.serverErrorMessage);
        }
    });

    // Load base layers configuration
    Ext.Ajax.request({
        url: Crdppf.getBaselayerConfigUrl,
        success: function(response) {
            Crdppf.baseLayersList = Ext.decode(response.responseText);
            loadingCounter += 1; 
            triggerFunction(loadingCounter);            
        },
        method: 'POST',
        failure: function () {
            Ext.Msg.alert(Crdppf.labels.serverErrorMessage);
        }
    });     
    
    // Load the interface configuration
    Ext.Ajax.request({
        url: Crdppf.getInterfaceConfigUrl,
        success: function(response) {
            Crdppf.layerList = Ext.decode(response.responseText);

            loadingCounter += 1;
            triggerFunction(loadingCounter);        
        },
        method: 'POST',
        failure: function () {
            Ext.Msg.alert(Crdppf.labels.serverErrorMessage);
        }
    }); 
});

Ext.namespace('Crdppf');

Crdppf.init_main = function(lang) {

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
    MapO = new Crdppf.Map(mapOptions,Crdppf.labels);
    var map = MapO.map;

    // getFeatureInfo button: activates the Openlayers infoControl
    var infoButton = new Ext.Button({
        xtype: 'button',
        tooltip: Crdppf.labels.infoButtonTlp,
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
        tooltip: Crdppf.labels.clearSelectionButtonTlp,
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

    var measureLabelBox = new Ext.form.Label({
        cls: 'measureOutput'
    });

    var measureControlO = new Crdppf.MeasureTool(map, measureLabelBox);
    measureControlO.makeMeasureTool();
    
    var lineMeasureButton = new Ext.Button({
        xtype: 'button',
        tooltip: Crdppf.labels.infoButtonTlp,
        text: Crdppf.labels.measureToolDistanceTxt,
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
        tooltip: Crdppf.labels.infoButtonTlp,
        text: Crdppf.labels.measureToolSurfaceTxt,
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
        text: Crdppf.labels.measureToolTxt,
        showText: true,
        menu: new Ext.menu.Menu({
            items: [
                lineMeasureButton,
                polygonMeasureButton
            ]
        })
    });
 
    // Panel to display the link to the PDF once generated
    var pdfDisplayPanel = new Ext.Panel({
        id:'pdfDisplayPanel',
        cls:'pdfDownloadCls',
        hidden: true,
        border: false,
        height:100,
        items: [{
            xtype: 'button',
            id: 'pdfDisplayButton',
            cls: 'msgButtonStyle',
            text: Crdppf.labels.extractPDFDisplayMsg,
            listeners: {
                click: function() {
                    Ext.getCmp('pdfExtractWindow').hide();
                    }
                }
            }
        ]
    });

    // Panel to render the PDF extract type choices
    var pdfChoicePanel = new Ext.Panel({
        id: 'pdfChoicePanel',
        cls:'extractChoiceBody',
        border: false,
        hidden: false,
        layout:'auto',
        items: [{
            xtype: 'spacer',
            height: 5
        },{
            xtype: 'label',
            text: Crdppf.labels.chooseExtractMsg,
            cls: 'textExtractCls'
        },{
            xtype: 'label',
            id: 'pdfLoadDiv'
        },{
            xtype: 'spacer',
            height: 5
        },{
            xtype: 'radiogroup',
            id: 'extractRadioGroup',
            fieldLabel: 'Auto Layout',
            items: [
                {boxLabel: Crdppf.labels.reducedExtract, name: 'rb-auto', inputValue: 'reduced',  cls: 'radioExtractCls', checked: true},
                {boxLabel: Crdppf.labels.extendedExtract, name: 'rb-auto', inputValue: 'standard',  cls: 'radioExtractCls'}
            ]
        },{
            xtype: 'buttongroup',
            cls: 'extractButtonCls',
            fieldLabel: 'Auto Layout',
            items: [{
                xtype: 'button',
                text: Crdppf.labels.generateExtract,  
                cls: 'msgButtonStyle',
                listeners: {
                    click: function(){
                        var pdfMask = new Ext.LoadMask(Ext.getCmp('pdfExtractWindow').body, {msg: Crdppf.labels.pdfLoadMessage});
                        pdfMask.show();
                        var urlToOpen = Crdppf.printUrl + '?id=' + select.features[0].attributes.idemai;
                        var selectedRadio = Ext.getCmp('extractRadioGroup').getValue();
                        urlToOpen += '&type=' + selectedRadio.inputValue;
                        
                        Ext.Ajax.request({
                            url: urlToOpen,
                            success: function(response) {
                                var result = Ext.util.JSON.decode(response.responseText);
                                var pdfurl = result['pdfurl'];
                                var button = Ext.getCmp('pdfDisplayButton');
                                button.setHandler(function() {window.open(pdfurl);});
                                Ext.getCmp('pdfDisplayPanel').show();
                                Ext.getCmp('pdfChoicePanel').hide();
                                pdfMask.hide();
                            },
                            method: 'POST',
                            timeout : 300000,
                            failure: function () {
                                Ext.Msg.alert(Crdppf.labels.serverErrorMessage);
                            }
                        }); 
                    }
                }
            },{
                    xtype: 'button',
                    cls: 'msgButtonStyle',
                    height: 20,
                    width: 100,    
                    text: Crdppf.labels.cancelExtract,
                    listeners: {
                        click: function(){
                            chooseExtract.hide();
                            }
                        }
                    }
                ]
            }
        ]
    });
        
    var chooseExtract = new Ext.Window({
        id: 'pdfExtractWindow',
        title: Crdppf.labels.chooseExtractTypeMsg,
        width: 300,
        height: 115,
        layout:'fit',
        closeAction: 'hide',
        items: [
            pdfChoicePanel,
            pdfDisplayPanel
        ],
        listeners: {
            hide: function() {
                Ext.getCmp('pdfDisplayPanel').hide();
                Ext.getCmp('pdfChoicePanel').show();
            }
        }
    });
    
    // generate the pdf file of the current map
    var printButton = new Ext.Button({
        xtype: 'button',
        tooltip: Crdppf.labels.printButtonTlp,
        width: 40,
        enableToggle: true,
        iconCls: 'crdppf_printbutton',
        listeners:{
            click: function (){
                if(select.features.length == 1){
                    chooseExtract.show();
                }
                else {
                    Ext.Msg.alert(Crdppf.labels.infoMsgTitle, Crdppf.labels.noSelectedParcelMessage);
                    infoButton.toggle(true);
                }
            }
        },
        scope: this
    });

    // activate the standard pan button
    var panButton = new Ext.Button({
        pressed: true,
        tooltip: Crdppf.labels.panButtonTlp,
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
        tooltip: Crdppf.labels.zoomInButtonTlp,
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
        tooltip: Crdppf.labels.zoomOutButtonTlp,
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
        measureLabelBox
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
    var bottomToolBarHtml = '<span style="padding: 0 20px;">' + Crdppf.labels.mapBottomTxt + '</span>';
    bottomToolBarHtml += '<span id="mousepos" style="padding: 0 20px;"></span>';
    bottomToolBarHtml += '<div style="padding: 0 20px; margin-top: 3px;">'+ Crdppf.labels.disclaimerTxt + '</div>';
    
    var bottomToolBar = new Ext.Toolbar({
        autoWidth: true,
        height: 50,
        html: bottomToolBarHtml
    });

    // create the mapContainer: one Ext.Panel with a map & a toolbar
   var mapContainer = new Ext.Panel({
        region: "center",
        title: Crdppf.labels.mapContainerTab,
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

    layerTree = Crdppf.LayerTree(Crdppf.labels, Crdppf.layerList, Crdppf.baseLayersList);
    themeSelector = Crdppf.ThemeSelector(Crdppf.labels, Crdppf.layerList);

    // create the CGPX searchbox
    var searcher = new Crdppf.SearchBox({
        map: mapPanel.map,
        url: Crdppf.fulltextsearchUrl
    });

    // Create the navigation panel
    var navigationPanel = new Ext.Panel({
        region: 'west',
        title: Crdppf.labels.navPanelLabel,
        layout:'vbox',
        flex: 1.0,
        split: true,
        collapseMode: 'mini',
        width: 250,
        boxMinWidth: 225,
        items: [
            searcher, 
            themeSelector, 
            layerTree
        ],
        layoutConfig: {
            align: 'stretch'
        }
      });

   // featureTree displayed in infoPanel as a global view 
    featureTree = new Ext.tree.TreePanel({
        title: Crdppf.labels.restrictionPanelTitle,
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
    
    //legend panel in the lower east layout part - serves to display the layer legends
    var legendPanel = new GeoExt.LegendPanel({
        collapsible:true, 
        map: MapO.map,
        cls:'legendPanelCls',
        title: Crdppf.labels.legendPanelTitle,
        autoScroll: true,
        flex: 1.0,
        defaults: {
            style: 'padding:5px',
            baseParams: {
            FORMAT: 'image/png',
            LEGEND_OPTIONS: 'forceLabels:on'
            }
        }
    });
    
    //query info display panel in the upper east part of the layout - serves to display the feature info
    infoPanel = new Ext.Panel({
        header: false,
        layout: 'vbox',
        width: 300,
        region: 'east',
        title: Crdppf.labels.infoTabLabel,
        collapseMode: 'mini',
        id: 'infoPanel',
        cls: 'infoPanelCls',
        collapsible: true,
        split: true,
        layoutConfig: {
            align: 'stretch'
        },
        items: [
            featureTree,
            legendPanel
        ]
    });
    
    // Container for the map and legal documents display
    centerPanel = new Ext.TabPanel({
        region: 'center',
        activeTab: 0, // index or id
        autoScroll: true,
        items:[
            mapContainer,
            Crdppf.legalDocuments(Crdppf.labels)
        ]
    });
    
    // Main window layout
    var crdppf = new Ext.Viewport({
        layout: 'border',
        renderTo:'main',
        id:'viewPort',
        border:true,
        items: [
            headerPanel,
            navigationPanel,
            infoPanel, 
            centerPanel
        ]
    });

    mapPanel = Ext.getCmp('mappanel');    
	// Refait la mise en page si la fenêtre change de taille
	//pass along browser window resize events to the panel
	Ext.EventManager.onWindowResize(crdppf.doLayout,crdppf);
};
