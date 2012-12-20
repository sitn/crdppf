<%inherit file="/base/index.mako"/>

<script type="text/javascript">

Ext.onReady(function(){
    Ext.QuickTips.init();
    
        var button = new Ext.Button({
        text: 'Créer l\'extrait',    
        renderTo: 'pdf',
    });
    
    Ext.get('pdf').on('click', function(){
        url = 'createExtrait';
        window.location = url;
	});
	
});


    
		  
</script>


<h1>Interface d'administration - Geoshop du SITN</h1>

<div id="pdf"></div>


