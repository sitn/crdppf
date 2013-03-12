Ext.namespace('Crdppf');

// create layer tree and append nodes & subnodes to it
Crdppf.LayerTree = function createLayerTree () {
    this.makeLayerTree = makeLayerTree;
};
var makeLayerTree = function makeLayertree(){
    // create layer tree object
    overlaysList = [];
    layerTree = new Ext.tree.TreePanel({
        title: labels.layerTreeTitle,
        collapsible:true,
        flex: 1.0,
        useArrows:true,
        animate:true,
        lines: true,
        enableDD:false,
        autoScroll: true,
        rootVisible: false,
        frame: true,
        id: 'layerTree'
    });
    // define root node
    rootLayerTree = new Ext.tree.TreeNode({
        text: 'rootLayerTree',
        draggable:false,
        id:'rootLayerTree'});
    var ll = layerList.themes;
    // create a node on top of tree to select all nodes
    checkAllNode = new Ext.tree.TreeNode({
        text: labels.selectAllLayerLabel,
        id: 'selectAllNode',
        draggable: false,
        checked: false,
        leaf: true,
        listeners: {
            'checkchange':function(node,checked){
                if(checked){
                    layerTree.expandAll();
                    for (n=1; n < rootLayerTree.childNodes.length; n++){
                        rootLayerTree.childNodes[n].getUI().toggleCheck(true);
                    }
                    Ext.getCmp('infoButton').toggle(true);
                    MapO.setInfoControl();
                    
                }else{
                    for (n=1; n < rootLayerTree.childNodes.length; n++){
                            rootLayerTree.childNodes[n].getUI().toggleCheck(false);
                        }
                    layerTree.collapseAll();
                    Ext.getCmp('panButton').toggle(true);
                }
            }
        }
    });
    rootLayerTree.appendChild(checkAllNode);
    // iterate over themes and create nodes
    for (i=0;i<ll.length;i++){
        var themeId = ll[i].id;
        // fill tree with nodes relative to themes (level 1)
        var themeNode =  new Ext.tree.TreeNode({
            text: ll[i].name,
            draggable:false,
            id: ll[i].id,
            leaf: false,
            checked:false,
            listeners: {
                'checkchange': function(node, checked){
                    MapO.disableInfoControl();
                    if(checked){
                        node.expand();
                        for (k=0; k < node.childNodes.length; k++){
                            node.childNodes[k].getUI().toggleCheck(true);
                        }
                    }else{ 
                        node.collapse();
                        for (k=0; k < node.childNodes.length; k++){
                            node.childNodes[k].getUI().toggleCheck(false);
                        }
                }
                }
            }
        });
        // fill each theme node with his contained node (level 2)
        for (var keys in ll[i].layers)
        {
            var lName = ll[i].layers[keys];
            layerNode =  new Ext.tree.TreeNode({
                text: ll[i].layers[keys],
                draggable: false,
                id: keys,
                cls:'layerNodeCls',
                leaf: true,
                checked:false,
                listeners: {
                        'checkchange': function(node, checked){
                            if(checked){
                                overlaysList.push(node.id);
                                MapO.setOverlays();
                                Ext.getCmp('infoButton').toggle(true);
                                MapO.setInfoControl();
                            }else{
                                overlaysList.remove(node.id);
                                MapO.setOverlays();
                                Ext.getCmp('panButton').toggle(true);
                            }
                        }
                    }
                });
            themeNode.appendChild(layerNode);
        }
        rootLayerTree.appendChild(themeNode);
    }
    layerTree.setRootNode(rootLayerTree);
    return layerTree;
};