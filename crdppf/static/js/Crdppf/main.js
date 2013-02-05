/*
 * @requires GeoExt/widgets/MapPanel.js
 * @include Crdppf/map.js
 * @include OpenLayers/Control/MousePosition.js
  * @include Crdppf/searcher/searcher.js
 */

// VARIABLES
var mapPanel;
var winWait;

// MAIN USER INTERFACE

Ext.onReady(function() {

    Ext.QuickTips.init();
    
    // create map
    var mapOptions = {
        divMousePosition: 'mousepos'
    }
    var MapO = new Crdppf.Map(mapOptions);
    var map = MapO.map;
    var infoButton = new Ext.Button({
        xtype: 'button',
        width: 40,
        enableToggle: true,
        iconCls: 'crdppf_infobutton',
        // cls: 'crdppf_infobutton',
        toggleGroup: 'mapTools',
        listeners:{
            click: function (){
                        MapO.setInfoControl()
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
                        // var mapP = document.getElementById('OpenLayers_Map_9');
                        // console.log(mapP);
                        // mapP.style.cursor = "pointer";
                    }  
        }
    });
   var mapToolbar = new Ext.Toolbar({
    autoWidth: true,
    height: 20,
    cls: 'map-toolbar',
    items: [panButton,
            infoButton]
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
        defaultText: '<b>Informations dépourvues de foi publique, <a style="color:#660000;" href="http://sitn.ne.ch/web/conditions_utilisation/contrat_SITN_MO.htm" target="_new">&copy; SITN</a>, <a style="color:#660000;" href="http://sitn.ne.ch/web/conditions_utilisation/contratdv5741.htm" target="_new">swisstopo DV 571.4</a>, <a style="color:#660000;" href="http://www.openstreetmap.org/copyright" target="_new">OpenStreetMap</a></b>'
    });   
   
    statusbar.add({
        xtype: 'tbtext',
        text: '<span id="mousepos" style="padding: 0 20px;"></span>'
    });
    

   var mapContainer = new Ext.Panel({
        region: "center",
        title: 'Carte',
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
    
    // layerTree diplayed in navPanel as a global view
    var layerTree = new Ext.tree.TreePanel({
        title: 'Vue d\'ensemble',
        height: 300,
        width: 400,
        useArrows:true,
        autoScroll:true,
        animate:true,
        enableDD:true,
        containerScroll: true,
        rootVisible: false,
        frame: true,
        root: new Ext.tree.AsyncTreeNode({
        text: 'Thèmes',
        draggable:false,
        id:'layerTree',
        children: Crdppf.layerTreeListFr}),
        listeners: {
                'checkchange': function(node, checked){
                    if(checked){
                        MapO.setOverlays(node.id)
                    }else{
                        //MapO.removeOverlays(node.id)
                    }
                }
            },
    });

    var navPanel = new Ext.Panel({
        layout: 'accordion',
        border: false,
        flex: 1.0,
        id : 'nav',
        items:[layerTree,
        {
            title: '73 - <b style=\'color:orange;\'>Plans d\'affectation - Pas disponible</b>',
            id: '73',
            themeId: '73',
            autoLoad : {
                url : '/dev_crdppf/static/public/adresse.html'
            }
        },{
            title: '79 - <b style=\'color:red;\'>Chemins pour piétons - pas concerné</b>',
            themeId: '79',
            html: 'Content'
        },{
            themeId: '87',
            title: '87 - Zones réservées des routes nationales',
            html: 'Content'
        },{
            title: '88 - Alignements des routes nationales',
            html: 'Content'
        },{
            title: '96 - Zones réservées des installations ferroviaires',
            html: 'Content'
        },{
            title: '97 - Alignements des installations ferroviaires',
            html: 'Content'
        },{
            title: '103 - zones réservées des installations aéropotuaires',
            themeId:'103',
            html: 'Content'
        },{
            title: '104 - Alignements des installations aéroportuaires',
            html: 'Content'
        },{
            title: '108 - Carte et liste des obstacles à la navigation aérienne',
            themeId:'108',
            html: 'Content'
        },{
            title: '116 - Cadastre des sites pollués',
            themeId:'116',
            html: 'Content'
        },{
            title: '117 - Cadastre des sites pollués - domaine militaire',
            html: 'Content'
        },{
            title: '118 - Cadastre des sites pollués - domaine des aérodromes civils',
            html: 'Content'
        },{
            title: '119 - Cadastre des sites pollués - domaine des transports publics',
            html: 'Content'
        },{
            title: '131 - Zones de protection des eaux souterraines',
            html: 'Content'
        },{
            title: '132 - Périmètres de protection des eaux souterraines',
            html: 'Content'
        },{
            title: '145 - Degrés de sensibilité au bruit',
            html: 'Content'
        },{
            title: '157 - Limites de la forêt',
            id: 'panel2',
            html: 'Content'
        },{
            title: '159 - Distances par rapport à la forêt',
            id: '159',
            html: 'Content'
        },{
            title: '50-NE - Plans d\'alignement (communaux)',
            id: '50-NE',
            html: 'Content'
        },{
            title: '74-NE - Alignements des routes cantonales',
            id: 'panel2',
            html: 'Content'
        }]
      });
      // set the beforeexpand event to add the corresponding layers
      for (i = 0; i < navPanel.items.length; i++){
        var item = navPanel.items.items[i];
        item.on('beforeexpand', function(item){
            MapO.setOverlays(item.themeId);
        });
      }
      
    var searcher = new Crdppf.SearchBox({
        map: mapPanel.map
    });
    
    var searchPanel = new Ext.Panel({
        autoHeight: true,
        width: 300,
        border: false,
        items: [searcher]
    });
    
    var navigationPanel = new Ext.Panel({
        region: 'west',
        title: 'Navigation',
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
        title: 'Attributs',
        height: 300,
        width: 400,
        useArrows:false,
        autoScroll:true,
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
        
    legendPanel = new Ext.Panel({
            region: 'east',
            title: 'Légende',
            id: 'legendPanel',
            width: 200,
            collapsible: true,
            split: true,
        })    
    infoPanel = new Ext.Panel({
            region: 'east',
            title: 'Informations',
            id: 'infoPanel',
            width: 200,
            html: 'Légende',
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
                title: 'Bases légales',
                autoLoad : {
                    url : '/dev_crdppf/static/public/bases_legales.html'
                }
            },{
                title: 'Règlements',
                autoEl: {
                    tag: 'iframe',
                    style: 'height: 100%; width: 100%',
                    src: 'http://sitn.ne.ch/web/reglements/Regl_Amenagement/recupere/01_Regl_Amenagement.pdf'
                }
            },{
                title: 'Informations et renvois supplémentaires',
                html: 'une information complémentaire'
            }]
        });
 
      
    var southPanel = new Ext.Panel({
        region: 'south',
        title: 'Disclaimer',
        collapsible: true,
        html: 'Mise en garde : Le canton de Neuchâtel n\'engage pas sa responsabilité sur l\'exactitude ou la fiabilité des documents législatifs dans leur version électronique. Ces documents ne créent aucun autre droit ou obligation que ceux qui découlent des textes légalement adoptés et publiés, qui font seuls foi.',
        split: true,
        height: 100,
        minHeight: 100
    });

    
    var crdppf = new Ext.Viewport({
        layout: 'border',
        renderTo:'main',
        border:true,
        items: [headerPanel,
            navigationPanel,
            infoPanel, 
            centerPanel,
            southPanel]
    });
    MapO.setOverlays('0');
    mapPanel = Ext.getCmp('mappanel');    
	// Refait la mise en page si la fenêtre change de taille
	//pass along browser window resize events to the panel
	Ext.EventManager.onWindowResize(crdppf.doLayout,crdppf);
    

    // set up and activate the infoControl
    // MapO.setInfoControl();
    // deactivate the infoControl
    // MapO.disableInfoControl();
    
});