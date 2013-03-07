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
// MAIN USER INTERFACE

Ext.onReady(function() {
    lang = '';
     var request = OpenLayers.Request.GET({
                    url: Crdppf.getLanguageUrl,
                    callback: defineLanguage,
                    async: false
    });
    
    function defineLanguage(request){
        lang = request.responseText;
    }
    layerList = Crdppf.layerListFr;
    if(lang=='Fr'){
        labels = Crdppf.labelsFr;
        layerList = Crdppf.layerListFr;
    }else if(lang=='De'){
        labels = Crdppf.labelsDe;
        layerList = Crdppf.layerListDe;
    }
    Ext.QuickTips.init();
    
    // create map
    var mapOptions = {
        divMousePosition: 'mousepos'
    }
    MapO = new Crdppf.Map(mapOptions);
    var map = MapO.map;
    var infoButton = new Ext.Button({
        xtype: 'button',
        margins: '0 0 0 20',
        id: 'infoButton',
        width: 40,
        enableToggle: true,
        toggleGroup: 'mapTools',
        iconCls: 'crdppf_infobutton',
        // cls: 'crdppf_infobutton',
        toggleGroup: 'mapTools',
        listeners:{
            click: function (){
                        MapO.setInfoControl()
                    }  
        }
    });
    var printButton = new Ext.Button({
    xtype: 'button',
    width: 40,
    enableToggle: true,
    iconCls: 'crdppf_printbutton',
    // cls: 'crdppf_printbutton',
    toggleGroup: 'mapTools',
    listeners:{
        click: function (){
                    alert('Impression en cours....'); 
                }  
    }
    });
    var panButton = new Ext.Button({
        pressed: true,
        xtype: 'button',
        margins: '0 0 0 20',
        width: 40,
        id: 'panButton',
        enableToggle: true,
        toggleGroup: 'mapTools',
        iconCls: 'crdppf_panbutton',
        listeners:{
            click: function (){
                        MapO.disableInfoControl()
                    }  
        }
    });
    
    // define the language buttons state
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
    // create language buttons
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
            click: function(){setLanguage('Fr')}
        }
    });
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
            click: function(){setLanguage('De')}
        }
    });
    // set the lang parameter in session
    function setLanguage(value){
         var request = OpenLayers.Request.GET({
                            url: Crdppf.setLanguageUrl,
                            params: {
                                lang:value
                            },
                            proxy: null,
                            async: false
            });
         window.location.reload();
    }
   var mapToolbar = new Ext.Toolbar({
    autoWidth: true,
    height: 20,
    cls: 'map-toolbar',
    items: [panButton,
            infoButton,
            printButton,
            frButton,
            deButton]
   });
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
    
    // Status bar
    statusbar = new Ext.ux.StatusBar({
        id: 'statusbar',
        defaultText: labels['mapBottomTxt']
    });   
   
    statusbar.add({
        xtype: 'tbtext',
        text: '<span id="mousepos" style="padding: 0 20px;"></span>'
    });
    

   var mapContainer = new Ext.Panel({
        region: "center",
        title: labels['mapContainerTab'],
        margins: '5 5 0 0',
        layout: 'border',
        items: [
            mapPanel,   
        ],
        bbar: statusbar
    }); 
    
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
    
    var navPanel = new Ext.Panel({
        
        split: true,
        collapside: true,
        border: false,
        flex: 1.0,
        id : 'nav',
        items:[themeSelector,layerTree

        ]
      });
      // set the beforeexpand event to add the corresponding layers
      // for (i = 0; i < navPanel.items.length; i++){
        // var item = navPanel.items.items[i];
        // item.on('beforeexpand', function(item){
            // MapO.setOverlays(item.themeId);
        // });
      // }
      
    var searcher = new Crdppf.SearchBox({
        map: mapPanel.map
    });
    
    var searchPanel = new Ext.Panel({
        autoHeight: true,
        autoWidth: true,
        border: false,
        items: [searcher]
    });
    
    var navigationPanel = new Ext.Panel({
        region: 'west',
        title: labels['navPanelLabel'],
        layout:'vbox',
        split: true,
        collapseMode: 'mini',
        width: 300,
        items:[searchPanel,navPanel],
        layoutConfig: {
            align: 'stretch'
        }
      });
      
   // featureTree diplayed in infoPanel as a global view 
          
    featureTree = new Ext.tree.TreePanel({
        title: labels['restrictionPanelTitle'],
        collapsed: true,
        autoheight: true,
        autoWidth: true,
        useArrows:false,
        autoScroll:true,
        collapside: true,
        animate:true,
        lines: true,
        enableDD:false,
        containerScroll: false,
        rootVisible: false,
        frame: true,
        id: 'featureTree'
    });
    
    root = new Ext.tree.TreeNode({
        text: 'Thèmes',
        draggable:false,
        id:'rootNode'})
    featureTree.setRootNode(root);
    var layerStore = new GeoExt.data.LayerStore({
        map: MapO.map
    });
    
    var legendPanel = new GeoExt.LegendPanel({
        map: MapO.map,
        title: labels['legendPanelTitle'],
        position: 'bottom',
        cls: 'legendPanelCls',
        height: 400,
        width:300,
        autoScroll:true,
        defaults: {
            style: 'padding:5px',
            baseParams: {
                FORMAT: 'image/png',
                LEGEND_OPTIONS: 'forceLabels:on'
            }
        }
    });
    infoPanel = new Ext.Panel({
            region: 'east',
            title: labels['infoTabLabel'],
            id: 'infoPanel',
            width: 300,
            collapsible: true,
            split: true,
            items:[featureTree, legendPanel]
        });

    var centerPanel = new Ext.TabPanel({
            region: 'center',
            activeTab: 0, // index or id
            items:[
                mapContainer,
            {
                title: labels['legalBasisTab'],
                autoLoad : {
                    url : '/dev_crdppf/static/public/bases_legales.html'
                }
            },{
                title: labels['lawTabLabel'],
                autoEl: {
                    tag: 'iframe',
                    style: 'height: 100%; width: 100%',
                    src: 'http://sitn.ne.ch/web/reglements/Regl_Amenagement/recupere/01_Regl_Amenagement.pdf'
                }
            },{
                title: labels['additionnalInfoTab'],
                html: 'une information complémentaire'
            }]
        });
 
      
    var southPanel = new Ext.Panel({
        region: 'south',
        title: 'Disclaimer',
        collapsible: true,
        html: labels['disclaimerTxt'],
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
    
});
