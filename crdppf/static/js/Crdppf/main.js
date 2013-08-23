/*
 * @requires GeoExt/widgets/MapPanel.js
 * @requires GeoExt/widgets/LegendPanel.js 
 * @requires GeoExt/widgets/WMSLegend.js
 * @include Crdppf/map.js
 * @include Crdppf/layerTree.js
 * @include OpenLayers/Control/MousePosition.js
 * @include Crdppf/searcher/searcher.js
 * @include Crdppf/themeSelector.js
 */

// VARIABLES
var mapPanel;
var winWait;
var layerList
// MAIN USER INTERFACE

Ext.onReady(function() {
    // set the application language to the user session settings
    var lang = '';

    Ext.Ajax.request({
        url: Crdppf.getLanguageUrl,
        success: function(response) {
            var lang_json = Ext.decode(response.responseText);
            lang = lang_json['lang'];
            Crdppf.init_main(lang);
        },
        method: 'POST',
        failure: function () {
            Ext.Msg.alert('Error', 'The request failed, please contact the administrator!');
        }
    });
});

Ext.namespace('Crdppf');

Crdppf.init_main = function(lang) {

    layerList = Crdppf.layerListFr;

    if(lang=='Fr'){
        labels = Crdppf.labelsFr;
        layerList = Crdppf.layerListFr;
    }else if(lang=='De'){
        labels = Crdppf.labelsDe;
        layerList = Crdppf.layerListDe;
    }
    
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
            click: function (){
                MapO.setInfoControl();
            }                  
        }
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
                    window.open(Crdppf.printUrl + '?id=' + select.features[0].attributes.idemai);
                }
                else {
                    alert(labels.noSelectedParcelMessage);
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
        enableToggle: true,
        toggleGroup: 'mapTools',
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
        enableToggle: true,
        toggleGroup: 'mapTools',
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
    items: [panButton,
        infoButton,
        printButton,
        zoomInButton,
        zoomOutButton
        // frButton,
        // deButton
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
    
    // create the status bar
    statusbar = new Ext.ux.StatusBar({
        id: 'statusbar',
        defaultText: labels.mapBottomTxt
    });   
    statusbar.add({
        xtype: 'tbtext',
        text: '<span id="mousepos" style="padding: 0 20px;"></span>'
    });
    
    // create the mapContaine: one Ext.Panel with a map & a toolbar
   var mapContainer = new Ext.Panel({
        region: "center",
        title: labels.mapContainerTab,
        margins: '5 5 0 0',
        layout: 'border',
        items: [
            mapPanel   
        ],
        bbar: statusbar
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
        map: mapPanel.map
    });
    
    // Add the searchBox to an Ext.Panel
    var searchPanel = new Ext.Panel({
        autoWidth: true,
        border: false,
        items: [searcher]
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
        items:[searchPanel,themeSelector,layerTree],
        layoutConfig: {
            align: 'stretch'
        }
      });
      
   // featureTree diplayed in infoPanel as a global view 
          
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
        defaults: {
            style: 'padding:5px',
            baseParams: {
                FORMAT: 'image/png',
                LEGEND_OPTIONS: 'forceLabels:on'
            }
        }
    });
    infoPanel = new Ext.Panel({
            header:false,
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
        items:[
            mapContainer,
            {
                title: labels.legalBasisTab,
                autoLoad : {
                    tag: 'iframe',
                    url : 'http://www.geobasisdaten.ch/index.php?lang=fr&loc=CH&s=data&data=73/'
                }
            },{
                title: labels.lawTabLabel,
                autoEl: {
                    tag: 'iframe',
                    style: 'height: 100%; width: 100%',
                    src: 'http://sitn.ne.ch/web/reglements/Regl_Amenagement/recupere/01_Regl_Amenagement.pdf'
                }
            },{
                title: labels.additionnalInfoTab,
                html: 'une information complémentaire'
        }]
    });
 
    var southPanel = new Ext.Panel({
        region: 'south',
        title: 'Disclaimer',
        collapsible: true,
        html: labels.disclaimerTxt,
        split: true,
        height: 70,
        minHeight: 70
    });

    var crdppf = new Ext.Viewport({
        layout: 'border',
        renderTo:'main',
        id:'viewPort',
        border:true,
        items: [headerPanel,
            navigationPanel,
            infoPanel, 
            centerPanel,
            southPanel]
    });
    mapPanel = Ext.getCmp('mappanel');    
	// Refait la mise en page si la fenêtre change de taille
	//pass along browser window resize events to the panel
	Ext.EventManager.onWindowResize(crdppf.doLayout,crdppf);
    
};
