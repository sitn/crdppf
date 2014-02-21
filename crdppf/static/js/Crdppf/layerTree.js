Ext.namespace('Crdppf');

// create layer tree and append nodes & subnodes to it
Crdppf.LayerTree = function(labels, layerList, baseLayersList) {
    // create layer tree object
    overlaysList = [];
    var layerTree = new Ext.tree.TreePanel({
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
    var rootLayerTree = new Ext.tree.TreeNode({
        text: 'rootLayerTree',
        draggable:false,
        id:'rootLayerTree'});
    var ll = layerList.themes;

    // create a node on top of tree to select all nodes
    var checkAllNode = new Ext.tree.TreeNode({
        text: labels.selectAllLayerLabel,
        id: 'selectAllNode',
        draggable: false,
        cls:'checkAllNodeCls',
        checked: false,
        leaf: true,
        listeners: {
            'checkchange': function(node,checked){
                if(checked){
                    layerTree.expandAll();
                    for (n=1; n < rootLayerTree.childNodes.length; n++){
                        if( rootLayerTree.childNodes[n].id != 'baseLayers') {
                            rootLayerTree.childNodes[n].getUI().toggleCheck(true);
                        }
                    }
                    Ext.getCmp('infoButton').toggle(true);
                    MapO.setInfoControl();
                    
                }else{
                    for (n=1; n < rootLayerTree.childNodes.length; n++){
                        if( rootLayerTree.childNodes[n].id != 'baseLayers') {
                            rootLayerTree.childNodes[n].getUI().toggleCheck(false);
                        }
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
            text: labels[ll[i].name],
            draggable: false,
            id: ll[i].id,
            leaf: false,
            checked: false,
            listeners: {
                'checkchange': function(node, checked){
                    MapO.disableInfoControl();
                    if (checked){
                        node.expand();
                        for (k=0; k < node.childNodes.length; k++){
                            node.childNodes[k].getUI().toggleCheck(true);
                        }
                    } else { 
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
            layerNode =  new Ext.tree.TreeNode({
                text: labels[keys],
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
    
    // Top node of the base layers group
    var baseLayersNode = new Ext.tree.TreeNode({
        text: labels.baseLayerGroup,
        cls:'baseLayersNodeCls',
        id: 'baseLayers',
        draggable: false,
        leaf: false,
        expanded: true
    });
    
    // create nodes for base layers
    
    var baseLayers = baseLayersList.baseLayers;
    
    // iterate over base layers and create nodes
    for (var i=0;i<baseLayers.length;i++){
        // default: check first layer
        isChecked = false;
        if (i == 0){
            isChecked = true;
        }
        
        // fill tree with nodes relative to baseLayers
        var baseLayerItem =  new Ext.tree.TreeNode({
            text: labels[baseLayers[i].name],
            draggable:false,
            id: baseLayers[i].wmtsname,
            leaf: true,
            checked: isChecked,
            cls: 'baseLayerNodeCls',
            listeners: {
                'checkchange': function(node, checked){
                    if(checked){
                        for (var k=0; k < node.parentNode.childNodes.length; k++){
                            if(node.parentNode.childNodes[k].id != node.id){
                                node.parentNode.childNodes[k].getUI().toggleCheck(false);
                            } else {
                                // set new backgound layer
                                 var theBaseLayer = MapO.map.getLayersBy('id', 'baseLayer')[0];
                                 if(theBaseLayer) {
                                    theBaseLayer.destroy();
                                 }
                                var format = "image/png";
                                var formatSuffixMap = {'image/png':'png'};
                                
                                if (node.id == 'ortho2011'){
                                    format = "image/jpeg";
                                    formatSuffixMap = {'image/jpeg':'jpeg'};
                                }
                                
                                var layer = new OpenLayers.Layer.WMTS({
                                    name: "Base layer",
                                    url: Crdppf.mapproxyUrl,
                                    layer: node.id,
                                    matrixSet: 'swiss_grid_new',
                                    format: format,
                                    formatSuffixMap: formatSuffixMap,
                                    isBaseLayer: true,
                                    style: 'default',
                                    fixedLayer: true,
                                    requestEncoding: 'REST'
                                }); 

                                layer.id = 'baseLayer';
                                MapO.map.addLayers([layer]);
                                layer.redraw();
                            }
                        }
                    }
                }
            }
        });
        baseLayersNode.appendChild(baseLayerItem);
    }
    
    rootLayerTree.appendChild(baseLayersNode);
    layerTree.setRootNode(rootLayerTree);
    
    return layerTree;
};
