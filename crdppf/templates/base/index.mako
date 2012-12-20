## -*- coding: utf-8 -*-

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"
"http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
    <title>Cadastre des restrictions de droit public à la propriété foncière - Canton de Neuchâtel</title>
    <link href="http://www.ne.ch/neat/site/favico.ico" rel="shortcut icon" type="image/x-icon" />
    <link rel="stylesheet" href="${request.static_url('crdppf:static/js/ext/resources/css/ext-all.css')}" type="text/css" media="screen" charset="utf-8" />
    <link rel="stylesheet" href="${request.static_url('crdppf:static/js/ext/resources/css/xtheme-gray.css')}" type="text/css" media="screen" charset="utf-8" />
    <link rel="stylesheet" href="${request.static_url('crdppf:static/css/main.css')}" type="text/css" media="screen" charset="utf-8" />
    <link rel="stylesheet" href="${request.static_url('crdppf:static/css/banner.css')}" type="text/css" media="screen" charset="utf-8" />
    <link rel="stylesheet" href="${request.static_url('crdppf:static/js/resources/ux/gridfilters/css/GridFilters.css')}" type="text/css" media="screen" charset="utf-8" />
    <link rel="stylesheet" href="${request.static_url('crdppf:static/js/resources/ux/gridfilters/css/RangeMenu.css')}" type="text/css" media="screen" charset="utf-8" />
    ${self.js()}
    <script type="text/javascript">
        var baseUrl = "${request.route_url('home')}";
    </script>
</head>
    
<body>
    <div id="header">
        <table width="100%">
            <tr>
                <td align="left" valign="top">
                    <img src="${request.static_url('crdppf:static/images/sitn_banniere_final_left.png')}" alt="" align="top" />                </td>
                <td rowspan="2" align="right">
                    <img src="${request.static_url('crdppf:static/images/sitn_banniere_final_right.png')}" alt="" />                </td>
            </tr>
            <tr valign="top">
              <td height="20" align="left" valign="top">
                <span class="Style1">&nbsp;
                <a href="http://www.ne.ch/sitn" target="_blank">Accueil</a> - 
                <a href="http://www.ne.ch/sitn/themes" target="_blank">Th&egrave;mes</a> - 
                <a href="http://www.ne.ch/sitn/donnees" target="_blank">G&eacute;odonn&eacute;es</a> - 
                <a href="http://www.ne.ch/neat/site/jsp/rubrique/rubrique.jsp?StyleType=bleu&CatId=12523" target="_blank">G&eacute;oservices</a> - 
                <a href="http://sitn.ne.ch/" target="_blank">G&eacute;oportail</a> - 
                <a href="http://sitn.ne.ch/mobile" target="_blank">G&eacute;oportail mobile</a> - 
                <a href="http://sitn.ne.ch/sitn_php/divers/liens_cartographiques.html" target="_blank">Liens cartographiques</a> - 
                <a href="mailto:sitn@ne.ch?subject=Nouveau Geoportail SITN" target="_blank">Contact</a>
        </span>
        </td>
          </tr>
        </table>
      </div>
     
          <br /><br />
    <h1>Cadastre des restrictions de droit public à la propriété foncière - Canton de Neuchâtel</h1>
% if debug:
    <p>J'ai réussi le debug...</p>
% endif


</body>
</html>

<%def name="title()">SimpleSite</%def>

<%def name="js()">
    <script src="${request.static_url('crdppf:static/js/ext/adapter/ext/ext-base.js')}" type="text/javascript"></script>
    <script src="${request.static_url('crdppf:static/js/ext/ext-all.js')}" type="text/javascript"></script> 
   <script src="${request.static_url('crdppf:static/js/ext/ext-all-debug.js')}" type="text/javascript"></script>
    <script src="${request.static_url('crdppf:static/js/ext/src/locale/ext-lang-fr.js')}" type="text/javascript"></script>
</%def>