Ext.namespace('Crdppf');

// create layer tree and append nodes & subnodes to it
Crdppf.legalDocuments = function() {
/*
Function to collect all legal documents related to a selection of restrictions
TODO: pass topic and layerfk to the function to request only related docs
*/
        var legaldocs = new Ext.data.JsonStore({
        autoDestroy: true,
        autoLoad: true,
        url: 'getLegalDocuments',
        idProperty: 'legalbaseid',
        fields:[
            {name: 'legalbaseid', type:'integer'},
            {name: 'numcom'},
            {name: 'topicfk'},
            {name: 'officialtitle'},
            {name: 'abreviation'}, 
            {name: 'officialnb'},
            {name: 'canton'},
            {name: 'commune'},
            {name: 'legalbaseurl'},
            {name: 'legalstate'},
            {name: 'publishedsince', type:'date'}
        ]
    });

    // Parse the legal documents and apply the corresponding template
    var templates = new Ext.XTemplate(
    '<div class="legaldocs" style="margin:5px">',
    '<tpl for=".">',
        '<div style="padding:3px">',
        '<h2 class="doctitle">{officialnb} - {officialtitle}</h2>',
        '<p class="docurl"><b>URL:</b> <a href="{legalbaseurl}" target="_blank">{legalbaseurl}</a></p>',
        '</div>',
    '</tpl>',
    '</div>',
    '<div class="x-clear"></div>'
    );

    // Create the legal information container
    var legalInfo = new Ext.DataView({
        title: labels.legalBasisTab,
        store: legaldocs,
        tpl: templates,
        autoHeight:true,
        multiSelect: true,
        overClass:'x-view-over',
        itemSelector:'div.thumb-wrap',
        emptyText: 'No legal documents to display'
    });
    
    return legalInfo

};

