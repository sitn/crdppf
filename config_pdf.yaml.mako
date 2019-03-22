# WMTS server urls
wmts_openlayers:
  mapproxyurl: [
        'https://tile1-sitn.ne.ch/mapproxy95/wmts',
        'https://tile2-sitn.ne.ch/mapproxy95/wmts',
        'https://tile3-sitn.ne.ch/mapproxy95/wmts',
        'https://tile4-sitn.ne.ch/mapproxy95/wmts',
        'https://tile5-sitn.ne.ch/mapproxy95/wmts'
    ]

app_config:
  # defaultfontfamily: Arial
  # topics provided by the confederation
  ch_topics: ['R087','R096','R097','R103','R104','R108','R118','R119']
  # federal topics with certificate but empty no content/layers
  emptytopics: ['R088','R117']

  # wms and feature service name of the layers used by the confederation
  ch_legend_layers:
    'R087': ch.astra.projektierungszonen-nationalstrassen.oereb
    'R096': ch.bav.projektierungszonen-eisenbahnanlagen.oereb
    'R097': ch.bav.baulinien-eisenbahnanlagen.oereb
    'R103': ch.bazl.projektierungszonen-flughafenanlagen.oereb
    'R104': ch.bazl.baulinien-flughafenanlagen.oereb
    'R108': ch.bazl.sicherheitszonenplan.oereb
    'R118': ch.bazl.kataster-belasteter-standorte-zivilflugplaetze.oereb
    'R119': ch.bav.kataster-belasteter-standorte-oev.oereb

  #  configuration and list of the wms layers used for the background image in the pdf
  crdppf_wms_layers:
    - cantons_situation
    - frontiere_pays_situation
    - surfaces_tot
    - surfaces_bois
    - batiments_souterrain
    - batiments
    - parcellaire_officiel
    - immeubles_txt_rappel
    - immeubles_txt
    - mo9_immeubles_txt_conc_hydr
    - pts_limites
    - obj_divers_couvert
    - obj_divers_cordbois
    - obj_divers_piscine
    - obj_divers_batsout15m
    - obj_divers_lineaire
    - obj_divers_surface_lig
    - obj_divers_ponctuels
    - pts_fixes
    - voie_adresse
    - nomenclature_lieux
  map_buffer: 1.3

  # coordinate system to be used by the wms
  wms_srs: EPSG:2056
  # version of the wms
  wms_version: 1.1.1
  # default transparency setting of the wms
  wms_transparency: 'TRUE'
  # default image format of the wms
  wms_imageformat: image/png
 
# Parameters for the PDF extract layout - only modify if you know what you do (may affect the layout)!! 
pdf_config:
  # default language of the pdf extract
  defaultlanguage: ${default_language}
  # Page format of the PDF extract
  pdfformat: A4
  # Page orientation of the PDF extract
  pdforientation: portrait
  # left margin
  leftmargin: 25
  # right margin
  rightmargin: 25
  # top margin for text
  topmargin: 55
  # margin from header for the map placement
  headermargin: 50
  footermargin: 20
  # Default text font
  fontfamily: Arial
  # text formats : b = bold, n= normal, i=italic ; size in pt
  textstyles:
    title1: [B, 22]
    title2: [B, 18]
    title3: [B, 16]
    normal: [N, 10]
    bold: [B,10]
    url: [N,10]
    small: [N, 7]
    tocbold: [B, 11]
    tocurl: [N, 9]
    tocnormal: [N, 11]
  # color for links - default is standard blue
  urlcolor: [0, 0, 255]
  # default color for text - black
  defaultcolor: [0, 0, 0]
  # Max ratio property bbox/map bbox - to insure that the property occupies at most 90% of the map and leaves 10% space around it
  fitratio: 0.9
  # path to the logo of the confederation
  CHlogopath: ecussons/Logo_Schweiz_Eidgen.png
  # path to the logo of the confederation
  crdppflogopath: ecussons/cadastrerdppfargb.png
  # path and dimensions in mm of cantonal logo
  cantonlogo:
    path: ecussons/06ne_ch_RVB.jpg
    width: 43.4
    height: 13.8
  
  # Default image file for missing armories picture of a municipality
  placeholder: Placeholder.jpg
  
  # Default base name for the PDF extract
  pdfbasename: _ExtraitCRDPPF
  
  # Default prefix/suffix for all the basemap files to ditinguish them from topic files
  siteplanbasename: _siteplan
  
  # Activates (true) or not cantonal and other optional topics (to be specified in crdppfportal/models.py)
  optionaltopics: false
  
  # Activates the signature block on the title pageof the PDF 
  # - IF and ONLY IF the report type is set to certified/reducedcertified
  signature: false
  
  # Allows to activate (true) or deactivate pilote phase text
  pilotphase: false
  
  # Activates (true) or not the disclaimer text on the title page of the PDF
  disclaimer: true

# URL to localhost Tomcat server webapp
print_url: http://localhost:8080/print-${instanceid}/print

# URL to internal instance
localhost_url: http://localhost/${instanceid}

# URL to internal MapServer instance
mapserver_url: http://localhost/${instanceid}/wmscrdppf

# URL to WMTS getCapabilities
wmts_getcapabilities_url: https://sitn.ne.ch/mapproxy95/service/?SERVICE=WMTS&REQUEST=GetCapabilities&VERSION=1.0.0

# Path to PDF extract archive folder - optional: if variable is ommited there will be no backup
pdf_archive_path: ${archive_path}
