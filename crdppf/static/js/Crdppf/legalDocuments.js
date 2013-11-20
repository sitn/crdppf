Ext.namespace('Crdppf');

Crdppf.legalDocuments = function() {
/*
Function to collect all legal documents related to a selection of restrictions from the db
and create a data view applying a template to format the page layout
TODO: pass topic and layerfk to the function to request only related docs
*/
        var legaldocs = new Ext.data.JsonStore({
        autoDestroy: true,
        autoLoad: true,
        url: 'getLegalDocuments',
        //idProperty: 'documentid',
        fields:[
            {name: 'documentid', type:'integer'},
            {name: 'numcom'},
            {name: 'topicfk'},
            {name: 'title'},
            {name: 'officialtitle'},
            {name: 'abreviation'}, 
            {name: 'officialnb'},
            {name: 'canton'},
            {name: 'commune'},
            {name: 'documenturl'},
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
        '<p class="docurl"><b>URL:</b> <a href="{documenturl}" target="_blank">{documenturl}</a></p>',
        '<br />',
        '</div>',
    '</tpl>',
    '</div>'
    );

    // Create the legal information container
    var legalInfo = new Ext.DataView({
        title: labels.legalBasisTab,
        store: legaldocs,
        tpl: templates,
        autoHeight: true,
        multiSelect: true,
        //overClass: 'x-view-over', - not used yet, might be nice so I leave it for now
        emptyText: 'No legal documents to display'
    });
    
    return legalInfo

};

