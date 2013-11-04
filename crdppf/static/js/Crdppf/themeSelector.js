Ext.namespace('Crdppf');

// create layer tree and append nodes & subnodes to it
Crdppf.ThemeSelector = function createThemeSelector () {
    this.makeThemeSelector = makeThemeSelector;
};
var makeThemeSelector = function makeThemeSelector(){

    var myReader = new Ext.data.JsonReader({
        idProperty: 'id',
        root: 'themes',
        fields: [
            {name: 'name', mapping: 'name'},
            {name: 'image', mapping: 'image'}
        ]
    });
    var myStore = new Ext.data.Store({
        reader: myReader
    });

    // load data and create listView
    myStore.loadData(layerList);
    var listView = new Ext.list.ListView({
        id: 'themeListView',
        store: myStore,
        hideHeaders: true,
        autoWidth: true,
        boxMinWidth: 100,
        expanded: true,
        singleSelect : true,
        flex: 1.0,
        emptyText: 'No images to display',
        reserveScrollOffset: true,
        columns: [
            {
                header:'icon',
                width: 0.25,
                dataIndex: 'image',
                tpl: '<img src=' + Crdppf.imagesDir + '/themes/{image}'+ ' width=50 height=25></img>'
            },
            {
                header: 'Thèmes',
                width: 0.75,
                dataIndex: 'name',
                tpl: '<p style="padding-top:6px">{name}</p>'
            }
            ],
        listeners:{
            click: function(view, index, node, e){
                layerTree.getRootNode().cascade(function(n) {
                    var ui = n.getUI();
                    ui.toggleCheck(false);
                });
                layerTree.getNodeById(myStore.getAt(index).id).getUI().toggleCheck(true);
                Ext.getCmp('infoButton').toggle(true);
                MapO.setInfoControl();
            }
        }
    });
    // insert listView into a nice looking panel
    var themePanel = new Ext.Panel({
        id:'images-view',
        collapsible:true,
        animate:true,
        layout:'fit',
        title:labels.themeSelectorLabel,
        items: listView
    });
    return themePanel;
};