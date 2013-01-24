/*
 * @include Crdppf/map.js
 */

var mapPanel;

Ext.onReady(function(){
  
    Ext.QuickTips.init();

    // create map
    var map = Crdppf.map;
    Crdppf.setOverlays('73')
        
    var crdppf = new Ext.Viewport({
        layout: 'border',
        renderTo:'main',
        items: [{
            region: 'north',
            height: 55,
            border: false,
            contentEl: 'header'
        }, {
            region: 'west',
            collapsible: true,
            title: 'Navigation',
            width: 300,
            layout: 'accordion',
            items:[{
                title: 'Vue d\'ensemble des restrictions disponibles',
                id: '0',
                html: 'arborescence complète'
            },{
                title: '73 - <b style=\'color:orange;\'>Plans d\'affectation - Pas disponible</b>',
                id: '73',
                html: '<h3>Service compétent : SAT</h3><p>Adresse</p><h3>Bases légales : RS xyz</h3><h3>Données publiées depuis : 01.01.2013</h3>'
            },{
                title: '79 - <b style=\'color:red;\'>Chemins pour piétons - pas concerné</b>',
                html: 'Content'
            },{
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
                html: 'Content'
            },{
                title: '104 - Alignements des installations aéroportuaires',
                html: 'Content'
            },{
                title: '108 - Carte et liste des obstacles à la navigation aérienne',
                html: 'Content'
            },{
                title: '116 - Cadastre des sites pollués',
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
          }, {
            region: 'south',
            title: 'Disclaimer',
            collapsible: true,
            border:false,
            html: 'Mise en garde : Le canton de Neuchâtel n\'engage pas sa responsabilité sur l\'exactitude ou la fiabilité des documents législatifs dans leur version électronique. Ces documents ne créent aucun autre droit ou obligation que ceux qui découlent des textes légalement adoptés et publiés, qui font seuls foi.',
            split: true,
            height: 100,
            minHeight: 100
        }, {
            region: 'east',
            title: 'Légende',
            width: 300,
            html: '<h3>Je suis la légende</h3>',
            collapsible: true,
            split: true
        }, {
            region: 'center',
            xtype: 'tabpanel',
            activeTab: 0, // index or id
            items:[{
                id: 'mappanel',
                title: 'Carte',
                xtype: 'gx_mappanel',
                zoom: 1,
                map: map
            },{
                title: 'Bases légales',
                html: 'une base légale'
            },{
                title: 'Règlements',
                html: 'un règlement communal'
            },{
                title: 'Informations et renvois supplémentaires',
                html: 'une information complémentaire'
            }]
        }]
    });
    mapPanel = Ext.getCmp('mappanel');    
	// Refait la mise en page si la fenêtre change de taille
	//pass along browser window resize events to the panel
	Ext.EventManager.onWindowResize(crdppf.doLayout,crdppf);
    
});