Ext.namespace('Crdppf');

Crdppf.legalDocuments = function(labels) {
/*
Function to collect all legal documents related to a selection of restrictions from the db
and create a data view applying a template to format the page layout
TODO: pass topic and layerfk to the function to request only related docs
*/
        var legaldocs = new Ext.data.JsonStore({
        autoDestroy: true,
        autoLoad: true,
        url: Crdppf.getLegalDocumentsUrl,
        sort: {
            field: 'doctype',
            direction: 'ASC'
        },
        //idProperty: 'documentid',
        fields:[
            {name: 'documentid', type:'integer'},
            {name: 'doctype'},
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
        '<h1 class="title" style="margin-bottom:10px;">Bases légales</h1>',
        '<tpl for=".">',
               '<tpl if="doctype == \'legalbase\'">',
                    '<tpl if="canton == null">',
                        '<h3 style="margin-left:10px;padding:3px">Niveau fédéral</h3>',
                    '</tpl>',
                    '<tpl if="canton == \'NE\' && commune== null">',
                        '<h3 style="margin-left:10px;padding:3px">Niveau cantonal</h3>',
                    '</tpl>',
                    '<tpl if="canton == \'NE\' && commune != null">',
                        '<h3 style="margin-left:10px;padding:3px">Niveau communal</h3>',
                    '</tpl>',
                    '<div style="margin-left:20px;padding:3px">',
                        '<h2 class="doctitle">{officialnb} - {officialtitle}</h2>',
                        '<p class="docurl"><b>URL:</b> <a href="#" onClick="window.open(\'{documenturl}\');" target="_blank">{documenturl}</a></p>',
                        '<br />',
                    '</div>',
                '</tpl>',
        '</tpl>',
        '<h1 class="title" style="margin-bottom:10px;">Dispositions juridiques</h1>',
        '<tpl for=".">',
               '<tpl if="doctype == \'legalprovision\'">',
                    '<tpl if="canton == null">',
                        '<h3 style="margin-left:10px;padding:3px">Niveau fédéral</h3>',
                    '</tpl>',
                    '<tpl if="canton == \'NE\' && commune== null">',
                        '<h3 style="margin-left:10px;padding:3px">Niveau cantonal</h3>',
                    '</tpl>',
                    '<tpl if="canton == \'NE\' && commune != null">',
                        '<h3 style="margin-left:10px;padding:3px">Niveau communal</h3>',
                    '</tpl>',
                    '<div style="margin-left:20px;padding:3px">',
                        '<h2 class="doctitle">{officialnb} - {officialtitle}</h2>',
                        '<p class="docurl"><b>URL:</b> <a href="{documenturl}" target="_blank">{documenturl}</a></p>',
                        '<br />',
                    '</div>',
                '</tpl>',
        '</tpl>',
        '<h1 class="title" style="margin-bottom:10px;">Références</h1>',
        '<tpl for=".">',
                    '<tpl if="canton == null && doctype == \'reference\'">',
                        '<h3 style="margin-left:10px;padding:3px">Niveau fédéral</h3>',
                    '</tpl>',
                    '<tpl if="canton == \'NE\' && commune== null && doctype == \'reference\'">',
                        '<h3 style="margin-left:10px;padding:3px">Niveau cantonal</h3>',
                    '</tpl>',
                    '<tpl if="canton == \'NE\' && commune != null && doctype == \'reference\'">',
                        '<h3 style="margin-left:10px;padding:3px">Niveau communal</h3>',
                    '</tpl>',
               '<tpl if="doctype == \'reference\'">',
                    '<div style="margin-left:20px;padding:3px">',
                        '<h2 class="doctitle">{officialnb} - {officialtitle}</h2>',
                        '<p class="docurl"><b>URL:</b> <a href="{documenturl}" target="_blank">{documenturl}</a></p>',
                        '<br />',
                    '</div>',
                '</tpl>',
        '</tpl>',
        //~ '<h1 class="title" style="margin-bottom:10px;">Dispositions transitoires</h1>',
        //~ '<tpl for=".">',
                    //~ '<tpl if="canton == null">',
                        //~ '<h3 style="margin-left:20px;padding:3px">Niveau fédéral</h3>',
                    //~ '</tpl>',
                    //~ '<tpl if="canton == \'NE\' && commune== null">',
                        //~ '<h3 style="margin-left:20px;padding:3px">Niveau cantonal</h3>',
                    //~ '</tpl>',
                    //~ '<tpl if="canton == \'NE\' && commune != null">',
                        //~ '<h3 style="margin-left:20px;padding:3px">Niveau communal</h3>',
                    //~ '</tpl>',
               //~ '<tpl if="doctype == \'temporaryprovision\'">',
                    //~ '<div style="margin-left:20px;padding:3px">',
                        //~ '<h2 class="doctitle">{officialnb} - {officialtitle}</h2>',
                        //~ '<p class="docurl"><b>URL:</b> <a href="{documenturl}" target="_blank">{documenturl}</a></p>',
                        //~ '<br />',
                    //~ '</div>',
                //~ '</tpl>',
        //~ '</tpl>',
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

    return legalInfo;

};

