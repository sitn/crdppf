Ext.namespace('Crdppf');

// create layer tree and append nodes & subnodes to it
Crdppf.LayerTree = function createLayerTree () {
    this.makeLayerTree = makeLayerTree;
}
var makeLayerTree = function makeLayertree(){
    // create layer tree object
    overlaysList = [];
    layerTree = new Ext.tree.TreePanel({
        title: 'Table des matières',
        height: 300,
        width: 400,
        useArrows:true,
        autoScroll:true,
        animate:true,
        lines: true,
        enableDD:false,
        containerScroll: false,
        rootVisible: false,
        frame: true,
        id: 'layerTree'
    });
    // define root node
    rootLayerTree = new Ext.tree.TreeNode({
        text: 'rootLayerTree',
        draggable:false,
        id:'rootLayerTree'})
    ll = Crdppf.layerListFr.themes;
    // iterate over themes and create nodes
    for (i=0;i<ll.length;i++){
        var themeId = ll[i].id;
        var themeNode =  new Ext.tree.TreeNode({
            text: ll[i].name,
            draggable:false,
            id: ll[i].id,
            leaf: false,
            checked:false,
            listeners: {
                'checkchange': function(node, checked){
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
        })
        // iterate over layers and create subnodes
        for (var keys in ll[i].layers)
        {
            var lName = ll[i].layers[keys];
            layerNode =  new Ext.tree.TreeNode({
                text: ll[i].layers[keys],
                draggable: false,
                id: keys,
                leaf: true,
                checked:false,
                listeners: {
                        'checkchange': function(node, checked){
                            if(checked){
                                overlaysList.push(node.id)
                                MapO.setOverlays()
                            }else{
                                overlaysList.remove(node.id)
                                MapO.setOverlays()
                            }
                        }
                    }
                })
            themeNode.appendChild(layerNode)
        }
        rootLayerTree.appendChild(themeNode)
    }
    layerTree.setRootNode(rootLayerTree);
    return layerTree
}