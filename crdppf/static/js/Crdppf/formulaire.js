Ext.onReady(function(){
	
	Ext.QuickTips.init();
    var winWait = new Ext.LoadMask(
        Ext.getBody(),
        {msg:"Veuillez patienter... chargement du formulaire."}
    );
    
     var fillform = function(response) {
        var results = Ext.decode(response.responseText);
        combostore.add(results); 
    };
 
    var combostore = new Ext.data.JsonStore({
        autoDestroy: true,
        autoLoad: true,
        url: 'getCadastreList',
        idProperty: 'idobj',
        fields:[
            {name: 'idobj'},
            {name: 'numcad', type:'integer'},
            {name: 'cadnom'},
            {name: 'numcom', type:'integer'},
            {name: 'comnom'},
            {name: 'nufeco',type:'integer'}
        ]
    }); 

    var cantons = new Ext.data.SimpleStore({
        autoDestroy: true,
        autoLoad: true,
        fields: [{name:'canton'}],
        data: [
            ['AG'],
            ['JU'],
            ['NE'],
            ['ZH']
        ]
    });

    var formulaire = new Ext.FormPanel({
        id: 'formulaire_saisie',
        title: 'Saisie des règlements',
        labelWidth: 200, 
        frame: true,
        bodyStyle: 'padding:5px 5px 0px',
        autoWidth: true,
        autoHeight: true,
        renderTo:'form',
        monitorValid: true,
        items: [{
                xtype:'numberfield',
                fieldLabel: 'Numéro de cadastre cantonal',
                labelStyle: 'white-space: nowrap;font-weight: bold;',
                store: combostore,
                displayField: 'numcad',
                valueField: 'numcad',
                name: 'numcad',
                allowBlank: false,
                width: 100,
                maxLength: 2
            },{
                xtype:'combo',
                store: combostore,
                displayField:'cadnom',
                valueField: 'cadnom',
                fieldLabel: 'Nom du cadastre',
                triggerAction: 'all',
                labelStyle: 'white-space: nowrap;font-weight: bold;',
                name: 'nomcad',
                allowBlank: false,
                width: 250,
                maxLength: 75,
                listeners : {
                    'select' : function(combo, record){
                    Ext.getCmp('formulaire_saisie').getForm().setValues(
                        {numcad:record.data.numcad,
                        numcom:record.data.numcom,
                        nufeco:record.data.nufeco,
                        comnom:record.data.comnom}
                        )
                    }
                }
            },{
                xtype:'numberfield',
                fieldLabel: 'Numéro de commune cantonal',
                labelStyle: 'white-space: nowrap;font-weight: bold;',
                name: 'numcom',
                allowBlank: false,
                width: 100,
                maxLength: 2
            },{
                xtype:'numberfield',
                fieldLabel: 'Numéro de commune fédéral',
                labelStyle: 'white-space: nowrap;font-weight: bold;',
                name: 'nufeco',
                allowBlank: false,
                width: 100,
                maxLength: 4
            },{
                xtype:'textfield',
                fieldLabel: 'Nom de la commune',
                labelStyle: 'white-space: nowrap;font-weight: bold;',
                name: 'comnom',
                allowBlank: false,
                width: 250,
                maxLength: 75
            },{
                xtype:'textfield',
                fieldLabel: 'Titre du document légal',
                labelStyle: 'white-space: nowrap;font-weight: bold;',
                name: 'titre',
                allowBlank: true,
                width: 500,
                maxLength: 255
            },{
                xtype:'textfield',
                fieldLabel: 'Titre officiel du document légal',
                labelStyle: 'white-space: nowrap;font-weight: bold;',
                name: 'titreofficiel',
                allowBlank: false,
                width: 500,
                maxLength: 255
            },{
                xtype:'textfield',
                fieldLabel: 'Abréviation',
                labelStyle: 'white-space: nowrap;font-weight: bold;',
                name: 'abreviation',
                allowBlank: false,
                width: 250,
                maxLength: 25
            },{
                xtype:'textfield',
                fieldLabel: 'Numéro officiel',
                labelStyle: 'white-space: nowrap;font-weight: bold;',
                name: 'noofficiel',
                allowBlank: false,
                width: 500,
                maxLength: 25
            },{
                xtype:'textfield',
                fieldLabel: 'Lien vers le document',
                labelStyle: 'white-space: nowrap;font-weight: bold;',
                name: 'url',
                allowBlank: false,
                width: 500,
                maxLength: 500
            },{
                xtype:'combo',
                fieldLabel: 'Statut juridique',
                store: new Ext.data.SimpleStore({
                    fields: ['status'],
                    data: [
                        ['En vigueur'],
                        ['En cours de modification']
                    ]
                }),
                displayField: 'status',   
                selectOnFocus: true,
                mode: 'local',
                triggerAction: 'all',
                labelStyle: 'white-space: nowrap;font-weight: bold;',
                name: 'statutjuridique',
                allowBlank: false,
                width: 250,
                maxLength: 100
            },{
                xtype:'datefield',
                fieldLabel: 'Date de sanction',
                labelStyle: 'white-space: nowrap;font-weight: bold;',
                name: 'datesanction',
                allowBlank: false,
                width: 250,
                maxLength: 100
            },{
                xtype:'datefield',
                fieldLabel: 'Date d\'abrogation',
                labelStyle: 'white-space: nowrap;font-weight: bold;',
                name: 'dateabrogation',
                allowBlank: false,
                width: 250,
                maxLength: 100
            },{
                xtype:'textfield',
                fieldLabel: 'Opérateur de saisie',
                labelStyle: 'white-space: nowrap;font-weight: bold;',
                name: 'operateursaisie',
                allowBlank: false,
                width: 250,
                maxLength: 100
            },{
                xtype:'datefield',
                fieldLabel: 'Date de saisie',
                labelStyle: 'white-space: nowrap;font-weight: bold;',
                name: 'datesaisie',
                allowBlank: false,
                width: 250,
                maxLength: 100
            },{
                xtype: 'combo',
                store:cantons,
                fieldLabel: 'Canton',
                displayField:'canton',
                labelStyle: 'white-space: nowrap;font-weight: bold;',
                name: 'canton',
                selectOnFocus: true,
                mode: 'local',
                allowBlank: false,
                width: 250,
                maxLength: 100
            },    
        ],

        buttons: [{
            text: 'Enregistrer',
            handler: function(){
                //~ add form validation
                var formvalues =formulaire.getForm().getValues();
                winWait.show();
                var transaction =Ext.Ajax.request({
                    url: 'createNewDocEntry',
                    method: 'POST',
                    params:{
                        data: Ext.encode(formvalues)
                    },
                    success:function(result,request) {
                        winWait.hide();
                        Ext.Msg.alert('Confirmation','Les données ont été enregistrées');
                    },
                    failure: function () {
                        winWait.hide();
                        Ext.Msg.alert('Error','Problème de serveur, veuillez contacter l\'administrateur.');
                    }
                });
            }
        },{
            text: 'Cancel'
        }]
    });

    
});