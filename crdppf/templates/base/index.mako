## -*- coding: utf-8 -*-

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"
"http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
    <title>Cadastre des restrictions de droit public à la propriété foncière - Canton de Neuchâtel</title>
    <link href="http://www.ne.ch/neat/site/favico.ico" rel="shortcut icon" type="image/x-icon" />
    <link rel="stylesheet" href="${request.static_url('crdppf:static/lib/ext/resources/css/ext-all.css')}" type="text/css" media="screen" charset="utf-8" />
    <link rel="stylesheet" href="${request.static_url('crdppf:static/lib/ext/resources/css/xtheme-gray.css')}" type="text/css" media="screen" charset="utf-8" />
    <link rel="stylesheet" href="${request.static_url('crdppf:static/css/main.css')}" type="text/css" media="screen" charset="utf-8" />
    <link rel="stylesheet" href="${request.static_url('crdppf:static/css/banner.css')}" type="text/css" media="screen" charset="utf-8" />
    <link rel="stylesheet" href="${request.static_url('crdppf:static/lib/ext/resources/ux/gridfilters/css/GridFilters.css')}" type="text/css" media="screen" charset="utf-8" />
    <link rel="stylesheet" href="${request.static_url('crdppf:static/lib/ext/resources/ux/gridfilters/css/RangeMenu.css')}" type="text/css" media="screen" charset="utf-8" />
    <link rel="stylesheet" type="text/css" href="${request.static_url('crdppf:static/lib/openlayers/theme/default/style.css')}" />
    ${self.js()}

    <!-- Load globals -->
    <script type="text/javascript" src="${request.route_url('globalsjs')}"></script>
    

</head>
    
<body>
    <div id="header">
        <table width="100%">
            <tr>
                <td align="left" valign="top">
                    <img src="${request.static_url('crdppf:static/images/banniere_crdppf_.png')}" alt=""/>                </td>
                <td rowspan="2" align="right" valign="top">
                    <a href="http://www.ne.ch" target="_blank"><img src="${request.static_url('crdppf:static/images/sitn_banniere_final_right_.png')}" alt="" /></a>                </td>
            </tr>
            <tr valign="top" >
              <td align="left" valign="top" height="60">
                <span class="Style1">&nbsp;
                <a class="banner2" href="http://www.ne.ch/sitn" target="_blank">Accueil</a> - 
                <a class="banner2" href="http://www.ne.ch/sitn/themes" target="_blank">Thèmes</a> - 
                <a class="banner2" href="http://www.ne.ch/sitn/donnees" target="_blank">Géodonnées</a> - 
                <a class="banner2" href="http://www.ne.ch/neat/site/jsp/rubrique/rubrique.jsp?StyleType=bleu&CatId=12523" target="_blank">Géoservices</a> - 
                <a class="banner2" href="http://sitn.ne.ch/" target="_blank">Géoportail</a> - 
                <a class="banner2" href="http://sitn.ne.ch/mobile" target="_blank">Géoportail mobile</a> - 
                <a class="banner2" href="http://sitn.ne.ch/sitn_php/divers/liens_cartographiques.html" target="_blank">Liens cartographiques</a> - 
                <a class="banner2" href="mailto:sitn@ne.ch?subject=Nouveau Geoportail SITN" target="_blank">Contact</a> - 
                <a class="banner2" href="" id="frLink">Fr</a> /
                <a class="banner2" href="" id="deLink">De</a>
        </span>
        </td>
          </tr>
        </table>
      </div>
    
% if debug:
    <p>debug:ok</p>
% endif
    ${next.body()}

</body>
</html>

<%def name="title()">SimpleSite</%def>

<%def name="js()">
    <script src="${request.static_url('crdppf:static/lib/ext/adapter/ext/ext-base-debug.js')}" type="text/javascript"></script>
    <script src="${request.static_url('crdppf:static/lib/ext/ext-all-debug.js')}" type="text/javascript"></script>

  <!--  <script src="${request.static_url('crdppf:static/lib/ext/adapter/ext/ext-base.js')}" type="text/javascript"></script>-->
   <!-- <script src="${request.static_url('crdppf:static/lib/ext/ext-all.js')}" type="text/javascript"></script> -->

  
    <script src="${request.static_url('crdppf:static/lib/ext/src/locale/ext-lang-fr.js')}" type="text/javascript"></script>
    
    <!-- <script src="${request.static_url('crdppf:static/lib/ext/resources/ux/statusbar/statusBar.js')}" type="text/javascript"></script> -->
    
</%def>