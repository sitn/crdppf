MAP
NAME CRDPPF
STATUS ON
SIZE 400 300
UNITS METERS
TRANSPARENT on
MAXSIZE 4096
SYMBOLSET "crdppf.sym"
FONTSET fonts.txt

#CONFIG "MS_ERRORFILE" "/tmp/ms.log"
DEBUG 3
EXTENT ${mapExtentMinX} ${mapExtentMinY} ${mapExtentMaxX} ${mapExtentMaxY}

WEB
  IMAGEPATH "/tmp"
  METADATA
    "ows_title"                         "CRDPPF OWS server"
    "ows_enable_request"          "*"
    "wfs_encoding"                   "utf-8"
    "wms_title"                        "${instanceid} WMS Server"
    "wms_onlineresource"          "http://${host}/${instanceid}/wmscrdppf"
    "wms_srs"                         "EPSG:2056"
  END
END

IMAGETYPE png24
IMAGECOLOR 255 255 255
TRANSPARENT OFF

RESOLUTION 200
DEFRESOLUTION 200

OUTPUTFORMAT
  NAME png24
  DRIVER "AGG/PNG"
  MIMETYPE "image/png"
  IMAGEMODE "RGB"
  EXTENSION "png"
END

OUTPUTFORMAT
  NAME jpeg
  DRIVER "AGG/JPEG"
  MIMETYPE "image/jpeg"
  EXTENSION "jpeg"
  FORMATOPTION QUALITY=88
END

PROJECTION
  "init=epsg:2056"   ##required
END

LEGEND
 STATUS ON        # Draw legend in the map
 KEYSIZE 17 10      # Define the size of the legend icon.
 LABEL            # Used only for embedded legend (in the map)
   TYPE TRUETYPE
   FONT "verdana"
   COLOR 0 0 0
   SIZE 8
   ANTIALIAS TRUE
 END
END


 # A scalebar object is defined one level below the map object.  This object
  # controls how a scalebar is drawn by MapServer.  Scalebars can be embedded
  # in the map itself or can be created as a separate image.  It has an
  # associated MapServer CGI variable called "scalebar" (or [scalebar] when
  # used in the HTML template).
  SCALEBAR
    IMAGECOLOR 255 255 255
    LABEL
      COLOR 0 0 0
      SIZE SMALL
    END
    STYLE 0
    SIZE 300 10
    COLOR 0 0 0
    UNITS METERS
    INTERVALS 5
    TRANSPARENT FALSE
    STATUS OFF
  END # Scalebar object ends

LAYER
  NAME "parcelles"
  TYPE POLYGON
  CONNECTIONTYPE POSTGIS
  CONNECTION "user=${dbuser} password=${dbpassword} dbname=${db} host=${dbhost} port=${dbport}"
  PROCESSING "CLOSE_CONNECTION=DEFER"
  DATA "geom from mensuration.mo9_immeubles using unique idobj using srid=2056"
  STATUS ON
  TEMPLATE "foo"
  CLASS
    NAME "name1"
    STYLE
      OUTLINECOLOR 120 120 0
    END
  END
  METADATA
    "ows_title" "parcelles"
    "wms_srs" "EPSG:2056"
    "wfs_enable_request" "*"
    "gml_types" "auto"
    "gml_include_items" "id,idemai,cadastre,nummai,typimm,srfmai,nufeco,valide"
  END
  PROJECTION
    "init=epsg:2056"   ##required
  END
  MINSCALEDENOM 0
  MAXSCALEDENOM 25001
END

######################
# RESTRICTIONS CRDPPF - début
######################

LAYER
  NAME "r73_contenus_ponctuels"
  TYPE POINT
   METADATA
       "ows_title"                    "r73_contenus_ponctuels"
       "wms_srs"                     "EPSG:2056"
       "wms_title"                   "${instanceid} WMS Server"
       "wms_onlineresource"     "http://${host}/${instanceid}/wmscrdppf"
       "wms_srs"                    "EPSG:2056"
  END
  CONNECTIONTYPE POSTGIS
  CONNECTION "user=${dbuser} password=${dbpassword} dbname=${db} host=${dbhost} port=${dbport}"
  PROCESSING "CLOSE_CONNECTION=DEFER"
  DATA "geom from crdppf.r73_contenus_ponctuels using unique idobj using srid=2056"
  STATUS ON
  CLASSITEM "codegenre"
  OPACITY 60
  TEMPLATE "ttt"
  CLASS
    NAME "Bloc erratique"
    EXPRESSION /8101/
    SYMBOL "square"
    COLOR 155 0 0
    SIZE 5
  END
  CLASS
    NAME "Arbre isolé"
    EXPRESSION /8102/
    SYMBOL "circle"
    COLOR 0 180 0
    SIZE 8
  END
  CLASS
    NAME "Bâtiment intéressant"
    EXPRESSION /8201/
    SYMBOL "patrimoine_architectural"
    MINSIZE 10
    SIZE 10
    MAXSIZE 10
    COLOR 255 115 66
    OUTLINECOLOR 132 0 0
  END
  CLASS
    NAME "Bâtiment typique ou pittoresque"
    EXPRESSION /8202/
    SYMBOL "patrimoine_architectural"
    MINSIZE 10
    SIZE 10
    MAXSIZE 10
    COLOR 0 200 0
    OUTLINECOLOR 132 0 0
  END
  CLASS
    NAME "Bâtiment intéressant"
    EXPRESSION /8201/
    SYMBOL "patrimoine_architectural"
    MINSIZE 10
    SIZE 10
    MAXSIZE 10
    COLOR 255 115 66
    OUTLINECOLOR 132 0 0
  END
  CLASS
    NAME "Bâtiment perturbant"
    EXPRESSION /8203/
    SYMBOL "patrimoine_architectural"
    MINSIZE 10
    SIZE 10
    MAXSIZE 10
    COLOR 180 0 0
    OUTLINECOLOR 132 0 0
  END
  TOLERANCE 8
  TOLERANCEUNITS pixels
END

LAYER
  NAME "r73_contenus_lineaires"
  TYPE LINE
   METADATA
       "ows_title"                   "r73_contenus_lineaires"
       "wms_srs"                    "EPSG:2056"
       "wms_title"                  "${instanceid} WMS Server"
       "wms_onlineresource"    "http://${host}/${instanceid}/wmscrdppf"
       "wms_srs"                   "EPSG:2056"
  END
  CONNECTIONTYPE POSTGIS
  CONNECTION "user=${dbuser} password=${dbpassword} dbname=${db} host=${dbhost} port=${dbport}"
  PROCESSING "CLOSE_CONNECTION=DEFER"
  DATA "geom from crdppf.r73_contenus_lineaires using unique idobj using srid=2056"
  STATUS ON
  CLASSITEM "codegenre"
  OPACITY 60
  TEMPLATE "ttt"
  # Limites à la construction
  CLASS
    NAME "Limite surfaces eaux"
    EXPRESSION /7101/
    STYLE
      OUTLINECOLOR 0 0 255
      WIDTH 2
    END
  END
  CLASS
    NAME "Terr. en nature de vigne"
    EXPRESSION /7102/
    STYLE
        PATTERN 4 4 END
        WIDTH 2
        COLOR 100 100 100
    END
  END
  CLASS
    NAME "Limite zone viticole"
    EXPRESSION /7103/
    STYLE
        PATTERN 4 4 END
        WIDTH 2
        COLOR 255 0 255
    END
  END
  CLASS
    NAME "Limite à la forêt"
    EXPRESSION /7104/
    STYLE
        PATTERN 4 4 END
        WIDTH 2
        COLOR 0 140 0
    END
  END
  # Objets protégés
  CLASS
    NAME "Objet protégé - Haie"
    EXPRESSION /7901/
    STYLE
      OUTLINECOLOR 0 155 0
      WIDTH 2
    END
  END
  CLASS
    NAME "Objet protégé - Mur de pierres sèches"
    EXPRESSION /7902/
    STYLE
      OUTLINECOLOR 180 100 100
      WIDTH 2
    END
  END
  CLASS
    NAME "Objet protégé - Allée d'arbres"
    EXPRESSION /7903/
    STYLE
      OUTLINECOLOR 0 90 0
      WIDTH 2
    END
  END
  CLASS
    NAME "Objet protégé 2 - Haie"
    EXPRESSION /7904/
    STYLE
      OUTLINECOLOR 0 190 0
      WIDTH 2
    END
  END
  CLASS
    NAME "Objet protégé 2 - Mur de pierres sèches"
    EXPRESSION /7905/
    STYLE
      OUTLINECOLOR 140 80 80
      WIDTH 2
    END
  END
END

LAYER
  NAME "r73_perimetres_superposes"
  TYPE LINE
   METADATA
       "ows_title"                  "r73_perimetres_superposes"
       "wms_srs"                   "EPSG:2056"
       "wms_title"                  "${instanceid} WMS Server"
       "wms_onlineresource"    "http://${host}/${instanceid}/wmscrdppf"
       "wms_srs"                   "EPSG:2056"
  END
  CONNECTIONTYPE POSTGIS
  CONNECTION "user=${dbuser} password=${dbpassword} dbname=${db} host=${dbhost} port=${dbport}"
  PROCESSING "CLOSE_CONNECTION=DEFER"
  DATA "geom from crdppf.r73_perimetres_superposes using unique idobj using srid=2056"
  STATUS ON
  CLASSITEM "codegenre"
  OPACITY 90
  TEMPLATE "ttt"
  CLASS
    NAME "Perim. plan spéc. en vigueur"
    EXPRESSION /6101/
    STYLE
      OUTLINECOLOR 255 0 255
      COLOR 0 255 0
      WIDTH 5
    END
  END
  CLASS
    NAME "Perim. plan spéc. obl. pas en vigueur"
    EXPRESSION /6201/
    STYLE
      OUTLINECOLOR 255 0 255
      COLOR 255 0 0
      WIDTH 5
    END
  END
  CLASS
    NAME "Perim. étape équipement différée"
    EXPRESSION /6301/
    STYLE
      OUTLINECOLOR 255 0 255
      COLOR 0 0 255
      WIDTH 5
    END
  END
  CLASS
    NAME "Objet protégé - Bosquet"
    EXPRESSION /6901/
    STYLE
      OUTLINECOLOR 0 155 0
      COLOR 0 155 0
      WIDTH 2
    END
  END
  CLASS
    NAME "Objet protégé - Doline"
    EXPRESSION /6902/
    STYLE
      OUTLINECOLOR 150 0 0
      COLOR 150 0 0
      WIDTH 2
    END
  END
    CLASS
    NAME "Objet protégé - Surface eau"
    EXPRESSION /6903/
    STYLE
      OUTLINECOLOR 0 0 255
      COLOR 0 0 255
      WIDTH 2
    END
  END
  CLASS
    NAME "Secteur de sites éoliens"
    EXPRESSION /6904/
    STYLE
        PATTERN 6 12 END
        OUTLINECOLOR 0 0 220
        WIDTH 4
    END
  END
  CLASS
    NAME "Périmètre soumis à PD"
    EXPRESSION /6905/
    STYLE
        PATTERN 6 10 END
        OUTLINECOLOR 0 0 0
        WIDTH 3
    END
  END
  CLASS
    NAME "Périmètre PD en vigueur"
    EXPRESSION /6906/
    STYLE
        PATTERN 6 4 END
        OUTLINECOLOR 0 0 0
        WIDTH 3
    END
  END
  CLASS
    NAME "Périmètre soumis à PDQ"
    EXPRESSION /6907/
    STYLE
        PATTERN 15 15 END
        OUTLINECOLOR 0 0 0
        WIDTH 4
    END
  END
  CLASS
    NAME "Périmètre  PDQ en vigueur"
    EXPRESSION /6908/
    STYLE
        PATTERN 15 7 END
        OUTLINECOLOR 0 0 0
        WIDTH 4
    END
  END
  CLASS
    NAME "Périmètre soumis à PQ"
    EXPRESSION /6909/
    STYLE
        PATTERN 15 15 END
        OUTLINECOLOR 0 0 0
        WIDTH 2
    END
  END
  CLASS
    NAME "Périmètre PQ en vigueur"
    EXPRESSION /6910/
    STYLE
        PATTERN 15 7 END
        OUTLINECOLOR 0 0 0
        WIDTH 2
    END
  END
  CLASS
    NAME "Périmètre de plan spécial"
    EXPRESSION /6911/
    STYLE
        PATTERN 15 3 3 3 END
        OUTLINECOLOR 0 0 0
        WIDTH 2
    END
  END
  CLASS
    NAME "Objet protégé 2 - Verger"
    EXPRESSION /6912/
    STYLE
      OUTLINECOLOR 0 180 0
      COLOR 0 220 0
      WIDTH 2
    END
  END
  CLASS
    NAME "Objet protégé 2 - Bosquet"
    EXPRESSION /6913/
    STYLE
      OUTLINECOLOR 0 155 0
      COLOR 0 155 0
      WIDTH 2
    END
  END
  CLASS
    NAME "Objet protégé 2 - Doline"
    EXPRESSION /6914/
    STYLE
      OUTLINECOLOR 150 0 0
      COLOR 150 0 0
      WIDTH 2
    END
  END
  CLASS
    NAME "Secteur indicatif de dangers -Glissements"
    EXPRESSION ([codegenre] = 6915 AND '[teneur]' eq 'Glissements')
    OUTLINECOLOR 255 190 189
  END
  CLASS
    NAME "Secteur indicatif de dangers -Phénomènes rocheux"
    EXPRESSION ([codegenre] = 6915 AND '[teneur]' eq 'Phénomènes rocheux')
    OUTLINECOLOR 255 255 189
  END
  CLASS
    NAME "Secteur indicatif de dangers -Lave torrentielle"
    EXPRESSION ([codegenre] = 6915 AND '[teneur]' eq 'Lave torrentielle')
    OUTLINECOLOR 189 255 190
  END
  CLASS
    NAME "Secteur indicatif de dangers -Inondation"
    EXPRESSION ([codegenre] = 6915 AND '[teneur]' eq 'Inondation')
    OUTLINECOLOR 189 190 255
  END
END

LAYER
  NAME "r73_zones_superposees"
  TYPE POLYGON
   METADATA
       "ows_title" "r73_zones_superposees"
       "wms_srs" "EPSG:2056"
       "wms_title"           "${instanceid} WMS Server"
       "wms_onlineresource" "http://${host}/${instanceid}/wmscrdppf"
       "wms_srs"            "EPSG:2056"
  END
  CONNECTIONTYPE POSTGIS
  CONNECTION "user=${dbuser} password=${dbpassword} dbname=${db} host=${dbhost} port=${dbport}"
  PROCESSING "CLOSE_CONNECTION=DEFER"
  DATA "geom from crdppf.r73_zones_superposees using unique idobj using srid=2056"
  STATUS ON
  CLASSITEM "codegenre"
  OPACITY 90
  TEMPLATE "ttt"
  CLASS
    NAME "Périmètre protection site bâti"
    EXPRESSION /5101/
    SYMBOL "pointilles2"
    SIZE 4
    OUTLINECOLOR 255 0 0
  END
  CLASS
    NAME "Zone de crêtes et forêts"
    EXPRESSION /5201/
    COLOR 255 255 0
    OUTLINECOLOR 0 0 0
  END
  CLASS
    NAME "Zone de vignes et grèves"
    EXPRESSION /5202/
    COLOR 0 255 0
    OUTLINECOLOR 0 0 0
  END
  CLASS
    NAME "Réserve naturelle"
    EXPRESSION /5203/
     STYLE
        OUTLINECOLOR 80 90 10
     END
     STYLE
        SYMBOL "hachure3"
        SIZE 3
        COLOR 135 145 45
     END
  END
  CLASS
    NAME "Biotope cantonal"
    EXPRESSION /5204/
    COLOR 135 145 45
    OUTLINECOLOR 80 90 10
  END
  CLASS
    NAME "Périmètres site marécageux"
    EXPRESSION /5205/
    STYLE
      OUTLINECOLOR 132 132 0
      WIDTH 3
    END
  END
  CLASS
    NAME "Périmètres paysages protégés"
    EXPRESSION /5206/
    STYLE
      WIDTH 3
      OUTLINECOLOR 40 100 40
    END
  END
  CLASS
    NAME "Danger élevé"
    EXPRESSION /5304/
    COLOR 255 0 0
  END
  CLASS
    NAME "Danger moyen"
    EXPRESSION /5303/
    COLOR 0 0 255
  END
  CLASS
    NAME "Danger faible"
    EXPRESSION /5302/
    COLOR 255 255 0
  END
  CLASS
    NAME "Danger résiduel"
    EXPRESSION /5301/
    STYLE
      COLOR 255 255 0
    END
    STYLE
      SYMBOL "hachure7"
    END
  END
  CLASS
    NAME "Protection rives"
    EXPRESSION /5901/
    COLOR 135 145 45
    OUTLINECOLOR 80 90 10
  END
  CLASS
    NAME "Zones réservées"
    EXPRESSION /5903/
    STYLE
      OUTLINECOLOR 0 0 0
      WIDTH 1
    END
    STYLE
      SYMBOL "hachure6"
      COLOR 0 0 0
      SIZE 5
    END
  END
END

LAYER
  NAME "r73_affectations_primaires"
  TYPE POLYGON
   METADATA
       "ows_title" "r73_affectations_primaires"
       "wms_srs" "EPSG:2056"
       "wms_title"           "${instanceid} WMS Server"
       "wms_onlineresource" "http://${host}/${instanceid}/wmscrdppf"
       "wms_srs"            "EPSG:2056"
  END
  CONNECTIONTYPE POSTGIS
  CONNECTION "user=${dbuser} password=${dbpassword} dbname=${db} host=${dbhost} port=${dbport}"
  PROCESSING "CLOSE_CONNECTION=DEFER"
  DATA "geom from crdppf.r73_affectations_primaires using unique idobj using srid=2056"
  STATUS ON
  CLASSITEM "codegenre"
  OPACITY 50
  TEMPLATE "ttt"
  CLASS
    NAME "Faible densité"
    EXPRESSION /1101/
    COLOR 255 236 176
  END
  CLASS
    NAME "Résidentielle densifiée"
    EXPRESSION /1102/
    COLOR 255 216 96
  END
  CLASS
    NAME "Moyenne densité"
    EXPRESSION /1103/
    COLOR 240 180 0
  END
  CLASS
    NAME "Forte densité"
    EXPRESSION /1104/
    COLOR 255 0 0
  END
  CLASS
    NAME "Chalets"
    EXPRESSION /1105/
    COLOR 255 255 144
  END
  CLASS
    NAME "Constructions basses"
    EXPRESSION /1106/
    COLOR 255 0 0
    OUTLINECOLOR 0 0 0
  END
  CLASS
    NAME "Plan spécial a"
    EXPRESSION /1107/
    STYLE
      SYMBOL 'circle'
      COLOR 255 0 0
      SIZE 3
    END
  END
  CLASS
    NAME "Zone spéciale a"
    EXPRESSION /1108/
    COLOR 128 128 128
  END
  CLASS
    NAME "Activités économiques"
    EXPRESSION /1201/
    COLOR 128 0 128
  END
  CLASS
    NAME "Artisanale"
    EXPRESSION /1202/
    COLOR 255 128 255
  END
  CLASS
    NAME "Commerciale"
    EXPRESSION /1203/
    COLOR 255 0 255
  END
  CLASS
    NAME "Activités économiques"
    EXPRESSION /1204/
    COLOR 128 0 128
  END
  CLASS
    NAME "Industrielle"
    EXPRESSION /1205/
    COLOR 0 0 128
  END
  CLASS
    NAME "Mixte"
    EXPRESSION /1301/
    STYLE
      COLOR 255 0 255
      SYMBOL 'circle'
      SIZE 3
    END
  END
  CLASS
    NAME "Ancienne localité"
    EXPRESSION /1401/
    COLOR 112 0 0
  END
  CLASS
    NAME "Ville en damier"
    EXPRESSION /1402/
    COLOR 112 0 0
  END
  CLASS
    NAME "Centre ville"
    EXPRESSION /1403/
    COLOR 224 56 0
  END
  CLASS
    NAME "Utilité publique"
    EXPRESSION /1501/
    COLOR 176 176 176
  END
  CLASS
    NAME "Sports,détente et loisir"
    EXPRESSION /1502/
    COLOR 0 255 255
  END
  CLASS
    NAME "Prot. ancienne localité"
    EXPRESSION /1601/
    COLOR 255 152 48
  END
  CLASS
    NAME "Protection patrimoine"
    EXPRESSION /1602/
    COLOR 192 144 0
  END
  CLASS
    NAME "Fermes"
    EXPRESSION /1603/
    COLOR 176 176 0
  END
  CLASS
    NAME "Verdure"
    EXPRESSION /1604/
    COLOR 0 255 0
  END
  CLASS
    NAME "Tourisme"
    EXPRESSION /1701/
    COLOR 128 171 255
  END
  CLASS
    NAME "Aérodrome"
    EXPRESSION /1801/
    COLOR 192 192 255
  END
  CLASS
    NAME "Agricole"
    EXPRESSION /2101/
  END
  CLASS
    NAME "Zones viticoles"
    EXPRESSION /2301/
    STYLE
      COLOR 135 0 135
      OUTLINECOLOR 128 0 128
      SYMBOL 9
      SIZE 3
    END
  END
  CLASS
    NAME "Zone de protection 1"
    EXPRESSION /3101/
    COLOR 0 128 0
  END
  CLASS
    NAME "Haut-marais"
    EXPRESSION /3102/
    COLOR 135 145 45
    OUTLINECOLOR 135 145 45
  END
  CLASS
    NAME "Bas-marais"
    EXPRESSION /3103/
    COLOR 135 145 45
    OUTLINECOLOR 135 145 45
  END
  CLASS
    NAME "Bas-marais / Zone alluviale"
    EXPRESSION /3104/
    COLOR 135 145 45
    OUTLINECOLOR 135 145 45
  END
  CLASS
    NAME "Terrain agricole inclu dans biotope marécageux"
    EXPRESSION /3105/
    COLOR 132 132 0
    OUTLINECOLOR 132 132 0
    SYMBOL 'triangle'
    SIZE 4
  END
  CLASS
    NAME "Zone-tampon"
    EXPRESSION /3106/
    COLOR  160 153 78
    OUTLINECOLOR 160 153 78
    STYLE
        SYMBOL hachure
        COLOR 135 145 45
        ANGLE 0
        SIZE 5
    END
    STYLE
        SYMBOL hachure
        COLOR 135 145 45
        ANGLE 90
        SIZE 5
    END
  END
  CLASS
    NAME "Zone de protection"
    EXPRESSION /3107/
    COLOR 0 128 0
  END
  CLASS
    NAME "Hameau"
    EXPRESSION /4101/
    COLOR 112 112 0
  END
  CLASS
    NAME "Utilisation différée"
    EXPRESSION /4301/
    STYLE
      SYMBOL 'circle'
      COLOR 0 0 0
      SIZE 3
    END
  END
  CLASS
    NAME "Sports,détente et loisir"
    EXPRESSION /4901/
    COLOR 0 255 255
  END
  CLASS
    NAME "Militaire"
    EXPRESSION /4902/
    COLOR 0 128 128
  END
  CLASS
    NAME "Traitement déchets"
    EXPRESSION /4903/
    COLOR 208 156 0
  END
  CLASS
    NAME "Décharge"
    EXPRESSION /4904/
    COLOR 144 108 0
  END
  CLASS
    NAME "Extraction"
    EXPRESSION /4905/
    COLOR 96 72 0
  END
  CLASS
    NAME "Plan spécial b"
    EXPRESSION /4906/
    STYLE
      SYMBOL 'circle'
      COLOR 255 0 0
      SIZE 3
    END
  END
  CLASS
    NAME "Zone spéciale b"
    EXPRESSION /4907/
    COLOR 128 128 128
  END
END

LAYER
  NAME "r87_astra_projektierungszonen_nationalstrassen"
  STATUS ON
  METADATA
       "ows_title"                      "r87_astra_projektierungszonen_nationalstrassen"
       "wms_srs"                    "EPSG:2056"
       "wms_title"                      "${instanceid} WMS Server"
       "wms_onlineresource"     "http://${host}/${instanceid}/wmscrdppf"
       "wms_srs"                    "EPSG:2056"
  END
  CONNECTIONTYPE POSTGIS
  CONNECTION "user=${dbuser} password=${dbpassword} dbname=${db} host=${dbhost} port=${dbport}"
  PROCESSING "CLOSE_CONNECTION=DEFER"
  DATA "geom from crdppf.r87_astra_projektierungszonen_nationalstrassen using unique idobj using srid=2056"
  TYPE POLYGON
  TEMPLATE "ttt"
  OPACITY 60
  CLASS
    NAME "Zones réservées des routes nationales"
    COLOR 0 220 220
    OUTLINECOLOR 0 180 180
   END
END

LAYER
  NAME "r96_bav_projektierungszonen_eisenbahnanlagen"
  STATUS ON
  METADATA
       "ows_title"                      "r96_bav_projektierungszonen_eisenbahnanlagen"
       "wms_srs"                    "EPSG:2056"
       "wms_title"                      "${instanceid} WMS Server"
       "wms_onlineresource"     "http://${host}/${instanceid}/wmscrdppf"
       "wms_srs"                    "EPSG:2056"
  END
  CONNECTIONTYPE POSTGIS
  CONNECTION "user=${dbuser} password=${dbpassword} dbname=${db} host=${dbhost} port=${dbport}"
  PROCESSING "CLOSE_CONNECTION=DEFER"
  DATA "geom from crdppf.r96_bav_projektierungszonen_eisenbahnanlagen using unique idobj using srid=2056"
  TYPE POLYGON
  TEMPLATE "ttt"
  OPACITY 60
  CLASS
    NAME "Zones réservées des inst. ferroviaires"
    COLOR 220 220 0
    OUTLINECOLOR 180 180 0
   END
END

LAYER
  NAME "r97_bav_baulinien_eisenbahnanlagen"
  STATUS ON
  METADATA
       "ows_title"                      "r97_bav_baulinien_eisenbahnanlagen"
       "wms_srs"                    "EPSG:2056"
       "wms_title"                      "${instanceid} WMS Server"
       "wms_onlineresource"     "http://${host}/${instanceid}/wmscrdppf"
       "wms_srs"                    "EPSG:2056"
  END
  CONNECTIONTYPE POSTGIS
  CONNECTION "user=${dbuser} password=${dbpassword} dbname=${db} host=${dbhost} port=${dbport}"
  PROCESSING "CLOSE_CONNECTION=DEFER"
  DATA "geom from crdppf.r97_bav_baulinien_eisenbahnanlagen using unique idobj using srid=2056"
  TYPE LINE
  TEMPLATE "ttt"
  OPACITY 60
  CLASS
    NAME "Alignements des inst. ferroviaires"
    COLOR 220 220 0
   END
END

LAYER
  NAME "r103_bazl_projektierungszonen_flughafenanlagen"
  STATUS ON
  METADATA
       "ows_title"                      "r103_bazl_projektierungszonen_flughafenanlagen"
       "wms_srs"                    "EPSG:2056"
       "wms_title"                      "${instanceid} WMS Server"
       "wms_onlineresource"     "http://${host}/${instanceid}/wmscrdppf"
       "wms_srs"                    "EPSG:2056"
  END
  CONNECTIONTYPE POSTGIS
  CONNECTION "user=${dbuser} password=${dbpassword} dbname=${db} host=${dbhost} port=${dbport}"
  PROCESSING "CLOSE_CONNECTION=DEFER"
  DATA "geom from crdppf.r103_bazl_projektierungszonen_flughafenanlagen using unique idobj using srid=2056"
  TYPE POLYGON
  TEMPLATE "ttt"
  CLASS
    NAME "Zones réservées des inst. aéroportuaires"
    STYLE
      COLOR 255 170 0
      OPACITY 70
    END
    STYLE
      OUTLINECOLOR 255 170 0
    END
   END
END

LAYER
  NAME "r104_bazl_baulinien_flughafenanlagen"
  STATUS ON
  METADATA
       "ows_title"                      "r104_bazl_baulinien_flughafenanlagen"
       "wms_srs"                    "EPSG:2056"
       "wms_title"                      "${instanceid} WMS Server"
       "wms_onlineresource"     "http://${host}/${instanceid}/wmscrdppf"
       "wms_srs"                    "EPSG:2056"
  END
  CONNECTIONTYPE POSTGIS
  CONNECTION "user=${dbuser} password=${dbpassword} dbname=${db} host=${dbhost} port=${dbport}"
  PROCESSING "CLOSE_CONNECTION=DEFER"
  DATA "geom from crdppf.r104_bazl_baulinien_flughafenanlagen using unique idobj using srid=2056"
  TYPE LINE
  TEMPLATE "ttt"
  OPACITY 60
  CLASS
    NAME "Alignements des install. aéroportuaires"
    COLOR 0 0 180
   END
END

LAYER
  NAME "r108_bazl_sicherheitszonenplan"
  STATUS ON
  METADATA
       "ows_title"                      "r108_bazl_sicherheitszonenplan"
       "wms_srs"                    "EPSG:2056"
       "wms_title"                      "${instanceid} WMS Server"
       "wms_onlineresource"     "http://${host}/${instanceid}/wmscrdppf"
       "wms_srs"                    "EPSG:2056"
  END
  CONNECTIONTYPE POSTGIS
  CONNECTION "user=${dbuser} password=${dbpassword} dbname=${db} host=${dbhost} port=${dbport}"
  PROCESSING "CLOSE_CONNECTION=DEFER"
  DATA "geom from crdppf.r108_bazl_sicherheitszonenplan using unique idobj using srid=2056"
  TYPE POLYGON
  TEMPLATE "ttt"
  CLASS
    NAME "Plan de la zone de sécurité"
    STYLE
      COLOR 192 0 192
      OPACITY 45
    END
    STYLE
      OUTLINECOLOR 192 0 192
    END
   END
END

LAYER
  STATUS ON
  NAME "r116_sites_pollues"
  METADATA
       "ows_title"                      "r116_sites_pollues"
       "wms_srs"                    "EPSG:2056"
       "wms_title"                      "${instanceid} WMS Server"
       "wms_onlineresource"     "http://${host}/${instanceid}/wmscrdppf"
       "wms_srs"                    "EPSG:2056"
  END
  CONNECTIONTYPE POSTGIS
  CONNECTION "user=${dbuser} password=${dbpassword} dbname=${db} host=${dbhost} port=${dbport}"
  PROCESSING "CLOSE_CONNECTION=DEFER"
  DATA "geom from crdppf.r116_sites_pollues using unique idobj using srid=2056"
  TYPE POLYGON
  TEMPLATE "ttt"
  OPACITY 60
  CLASSITEM "codegenre"
  CLASS
    NAME "Pollué, investigation nécessaire"
    EXPRESSION /9903/
    COLOR 0 0 255
    OUTLINECOLOR 0 0 0
  END
   CLASS
    NAME "Pollué, ne nécessite ni surveillance ni assainissement"
    EXPRESSION /9905/
    COLOR 255 204 0
    OUTLINECOLOR 0 0 0
   END
   CLASS
    NAME "Pollué, nécessite une surveillance"
    EXPRESSION /9906/
    COLOR 255 102 5
    OUTLINECOLOR 0 0 0
   END
   CLASS
    NAME "Pollué, nécessite un assainissement"
    EXPRESSION /9907/
    COLOR 255 0 0
    OUTLINECOLOR 0 0 0
   END
   CLASS
    NAME "Pollué, nécessitée d'une investigation non encore évaluée"
    EXPRESSION /9908/
    COLOR 95 95 95
    OUTLINECOLOR 0 0 0
   END
  CLASS
    NAME "Pollué, pas d'atteinte nuisible ou incommodante à attendre"
    EXPRESSION /9904/
    COLOR 255 255 0
    OUTLINECOLOR 0 0 0
   END
END

LAYER
  STATUS ON
  NAME "r118_bazl_belastete_standorte_zivilflugplaetze_pts"
  GROUP "r118_bazl_belastete_standorte_zivilflugplaetze"
  METADATA
       "ows_title"                   "r118_bazl_belastete_standorte_zivilflugplaetze_pts"
       "wms_srs"                    "EPSG:2056"
       "wms_title"                  "${instanceid} WMS Server"
       "wms_onlineresource"    "http://${host}/${instanceid}/wmscrdppf"
       "wms_srs"                   "EPSG:2056"
  END
  CONNECTIONTYPE POSTGIS
  CONNECTION "user=${dbuser} password=${dbpassword} dbname=${db} host=${dbhost} port=${dbport}"
  PROCESSING "CLOSE_CONNECTION=DEFER"
  DATA "geom from (
    select *
    from crdppf.r118_bazl_belastete_standorte_zivilflugplaetze
    WHERE  st_geometrytype(geom) like 'ST_Point'
    ) as foo using unique idobj using srid=2056"
  TYPE POINT
  TEMPLATE "ttt"
  OPACITY 60
  CLASSITEM "codegenre"
  CLASS
    NAME "Pollué, investigation nécessaire"
    SYMBOL "circle"
    EXPRESSION /9903/
    COLOR 0 0 255
    OUTLINECOLOR 0 0 0
    SIZE 7
  END
  CLASS
    NAME "Pollué, pas d'atteinte nuisible ou incommodante à attendre"
    SYMBOL "circle"
    EXPRESSION /9904/
    COLOR 255 255 0
    OUTLINECOLOR 0 0 0
    SIZE 7
   END
   CLASS
    NAME "Pollué, ne nécessite ni surveillance ni assainissement"
    SYMBOL "circle"
    EXPRESSION /9905/
    COLOR 255 204 0
    OUTLINECOLOR 0 0 0
    SIZE 7
   END
   CLASS
    NAME "Pollué, nécessite une surveillance"
    SYMBOL "circle"
    EXPRESSION /9906/
    COLOR 255 102 5
    OUTLINECOLOR 0 0 0
    SIZE 7
   END
   CLASS
    NAME "Pollué, nécessite un assainissement"
    SYMBOL "circle"
    EXPRESSION /9907/
    COLOR 255 0 0
    OUTLINECOLOR 0 0 0
    SIZE 7
   END
   CLASS
    NAME "Pollué, nécessitée d'une investigation non encore évaluée"
    SYMBOL "circle"
    EXPRESSION /9908/
    COLOR 95 95 95
    OUTLINECOLOR 0 0 0
    SIZE 7
   END
END

LAYER
  STATUS ON
  NAME "r118_bazl_belastete_standorte_zivilflugplaetze_poly"
  GROUP "r118_bazl_belastete_standorte_zivilflugplaetze"
  METADATA
       "ows_title"                   "r118_bazl_belastete_standorte_zivilflugplaetze_poly"
       "wms_srs"                    "EPSG:2056"
       "wms_title"                  "${instanceid} WMS Server"
       "wms_onlineresource"    "http://${host}/${instanceid}/wmscrdppf"
       "wms_srs"                   "EPSG:2056"
  END
  CONNECTIONTYPE POSTGIS
  CONNECTION "user=${dbuser} password=${dbpassword} dbname=${db} host=${dbhost} port=${dbport}"
  PROCESSING "CLOSE_CONNECTION=DEFER"
  DATA "geom from crdppf.r118_bazl_belastete_standorte_zivilflugplaetze using unique idobj using srid=2056"
  TYPE POLYGON
  TEMPLATE "ttt"
  OPACITY 60
  CLASSITEM "codegenre"
  CLASS
    NAME "Pollué, investigation nécessaire"
    EXPRESSION /9903/
    COLOR 0 0 255
    OUTLINECOLOR 0 0 0
  END
  CLASS
    NAME "Pollué, pas d'atteinte nuisible ou incommodante à attendre"
    EXPRESSION /9904/
    COLOR 255 255 0
    OUTLINECOLOR 0 0 0
   END
   CLASS
    NAME "Pollué, ne nécessite ni surveillance ni assainissement"
    EXPRESSION /9905/
    COLOR 255 204 0
    OUTLINECOLOR 0 0 0
   END
   CLASS
    NAME "Pollué, nécessite une surveillance"
    EXPRESSION /9906/
    COLOR 255 102 5
    OUTLINECOLOR 0 0 0
   END
   CLASS
    NAME "Pollué, nécessite un assainissement"
    EXPRESSION /9907/
    COLOR 255 0 0
    OUTLINECOLOR 0 0 0
   END
   CLASS
    NAME "Pollué, nécessitée d'une investigation non encore évaluée"
    EXPRESSION /9908/
    COLOR 95 95 95
    OUTLINECOLOR 0 0 0
   END
END

LAYER
  STATUS ON
  NAME "r119_bav_belastete_standorte_oev"
  METADATA
       "ows_title"                   "r119_bav_belastete_standorte_oev"
       "wms_srs"                    "EPSG:2056"
       "wms_title"                  "${instanceid} WMS Server"
       "wms_onlineresource"    "http://${host}/${instanceid}/wmscrdppf"
       "wms_srs"                   "EPSG:2056"
  END
  CONNECTIONTYPE POSTGIS
  CONNECTION "user=${dbuser} password=${dbpassword} dbname=${db} host=${dbhost} port=${dbport}"
  PROCESSING "CLOSE_CONNECTION=DEFER"
  DATA "geom from crdppf.r119_bav_belastete_standorte_oev using unique idobj using srid=2056"
  TYPE POLYGON
  TEMPLATE "ttt"
  OPACITY 60
  CLASSITEM "codegenre"
  CLASS
    NAME "Pollué, investigation nécessaire"
    EXPRESSION /9903/
    COLOR 0 0 255
    OUTLINECOLOR 0 0 0
  END
   CLASS
    NAME "Pollué, ne nécessite ni surveillance ni assainissement"
    EXPRESSION /9905/
    COLOR 255 204 0
    OUTLINECOLOR 0 0 0
   END
   CLASS
    NAME "Pollué, nécessite une surveillance"
    EXPRESSION /9906/
    COLOR 255 102 5
    OUTLINECOLOR 0 0 0
   END
   CLASS
    NAME "Pollué, nécessite un assainissement"
    EXPRESSION /9907/
    COLOR 255 0 0
    OUTLINECOLOR 0 0 0
   END
   CLASS
    NAME "Pollué, nécessitée d'une investigation non encore évaluée"
    EXPRESSION /9908/
    COLOR 95 95 95
    OUTLINECOLOR 0 0 0
   END
  CLASS
    NAME "Pollué, pas d'atteinte nuisible ou incommodante à attendre"
    EXPRESSION /9904/
    COLOR 255 255 0
    OUTLINECOLOR 0 0 0
   END
END

LAYER
  NAME "r131_zone_prot_eau"
  STATUS ON
  METADATA
       "ows_title"                   "r131_zone_prot_eau"
       "wms_srs"                    "EPSG:2056"
       "wms_title"                  "${instanceid} WMS Server"
       "wms_onlineresource"    "http://${host}/${instanceid}/wmscrdppf"
       "wms_srs"                   "EPSG:2056"
  END
  CONNECTIONTYPE POSTGIS
  CONNECTION "user=${dbuser} password=${dbpassword} dbname=${db} host=${dbhost} port=${dbport}"
  PROCESSING "CLOSE_CONNECTION=DEFER"
  DATA "geom from crdppf.r131_zone_prot_eau using unique idobj using srid=2056"
  TYPE POLYGON
  TEMPLATE "ttt"
  OPACITY 60
  CLASSITEM "teneur"
  CLASS
    NAME "Zone S1"
    EXPRESSION /S1/
    COLOR 0 59 179
    OUTLINECOLOR 0 0 128
  END
  CLASS
    NAME "S2 à efficacité limitée"
    EXPRESSION /S2EL/
    COLOR 64 124 184
    OUTLINECOLOR 0 0 0
  END
  CLASS
    NAME "Zone S2"
    EXPRESSION /S2/
    COLOR 51 136 255
    OUTLINECOLOR 0 0 128
  END
  CLASS
    NAME "Zone S3"
    EXPRESSION /S3/
    COLOR 179 210 255
    OUTLINECOLOR 0 0 128
  END
  CLASS
    NAME "S3Zu"
    EXPRESSION /S3ZU/
    STYLE
      COLOR 179 210 255
      OUTLINECOLOR 0 0 128
    END
    STYLE
      SYMBOL "hachure1"
      ANGLE 90
      COLOR 0 0 128
      SIZE 5
    END
  END
END

LAYER
  NAME "r132_perimetre_prot_eau"
  STATUS ON
  METADATA
       "ows_title"                   "r132_perimetre_prot_eau"
       "wms_srs"                    "EPSG:2056"
       "wms_title"                  "${instanceid} WMS Server"
       "wms_onlineresource"    "http://${host}/${instanceid}/wmscrdppf"
       "wms_srs"                   "EPSG:2056"
  END
  CONNECTIONTYPE POSTGIS
  CONNECTION "user=${dbuser} password=${dbpassword} dbname=${db} host=${dbhost} port=${dbport}"
  PROCESSING "CLOSE_CONNECTION=DEFER"
  DATA "geom from crdppf.r132_perimetre_prot_eau using unique idobj using srid=2056"
  TYPE POLYGON
  TEMPLATE "ttt"
  CLASSITEM "teneur"
  CLASS
    NAME "secteur Ao et Au"
    EXPRESSION /secteur Ao et Au/
    STYLE
      COLOR 255 0 0
      OUTLINECOLOR 255 0 0
      OPACITY 40
    END
  END
  CLASS
    NAME "secteur Au"
    EXPRESSION /secteur Au/
    STYLE
      COLOR 255 0 0
      OUTLINECOLOR 255 0 0
      OPACITY 40
    END
  END
  CLASS
    NAME "secteur Ao"
    EXPRESSION /secteur Ao/
    STYLE
      COLOR 255 218 191
      OUTLINECOLOR 255 218 191
      OPACITY 60
    END
  END
  CLASS
    NAME "Aire Zu"
    EXPRESSION /A. ZU/
    STYLE
      COLOR 0 0 0
      OUTLINECOLOR 170 102 204
    END
    STYLE
      SYMBOL "hachure1"
      ANGLE 90
      COLOR 170 102 204
      SIZE 5
    END
  END
END

LAYER
 NAME "r145_sens_bruit"
  TYPE POLYGON
   METADATA
       "ows_title" "r145_sens_bruit"
       "wms_srs" "EPSG:2056"
       "wms_title"           "${instanceid} WMS Server"
       "wms_onlineresource" "http://${host}/${instanceid}/wmscrdppf"
       "wms_srs"            "EPSG:2056"
  END
  CONNECTIONTYPE POSTGIS
  CONNECTION "user=${dbuser} password=${dbpassword} dbname=${db} host=${dbhost} port=${dbport}"
  PROCESSING "CLOSE_CONNECTION=DEFER"
  DATA "geom from crdppf.r145_sens_bruit using unique idobj using srid=2056"
  STATUS ON
  CLASSITEM "teneur"
  OPACITY 50
  TEMPLATE "ttt"
  CLASS
    NAME "IV"
    EXPRESSION /DS IV/
    COLOR 230 0 0
    # OUTLINECOLOR 0 0 0
  END
  CLASS
    NAME "III"
    EXPRESSION /DS III/
    COLOR 255 77 0
    # OUTLINECOLOR 0 0 0
  END
  CLASS
    NAME "II"
    EXPRESSION /DS II/
    COLOR 255 166 0
    # OUTLINECOLOR 0 0 0
  END
  CLASS
    NAME "I"
    EXPRESSION /DS I/
    COLOR 255 242 0
    # OUTLINECOLOR 0 0 0
  END
END

LAYER
  NAME "r157_lim_foret"
  TYPE LINE
  METADATA
       "ows_title" "r157_lim_foret"
       "wms_srs"                    "EPSG:2056"
       "wms_title"                      "${instanceid} WMS Server"
       "wms_onlineresource"     "http://${host}/${instanceid}/wmscrdppf"
       "wms_srs"                    "EPSG:2056"
  END
  CONNECTIONTYPE POSTGIS
  CONNECTION "user=${dbuser} password=${dbpassword} dbname=${db} host=${dbhost} port=${dbport}"
  PROCESSING "CLOSE_CONNECTION=DEFER"
  DATA "geom from crdppf.r157_lim_foret using unique idobj using srid=2056"
  STATUS ON
  TEMPLATE "ttt"
  CLASSITEM "codegenre"
  CLASS
    NAME "Limite forestière statique"
    EXPRESSION /1/
    STYLE
      WIDTH 2
      COLOR 230 0 0
    END
  END
  TOLERANCE 5
  TOLERANCEUNITS pixels
END

LAYER
  NAME "r159_dist_foret"
  TYPE LINE
  METADATA
       "ows_title" "r159_dist_foret"
       "wms_srs"                    "EPSG:2056"
       "wms_title"                      "${instanceid} WMS Server"
       "wms_onlineresource"     "http://${host}/${instanceid}/wmscrdppf"
       "wms_srs"                    "EPSG:2056"
  END
  CONNECTIONTYPE POSTGIS
  CONNECTION "user=${dbuser} password=${dbpassword} dbname=${db} host=${dbhost} port=${dbport}"
  PROCESSING "CLOSE_CONNECTION=DEFER"
  DATA "geom from crdppf.r159_dist_foret using unique idobj using srid=2056"
  STATUS ON
  TEMPLATE "ttt"
  TOLERANCE 5
  TOLERANCEUNITS pixels
  CLASSITEM "codegenre"
  CLASS
    NAME "Distance par rapport à la forêt"
    EXPRESSION /7105/
    STYLE
        PATTERN 8 4 1 4 END
        WIDTH 2
        COLOR 0 255 0
    END
  END
END

#####################
# RESTRICTIONS CRDPPF - fin
#####################


#####################
# Aménagement
#####################

LAYER
  NAME "la3_limites_communales"
  TYPE POLYGON
  CONNECTIONTYPE POSTGIS
  CONNECTION "user=${dbuser} password=${dbpassword} dbname=${db} host=${dbhost} port=${dbport}"
  PROCESSING "CLOSE_CONNECTION=DEFER"
  DATA "geom from general.la3_limites_communales using unique numcom using srid=2056"
  STATUS ON
  CLASS
    NAME "Limites communales"
    STYLE
      OUTLINECOLOR 90 90 90
    END
  END
  METADATA
    "ows_title" "la3_limites_communales"
    "wms_srs" "EPSG:2056"
  END
  PROJECTION
    "init=epsg:2056"   ##required
  END
END

LAYER
  NAME "at23_perimetres_archeologiques"
  TYPE POLYGON
  METADATA
       "ows_title" "at23_perimetres_archeologiques"
       " wms_srs" "EPSG:2056"
  END
  CONNECTIONTYPE POSTGIS
  CONNECTION "user=${dbuser} password=${dbpassword} dbname=${db} host=${dbhost} port=${dbport}"
  PROCESSING "CLOSE_CONNECTION=DEFER"
  DATA "geom from amenagement.at23_perimetres_archeologiques using unique idobj using srid=2056"
  STATUS ON
  TEMPLATE "ttt"
  CLASS
    NAME "Périmètres archéologiques"
    SYMBOL "pointilles2"
    SIZE 4
    OUTLINECOLOR 0 0 0
  END
  MAXSCALEDENOM 200000
END

LAYER
  NAME "at24_perimetres_tir"
  TYPE POLYGON
  METADATA
       "ows_title" "at24_perimetres_tir"
       " wms_srs" "EPSG:2056"
  END
  CONNECTIONTYPE POSTGIS
  CONNECTION "user=${dbuser} password=${dbpassword} dbname=${db} host=${dbhost} port=${dbport}"
  PROCESSING "CLOSE_CONNECTION=DEFER"
  DATA "geom from amenagement.at24_perimetres_tir using unique idobj using srid=2056"
  STATUS ON
  TEMPLATE "ttt"
  CLASS
    NAME "Périmètres de tir"
    STYLE
        OUTLINECOLOR 0 0 0
        PATTERN 7 4 7 4 3 4 3 4 3 4 END
        WIDTH 3
    END
  END
END

LAYER
 NAME "clo_couloirs"
  TYPE POLYGON
  METADATA
       "ows_title" "clo_couloirs"
       " wms_srs" "EPSG:2056"
  END
  CONNECTIONTYPE POSTGIS
  CONNECTION "user=${dbuser} password=${dbpassword} dbname=${db} host=${dbhost} port=${dbport}"
  PROCESSING "CLOSE_CONNECTION=DEFER"
  DATA "geom from amenagement.clo_couloirs using unique idobj using srid=2056"
  STATUS ON
  TEMPLATE "ttt"
  CLASS
    NAME "Couloirs lim. obstacles"
    STYLE
        OUTLINECOLOR 255 0 0
        SYMBOL points3
        SIZE 5
    END
  END
  MINSCALEDENOM 0
  MAXSCALEDENOM 101000
END

LAYER
 NAME "clo_cotes_altitude_surfaces"
  TYPE POLYGON
  METADATA
       "ows_title" "clo_cotes_altitude_surfaces"
       " wms_srs" "EPSG:2056"
  END
  CONNECTIONTYPE POSTGIS
  CONNECTION "user=${dbuser} password=${dbpassword} dbname=${db} host=${dbhost} port=${dbport}"
  PROCESSING "CLOSE_CONNECTION=DEFER"
  DATA "geom from amenagement.clo_cotes_altitude_surfaces using unique idobj using srid=2056"
  STATUS ON
  TEMPLATE "ttt"
  LABELITEM "cote_alt_obstacles_maximum"
  CLASS
    NAME "Cote altitude surfaces"
    STYLE
        OUTLINECOLOR 255 0 0
        WIDTH 1.0
        PATTERN 3 3 END
    END
    LABEL
      TYPE TRUETYPE
      FONT verdana
      SIZE 8
      ANTIALIAS TRUE
      COLOR 255 0 0
      OUTLINECOLOR 255 255 255
      MINFEATURESIZE 50
    END
  END
  MINSCALEDENOM 0
  MAXSCALEDENOM 101000
END

#####################
# Environnement
#####################

LAYER
 NAME "ex01_cours_eau"
  TYPE LINE
  METADATA
       "ows_title" "ex01_cours_eau"
       " wms_srs" "EPSG:2056"
  END
  CONNECTIONTYPE POSTGIS
  CONNECTION "user=${dbuser} password=${dbpassword} dbname=${db} host=${dbhost} port=${dbport}"
  PROCESSING "CLOSE_CONNECTION=DEFER"
  DATA "geom from environnement.ex01_cours_eau using unique idobj using srid=2056"
  STATUS ON
  TEMPLATE "ttt"
  CLASS
    NAME "Cours eau"
    STYLE
      WIDTH 2
      COLOR 0 0 255
    END
  END
  MINSCALEDENOM 500
END

#####################
# Mensuration
#####################

LAYER
    NAME "cantons_situation"
    METADATA
        "wms_title" "Cantons suisse situation"
        "wms_srs" "EPSG:2056"
    END
    TYPE POLYGON
    STATUS ON
    CONNECTIONTYPE POSTGIS
    CONNECTION "user=${dbuser} password=${dbpassword} dbname=${db} host=${dbhost} port=${dbport}"
    PROCESSING "CLOSE_CONNECTION=DEFER"
    DATA "geom from situation.cantons using unique idobj using srid=2056"  
    MINSCALEDENOM 60001
    MAXSCALEDENOM 1000000000
    CLASSITEM "libgeo"
    CLASS
        EXPRESSION /Lucerne/
        STYLE
            COLOR 255 255 255
        END
    END
    CLASS
        EXPRESSION /Berne/ 
        STYLE
            COLOR 160 160 160
        END
    END
    CLASS
        EXPRESSION /Fribourg/
        STYLE
            COLOR 240 240 240
        END
    END
    CLASS
        EXPRESSION /Vaud/ 
        STYLE
            COLOR 192 192 192
        END
    END
    CLASS
        EXPRESSION ('[libgeo]' eq 'Jura (CH)')
        STYLE
            COLOR 190 190 190
        END
    END
    CLASS
        EXPRESSION /Neuchâtel/ 
    END
    CLASS
        EXPRESSION /Valais/ 
        STYLE
            COLOR 120 120 120
        END
    END
    CLASS
        EXPRESSION /Genève/ 
        STYLE
            COLOR 220 220 220
        END  
    CLASS
        EXPRESSION /Zürich/
        STYLE
            COLOR 130 130 130
        END  
    END  
    CLASS
        EXPRESSION /Uri/
        STYLE
            COLOR 220 220 220
        END  
    END  
    CLASS
        EXPRESSION /Schwyz/
        STYLE
            COLOR 100 100 100
        END  
    END  
    CLASS
        EXPRESSION /Obwald/ 
        STYLE
            COLOR 200 200 200
        END  
    END  
    CLASS
        EXPRESSION /Glaris/ 
        STYLE
            COLOR 190 190 190
        END  
    END  
    CLASS
        EXPRESSION /Niedwald/
        STYLE
            COLOR 150 150 150
        END  
    END  
    CLASS
        EXPRESSION /Zoug/
        STYLE
            COLOR 200 200 200
        END  
    END  
    CLASS
        EXPRESSION /Soleure/
        STYLE
            COLOR 130 130 130
        END   
    END   
    CLASS
        EXPRESSION /St-Gall/
        STYLE
            COLOR 190 190 190
        END  
    END  
    CLASS
        EXPRESSION /Argovie/
        STYLE
            COLOR 180 180 180
        END  
    END  
    CLASS
        EXPRESSION /Schaffouse/
        STYLE
            COLOR 160 160 160
        END  
    END  
    CLASS
        EXPRESSION /Bâle Ville/
        STYLE
            COLOR 220 220 220
        END  
    END  
    CLASS
        EXPRESSION /Bâle Campagne/
        STYLE
            COLOR 230 230 230
        END  
    END  
    CLASS
        EXPRESSION /Thurgovie/
        STYLE
            COLOR 230 230 230
        END  
    END  
    CLASS
        EXPRESSION /Tessin/
        STYLE
            COLOR 180 180 180
        END  
    END  
    CLASS
        EXPRESSION /Grisons/
        STYLE
            COLOR 120 120 120
        END  
    END  
    CLASS
        EXPRESSION /Appenzell Ausserrhoden/
        STYLE
            COLOR 220 220 220
        END  
    END  
    CLASS
        EXPRESSION /Appenzell Innerrhoden/
        STYLE
            COLOR 140 140 140
        END  
    END  
    CLASS
        EXPRESSION /Doubs/
        STYLE
            COLOR 255 255 255
            OUTLINECOLOR 200 200 200
        END  
    END  
    CLASS
        EXPRESSION /./
        STYLE
            OUTLINECOLOR 200 200 200
        END  
    END
END

LAYER
    NAME "frontiere_pays_situation"
    METADATA
        "wms_title" "Frontière des pays limitrophe de la Suisse"
        "wms_srs" "EPSG:2056"
    END
    TYPE POLYGON
    STATUS ON
    CONNECTIONTYPE POSTGIS
    CONNECTION "user=${dbuser} password=${dbpassword} dbname=${db} host=${dbhost} port=${dbport}"
    PROCESSING "CLOSE_CONNECTION=DEFER"
    DATA "geom from situation.frontiere_pays using unique idobj using srid=2056"  
    MINSCALEDENOM 60001
    MAXSCALEDENOM 1000000000
    CLASS
        STYLE
            WIDTH 2
            OUTLINECOLOR 192 192 192
        END
    END
END

LAYER
    NAME "couvsol_situation"
    METADATA
        "wms_title" "Couverture du sol vector25"
        "wms_srs" "EPSG:2056"
    END
    TYPE polygon
    CONNECTIONTYPE POSTGIS
    CONNECTION "user=${dbuser} password=${dbpassword} dbname=${db} host=${dbhost} port=${dbport}"
    PROCESSING "CLOSE_CONNECTION=DEFER"
    DATA "geom from situation.couvsol_situation using unique idobj using srid=2056"  
    OPACITY 30
    CLASSITEM "objectval"
    CLASS
        EXPRESSION /(Z_Wald)|(Z_WaldOf)/
        STYLE
            COLOR 150 150 150
        END
        MINSCALEDENOM 60001
        MAXSCALEDENOM 2000000
    END
    CLASS
        EXPRESSION /Z_Siedl/
        STYLE
            COLOR 0 0 0
        END
        MINSCALEDENOM 60001
        MAXSCALEDENOM 2000000
    END
END 

LAYER
    NAME "lacs_situation"
    METADATA
        "wms_title" "Lacs suisse"
        "wms_srs" "EPSG:2056"
    END
    TYPE POLYGON
    STATUS ON
    CONNECTIONTYPE POSTGIS
    CONNECTION "user=${dbuser} password=${dbpassword} dbname=${db} host=${dbhost} port=${dbport}"
    PROCESSING "CLOSE_CONNECTION=DEFER"
    DATA "geom from situation.lacs using unique idobj using srid=2056"  
    MINSCALEDENOM 60001
    MAXSCALEDENOM 1000000000
    CLASS
        STYLE
            COLOR 144 144 144
            OUTLINECOLOR 104 104 104
        END
    END
END

LAYER
    NAME "hydro_suisse"
    METADATA
        "wms_title" "Réso hydro suisse"
        "wms_srs" "EPSG:2056"
    END
    TYPE LINE
    STATUS ON
    CONNECTIONTYPE POSTGIS
    CONNECTION "user=${dbuser} password=${dbpassword} dbname=${db} host=${dbhost} port=${dbport}"
    PROCESSING "CLOSE_CONNECTION=DEFER"
    DATA "geom from situation.hydro_suisse using unique idobj using srid=2056"  
    MINSCALEDENOM 60001
    MAXSCALEDENOM 1100000
    CLASS
        STYLE
            COLOR 144 144 144
        END
    END
END

LAYER
    NAME "communes_situation"
    METADATA
        "wms_title" "Communes neuchâteloises 2013"
        "wms_srs" "EPSG:2056"
    END
    TYPE POLYGON
    STATUS ON
    CONNECTIONTYPE POSTGIS
    CONNECTION "user=${dbuser} password=${dbpassword} dbname=${db} host=${dbhost} port=${dbport}"
    PROCESSING "CLOSE_CONNECTION=DEFER"
    DATA "geom from situation.communes using unique idobj using srid=2056"
    MINSCALEDENOM 60001
    MAXSCALEDENOM 200000
    CLASS
        STYLE
            OUTLINECOLOR 100 100 100
        END
    END
END

LAYER
    NAME "districts_situation"
    METADATA
        "wms_title" "Districts situation"
        "wms_srs" "EPSG:2056"
    END
    TYPE POLYGON
    STATUS ON
    CONNECTIONTYPE POSTGIS
    CONNECTION "user=${dbuser} password=${dbpassword} dbname=${db} host=${dbhost} port=${dbport}"
    PROCESSING "CLOSE_CONNECTION=DEFER"
    DATA "geom from situation.districts using unique idobj using srid=2056"  
    MINSCALEDENOM 60001
    MAXSCALEDENOM 200000
    CLASS
        STYLE
            WIDTH 2
            OUTLINECOLOR 100 100 100
        END
    END
END

LAYER
    NAME "frontiere_suisse"
    METADATA
        "wms_title" "Frontière suisse"
        "wms_srs" "EPSG:2056"
    END
    TYPE POLYGON
    STATUS ON
    CONNECTIONTYPE POSTGIS
    CONNECTION "user=${dbuser} password=${dbpassword} dbname=${db} host=${dbhost} port=${dbport}"
    PROCESSING "CLOSE_CONNECTION=DEFER"
    DATA "geom from situation.frontiere_suisse using unique idobj using srid=2056"  
    MINSCALEDENOM 60001
    MAXSCALEDENOM 1000000000
    OPACITY 80
    CLASS
        STYLE  
            WIDTH 2
            OUTLINECOLOR 40 40 40
        END
    END
END

LAYER
    NAME "rail1"
    METADATA
        "wms_title" "Rails niveau 1"
        "wms_srs" "EPSG:2056"
    END
    STATUS ON 
    OPACITY 40
    CONNECTIONTYPE postgis 
    CONNECTION "user=${dbuser} password=${dbpassword} dbname=${db} host=${dbhost} port=${dbport}"
    PROCESSING "CLOSE_CONNECTION=DEFER" 
    MAXSCALEDENOM 210000 
    MINSCALEDENOM  50010
    TYPE LINE
    DATA "geom from (select geom, osm_id ,railway, name from situation.osm_line_ch where railway='rail') as foo using unique osm_id using srid=2056"
    CLASS
        STYLE
            WIDTH 1
            OUTLINEWIDTH 1
            OUTLINECOLOR "#555554"
        END
        STYLE
            SYMBOL "railfar"
            PATTERN 5 5 END
            WIDTH 1
            COLOR "#ffffff"
        END
    END
END

LAYER
    NAME "rail2" 
    METADATA
        "wms_title" "Rails 2"
        "wms_srs" "EPSG:2056"
    END
    STATUS ON 
    CONNECTIONTYPE postgis 
    CONNECTION "user=${dbuser} password=${dbpassword} dbname=${db} host=${dbhost} port=${dbport}"
    PROCESSING "CLOSE_CONNECTION=DEFER" 
    MAXSCALEDENOM 50010 
    MINSCALEDENOM 35000
    TYPE LINE
    DATA "geom from (select geom, osm_id ,railway, name from situation.osm_line_ch where railway='rail') as foo using unique osm_id using srid=2056"
    CLASS
        STYLE
            WIDTH 1
            OUTLINEWIDTH 1
            OUTLINECOLOR "#555554"
            COLOR "#ffffff"
        END
        STYLE
            SYMBOL rail
            GAP -3
            SIZE 4
            COLOR "#555554"
        END
    END
END


LAYER
    NAME "surfaces_tot"
    METADATA
        "wms_title" "Couverture du sol"
        "wms_srs" "EPSG:2056"
    END
    TYPE POLYGON
    STATUS ON
    CONNECTIONTYPE POSTGIS
    CONNECTION "user=${dbuser} password=${dbpassword} dbname=${db} host=${dbhost} port=${dbport}"
    PROCESSING "CLOSE_CONNECTION=DEFER"
    DATA "geom from mensuration.mo6_couverture_du_sol_surf_tot using unique idobj using srid=2056"
    CLASSITEM desnat
    CLASS
        STYLE
            COLOR 255 255 255	
            OUTLINECOLOR 0 0 0
            WIDTH 0.5
        END
    END
    MINSCALEDENOM 0
    MAXSCALEDENOM 2499
END

LAYER
    NAME "surfaces_bois"
    METADATA
        "wms_title" "Surfaces bois"
        "wms_srs" "EPSG:2056"
    END
    TYPE POLYGON
    STATUS ON
    CONNECTIONTYPE POSTGIS
    CONNECTION "user=${dbuser} password=${dbpassword} dbname=${db} host=${dbhost} port=${dbport}"
    PROCESSING "CLOSE_CONNECTION=DEFER"
    DATA "geom from mensuration.mo6_couverture_du_sol_surf_tot using unique idobj using srid=2056"
    CLASSITEM "desnat"
    CLASS
        NAME "Forêt"
        EXPRESSION /forêt/
        STYLE
            SYMBOL "bois_rf"
            COLOR 150 150 150	
            OUTLINECOLOR 0 0 0
            SIZE 5
        END
    END
    CLASS
        NAME "toto"
        EXPRESSION /pâturage boisé/
        STYLE
            SYMBOL "bois_pat"
            COLOR 150 150 150	
            OUTLINECOLOR 0 0 0
            SIZE 7
        END
    END
    CLASS
        NAME "Forêt"
        EXPRESSION /boisée/
        STYLE
            SYMBOL "bois_pat"
            COLOR 150 150 150	
            OUTLINECOLOR 0 0 0
            SIZE 7
        END
    END
    MINSCALEDENOM 0
    MAXSCALEDENOM 2499
END

LAYER
    NAME "surfaces_vignes2"
    METADATA
        "wms_title" "Surfaces vignes"
        "wms_srs" "EPSG:2056"
    END
    TYPE POLYGON
    STATUS ON
    CONNECTIONTYPE POSTGIS
    CONNECTION "user=${dbuser} password=${dbpassword} dbname=${db} host=${dbhost} port=${dbport}"
    PROCESSING "CLOSE_CONNECTION=DEFER"
    DATA "geom from mensuration.mo6_couverture_du_sol_surf_tot using unique idobj using srid=2056"
    CLASSITEM "desnat"
    CLASS
        EXPRESSION /vigne/
        STYLE
            SYMBOL "vigne"
            COLOR 150 150 150	
            SIZE 5
        END
    END
    MINSCALEDENOM 0
    MAXSCALEDENOM 2499
END

LAYER
    NAME "batiments_souterrain"
    METADATA
        "wms_title" "batiments_souterrain"
        "wms_srs" "EPSG:2056"
    END
    TYPE POLYGON
    STATUS ON
    CONNECTIONTYPE POSTGIS
    CONNECTION "user=${dbuser} password=${dbpassword} dbname=${db} host=${dbhost} port=${dbport}"
    PROCESSING "CLOSE_CONNECTION=DEFER"
    DATA "geom from mensuration.mo22_batiments using unique idobj using srid=2056"
    LABELMAXSCALEDENOM 1500
    CLASSITEM "typcou"
    CLASS
        EXPRESSION /souterrain/
        NAME "Souterrains"
        STYLE
            COLOR 255 255 255
            OUTLINECOLOR 0 0 0
        END
    END
    MINSCALEDENOM 50
    MAXSCALEDENOM 24999
END

LAYER
    NAME "batiments_souterrain_gris"
    METADATA
        "wms_title" "batiments_souterrain_gris"
        "wms_srs" "EPSG:2056"
    END
    TYPE POLYGON
    STATUS ON
    CONNECTIONTYPE POSTGIS
    CONNECTION "user=${vars:dbuser} password=${vars:dbpassword} dbname=${vars:db} host=${vars:dbhost} port=${vars:dbport}"
    PROCESSING "CLOSE_CONNECTION=DEFER"
    DATA "geom from mensuration.mo22_batiments using unique idobj using srid=2056"
    LABELMAXSCALEDENOM 1500
    CLASSITEM "typcou"
    CLASS
        EXPRESSION /souterrain/
        NAME "Souterrains"
        STYLE
            COLOR 230 230 230
            OUTLINECOLOR 0 0 0
        END
    END
    MINSCALEDENOM 50
    MAXSCALEDENOM 24999
END

LAYER
    NAME "batiments"
    METADATA
        "wms_title" "Batiments"
        "wms_srs" "EPSG:2056"
    END
    TYPE POLYGON
    STATUS ON
    CONNECTIONTYPE POSTGIS
    CONNECTION "user=${dbuser} password=${dbpassword} dbname=${db} host=${dbhost} port=${dbport}"
    PROCESSING "CLOSE_CONNECTION=DEFER"
    DATA "geom from mensuration.mo22_batiments using unique idobj using srid=2056"
    LABELMAXSCALEDENOM 1500
    CLASSITEM "typcou"
    CLASS
        EXPRESSION /ordinaire/
        NAME "Ordinaires"
        STYLE
            COLOR 255 255 255
            OUTLINECOLOR 0 0 0
        END
    END
    MINSCALEDENOM 50
    MAXSCALEDENOM 24999
END

LAYER
    NAME "batiments_gris"
    METADATA
        "wms_title" "Batiments gris"
        "wms_srs" "EPSG:2056"
    END
    TYPE POLYGON
    STATUS ON
    CONNECTIONTYPE POSTGIS
    CONNECTION "user=${vars:dbuser} password=${vars:dbpassword} dbname=${vars:db} host=${vars:dbhost} port=${vars:dbport}"
    PROCESSING "CLOSE_CONNECTION=DEFER"
    DATA "geom from mensuration.mo22_batiments using unique idobj using srid=2056"
    LABELMAXSCALEDENOM 1500
    CLASSITEM "typcou"
    CLASS
        EXPRESSION /ordinaire/
        NAME "Ordinaires"
        STYLE
            COLOR 200 200 200
            OUTLINECOLOR 0 0 0
        END
    END
    MINSCALEDENOM 50
    MAXSCALEDENOM 24999
END

LAYER
    NAME "parcellaire_officiel"
    METADATA
        "wms_title" "Parcellaire officiel"
        "wms_srs" "EPSG:2056"
    END
    TYPE POLYGON
    STATUS ON
    CONNECTIONTYPE POSTGIS
    CONNECTION "user=${dbuser} password=${dbpassword} dbname=${db} host=${dbhost} port=${dbport}"
    PROCESSING "CLOSE_CONNECTION=DEFER"
    DATA "geom from mensuration.mo9_immeubles using unique idobj using srid=2056"
    OPACITY 70
    CLASSITEM "typimm"
    CLASS
        EXPRESSION /DDP/
        NAME "DDP"
        STYLE
            OUTLINECOLOR 10 10 10 
            PATTERN 7 7 END
            WIDTH 1
        END
    END
    CLASS
        EXPRESSION /DP/
        NAME "DP"
        STYLE
            OUTLINECOLOR 10 10 10 
            PATTERN 7 7 END
            WIDTH 1
        END
    END
    CLASS
        EXPRESSION /./
        NAME "Parcel. officiel"
        STYLE
            OUTLINECOLOR 0 0 0
            WIDTH 1.5
        END
    END
    MINSCALEDENOM 50
    MAXSCALEDENOM 25001
END

LAYER
    NAME "immeubles_txt_rappel"
    METADATA
        "wms_title" "Traits de rappel numéros de parcelles"
        "wms_srs" "EPSG:2056"
    END
    TYPE LINE
    CONNECTIONTYPE POSTGIS
    CONNECTION "user=${dbuser} password=${dbpassword} dbname=${db} host=${dbhost} port=${dbport}"
    PROCESSING "CLOSE_CONNECTION=DEFER"
    DATA "geom from mensuration.mo9_immeubles_txt_rappel using unique idobj using srid=2056"
    STATUS ON
    MINSCALEDENOM 0
    MAXSCALEDENOM 5000
    CLASS
        STYLE
            WIDTH 1
            COLOR 0 0 0
        END
    END
END

LAYER
    NAME "immeubles_txt"
    TYPE POINT
    METADATA
        "ows_title" "immeubles_txt"
        " wms_srs" "epsg:21781"
    END
    CONNECTIONTYPE POSTGIS
    CONNECTION "user=${dbuser} password=${dbpassword} dbname=${db} host=${dbhost} port=${dbport}"
    PROCESSING "CLOSE_CONNECTION=DEFER"
    DATA "geom from mensuration.mo9_immeubles_txt using unique idobj using srid=2056"
    STATUS ON
    LABELITEM "label"
    MAXSCALEDENOM 5000
    SYMBOLSCALE 1000
    LABELMAXSCALEDENOM 5000
    TEMPLATE "ttt"
    CLASS
        LABEL
            TYPE TRUETYPE
            FONT arialbd
            MAXSIZE 11
            SIZE 10
            MINSIZE 7
            ANGLE AUTO
            ANTIALIAS TRUE
            COLOR 0 0 0
            FORCE TRUE
            OUTLINECOLOR 255 255 255
            POSITION cc
        END
    END
END

LAYER
    NAME "mo9_immeubles_txt_conc_hydr"
    TYPE POINT
    METADATA
        "ows_title" "mo9_immeubles_txt_conc_hydr"
        " wms_srs" "epsg:21781"
    END
    CONNECTIONTYPE POSTGIS
    CONNECTION "user=${dbuser} password=${dbpassword} dbname=${db} host=${dbhost} port=${dbport}"
    PROCESSING "CLOSE_CONNECTION=DEFER"
    DATA "geom FROM (SELECT
        idobj,
        geom,
        label_position_mapserver,
        ori_mapserver,
        'CONC HYD ' || nummai::text as label
        from mensuration.mo9_immeubles_txt_conc_hydr) as FOO using unique idobj using srid=2056"
    STATUS ON
    LABELITEM "label"
    MAXSCALEDENOM 4000
    SYMBOLSCALE 1000
    LABELMAXSCALEDENOM 3000
    TEMPLATE "ttt"
    CLASSITEM "label_position_mapserver"
    CLASS
        EXPRESSION "ul"
        STYLE
            # NEEDED, OTHERWISE MAPSERVER THROWS AN ERROR
            # ANNOTATION COULD BE USED, DEPRECATED IN V6.2
        END
        LABEL
            TYPE TRUETYPE
            FONT arialbd
            MAXSIZE 11
            SIZE 10
            MINSIZE 7
            FORCE TRUE
            POSITION ul
            ANGLE [ori_mapserver]
            COLOR 0 0 0
            OUTLINECOLOR 255 255 255
        END
    END
    CLASS
        EXPRESSION "uc"
        STYLE
            # NEEDED, OTHERWISE MAPSERVER THROWS AN ERROR
            # ANNOTATION COULD BE USED, DEPRECATED IN V6.2
        END
        LABEL
            TYPE TRUETYPE
            FONT arialbd
            MAXSIZE 11
            SIZE 10
            MINSIZE 7
            FORCE TRUE
            POSITION uc
            ANGLE [ori_mapserver]
            COLOR 0 0 0
            OUTLINECOLOR 255 255 255
        END
    END
    CLASS
        EXPRESSION "ur"
        STYLE
            # NEEDED, OTHERWISE MAPSERVER THROWS AN ERROR
            # ANNOTATION COULD BE USED, DEPRECATED IN V6.2
        END
        LABEL
            TYPE TRUETYPE
            FONT arialbd
            MAXSIZE 11
            SIZE 10
            MINSIZE 7
            FORCE TRUE
            POSITION ur
            ANGLE [ori_mapserver]
            COLOR 0 0 0
            OUTLINECOLOR 255 255 255
        END
    END
    CLASS
        EXPRESSION "cl"
        STYLE
            # NEEDED, OTHERWISE MAPSERVER THROWS AN ERROR
            # ANNOTATION COULD BE USED, DEPRECATED IN V6.2
        END
        LABEL
            TYPE TRUETYPE
            FONT arialbd
            MAXSIZE 11
            SIZE 10
            MINSIZE 7
            FORCE TRUE
            POSITION cl
            ANGLE [ori_mapserver]
            COLOR 0 0 0
            OUTLINECOLOR 255 255 255
        END
    END
    CLASS
        EXPRESSION "cc"
        STYLE
            # NEEDED, OTHERWISE MAPSERVER THROWS AN ERROR
            # ANNOTATION COULD BE USED, DEPRECATED IN V6.2
        END
        LABEL
            TYPE TRUETYPE
            FONT arialbd
            MAXSIZE 11
            SIZE 10
            MINSIZE 7
            FORCE TRUE
            POSITION cc
            ANGLE [ori_mapserver]
            COLOR 0 0 0
            OUTLINECOLOR 255 255 255
        END
    END
    CLASS
        EXPRESSION "cr"
        STYLE
            # NEEDED, OTHERWISE MAPSERVER THROWS AN ERROR
            # ANNOTATION COULD BE USED, DEPRECATED IN V6.2
        END
        LABEL
            TYPE TRUETYPE
            FONT arialbd
            MAXSIZE 11
            SIZE 10
            MINSIZE 7
            FORCE TRUE
            POSITION cr
            ANGLE [ori_mapserver]
            COLOR 0 0 0
            OUTLINECOLOR 255 255 255
        END
    END
    CLASS
        EXPRESSION /ll/
        STYLE
            # NEEDED, OTHERWISE MAPSERVER THROWS AN ERROR
            # ANNOTATION COULD BE USED, DEPRECATED IN V6.2
        END
        LABEL
            TYPE TRUETYPE
            FONT arialbd
            MAXSIZE 11
            SIZE 10
            MINSIZE 7
            FORCE TRUE
            POSITION ll
            ANGLE [ori_mapserver]
            COLOR 0 0 0
            OUTLINECOLOR 255 255 255
        END
    END
    CLASS
        EXPRESSION "lc"
        STYLE
            # NEEDED, OTHERWISE MAPSERVER THROWS AN ERROR
            # ANNOTATION COULD BE USED, DEPRECATED IN V6.2
        END
        LABEL
            TYPE TRUETYPE
            FONT arialbd
            MAXSIZE 11
            SIZE 10
            MINSIZE 7
            FORCE TRUE
            POSITION lc
            ANGLE [ori_mapserver]
            COLOR 0 0 0
            OUTLINECOLOR 255 255 255
        END
    END
    CLASS
        EXPRESSION "lr"
        STYLE
            # NEEDED, OTHERWISE MAPSERVER THROWS AN ERROR
            # ANNOTATION COULD BE USED, DEPRECATED IN V6.2
        END
        LABEL
            TYPE TRUETYPE
            FONT arialbd
            MAXSIZE 11
            SIZE 10
            MINSIZE 7
            FORCE TRUE
            POSITION lr
            ANGLE [ori_mapserver]
            COLOR 0 0 0
            OUTLINECOLOR 255 255 255
        END
    END
END

LAYER
    NAME "pts_limites"
    METADATA
        "wms_title" "Points limites"
        "wms_srs" "EPSG:2056"
    END
    TYPE POINT
    CONNECTIONTYPE POSTGIS
    CONNECTION "user=${dbuser} password=${dbpassword} dbname=${db} host=${dbhost} port=${dbport}"
    PROCESSING "CLOSE_CONNECTION=DEFER"
    DATA "geom from mensuration.mo5_point_de_detail using unique idobj using srid=2056"
    STATUS ON
    MINSCALEDENOM 0
    MAXSCALEDENOM 1900
    CLASSITEM "nature"
    CLASS
        NAME "Borne"
        EXPRESSION ([nature] = 1 AND [gros_borne] = 1)
        STYLE
            SYMBOL "circle"
            SIZE 7
            COLOR 255 255 255
            OUTLINECOLOR 0 0 0
        END
    END
    CLASS
        NAME "Cheville"
        EXPRESSION ([nature] = 2 AND [gros_borne] = 1)
        STYLE
            SYMBOL "circle"
            SIZE 5
            COLOR 255 255 255
            OUTLINECOLOR 0 0 0
        END
    END  
    CLASS
        NAME "Croix"
        EXPRESSION ([nature] = 3 AND [gros_borne] = 1)
        STYLE
            SYMBOL "croix"
        END
    END  
    CLASS
        NAME "Pieu, piquet"
        EXPRESSION ([nature] = 4 AND [gros_borne] = 1)
        STYLE
            SYMBOL "circle"
            SIZE 3
            COLOR 255 255 255
            OUTLINECOLOR 0 0 0
        END
    END
    CLASS
        NAME "Non mat."
        EXPRESSION ([nature] = 5 AND [gros_borne] = 1)
        STYLE
            SYMBOL "circle"
            SIZE 4
            COLOR 0 0 0
            OUTLINECOLOR 255 255 255
        END
    END
    CLASS
        NAME "Borne artif."
        EXPRESSION ([nature] = 6 AND [gros_borne] = 1)
        STYLE
            SYMBOL "circle"
            SIZE 7
            COLOR 255 255 255
            OUTLINECOLOR 0 0 0
        END
    END
    CLASS
        NAME "Tuyau"
        EXPRESSION ([nature] = 7 AND [gros_borne] = 1)
        STYLE
            SYMBOL "circle"
            SIZE 3
            COLOR 255 255 255
            OUTLINECOLOR 0 0 0
        END
    END
    CLASS
        NAME "Borne territoriale"
        EXPRESSION ([nature] = 1 AND [gros_borne] = 0)
        STYLE
            SYMBOL "circle"
            SIZE 7
            COLOR 255 255 255
            OUTLINECOLOR 0 0 0
        END
        STYLE
            SYMBOL "circle"
            SIZE 14
            OUTLINECOLOR 0 0 0
        END
    END
    CLASS
        NAME "Cheville / borne territoriale"
        EXPRESSION ([nature] = 2 AND [gros_borne] = 0)
        STYLE
            SYMBOL "circle"
            SIZE 5
            COLOR 255 255 255
            OUTLINECOLOR 0 0 0
        END
        STYLE
            SYMBOL "circle"
            SIZE 14
            OUTLINECOLOR 0 0 0
        END
    END
    CLASS
        NAME "Croix / borne territoriale"
        EXPRESSION ([nature] = 3 AND [gros_borne] = 0)
        STYLE
            SYMBOL "croix"
        END
        STYLE
            SYMBOL "circle"
            SIZE 14
            OUTLINECOLOR 0 0 0
        END
    END
    CLASS
        NAME "Pieu, piquet / borne territoriale"
        EXPRESSION ([nature] = 4 AND [gros_borne] = 0)
        STYLE
            SYMBOL "circle"
            SIZE 3
            COLOR 255 255 255
            OUTLINECOLOR 0 0 0
        END
        STYLE
            SYMBOL "circle"
            SIZE 14
            OUTLINECOLOR 0 0 0
        END
    END
    CLASS
        NAME "Non mat. / borne territoriale"
        EXPRESSION ([nature] = 5 AND [gros_borne] = 0)
        STYLE
            SYMBOL "circle"
            SIZE 4
            COLOR 0 0 0
            OUTLINECOLOR 255 255 255
        END
        STYLE
            SYMBOL "circle"
            SIZE 14
            OUTLINECOLOR 0 0 0
        END
    END
    CLASS
        NAME "Borne artif. territoriale"
        EXPRESSION ([nature] = 6 AND [gros_borne] = 0)
        STYLE
            SYMBOL "circle"
            SIZE 7
            COLOR 255 255 255
            OUTLINECOLOR 0 0 0
        END
        STYLE
            SYMBOL "circle"
            SIZE 14
            OUTLINECOLOR 0 0 0
        END
    END
    CLASS
        NAME "Tuyau / borne territoriale"
        EXPRESSION ([nature] = 7 AND [gros_borne] = 0)
        STYLE
            SYMBOL "circle"
            SIZE 3
            COLOR 255 255 255
            OUTLINECOLOR 0 0 0
        END
        STYLE
            SYMBOL "circle"
            SIZE 14
            OUTLINECOLOR 0 0 0
        END
    END
END

LAYER
    NAME "obj_divers_couvert"
    METADATA
        "wms_title" "Objets divers couverts"
        "wms_srs" "EPSG:2056"
    END
    TYPE POLYGON
    CONNECTIONTYPE POSTGIS
    CONNECTION "user=${dbuser} password=${dbpassword} dbname=${db} host=${dbhost} port=${dbport}"
    PROCESSING "CLOSE_CONNECTION=DEFER"
    DATA "geom from (SELECT
        *
        FROM mensuration.mo7_obj_divers_surface
        WHERE genre = 14
        ) as foo using unique idobj using srid=2056"
    STATUS ON
    MINSCALEDENOM 0
    MAXSCALEDENOM 2499
    CLASS
        STYLE
            PATTERN 3 3 END
            OUTLINECOLOR 0 0 0
            WIDTH 0.5
        END
    END
END

LAYER
    NAME "obj_divers_cordbois"
    METADATA
        "wms_title" "Objets divers cordons boisés"
        "wms_srs" "EPSG:2056"
    END
    TYPE POLYGON
    CONNECTIONTYPE POSTGIS
    CONNECTION "user=${dbuser} password=${dbpassword} dbname=${db} host=${dbhost} port=${dbport}"
    PROCESSING "CLOSE_CONNECTION=DEFER"
    DATA "geom from (SELECT
        *
        FROM mensuration.mo7_obj_divers_surface
        WHERE genre = 27
        ) as foo using unique idobj using srid=2056"
    STATUS ON
    MINSCALEDENOM 0
    MAXSCALEDENOM 2499
    CLASS
        STYLE
            OUTLINECOLOR 0 0 0
            SYMBOL "bois"
            SIZE 0.5
        END
    END
END

LAYER
    NAME "obj_divers_piscine"
    METADATA
        "wms_title" "Objets divers piscines"
        "wms_srs" "EPSG:2056"
    END
    TYPE LINE # ET NE PAS POLYGON POUR EVITER REMPLISSAGE NOIR
    CONNECTIONTYPE POSTGIS
    CONNECTION "user=${dbuser} password=${dbpassword} dbname=${db} host=${dbhost} port=${dbport}"
    PROCESSING "CLOSE_CONNECTION=DEFER"
    DATA "geom from (SELECT
        *
        FROM mensuration.mo7_obj_divers_surface
        WHERE genre = 44
        ) as foo using unique idobj using srid=2056"
    STATUS ON
    MINSCALEDENOM 0
    MAXSCALEDENOM 2499
    CLASS
        STYLE
            COLOR 0 0 0
            PATTERN 5 5 END
            WIDTH 0.5
        END
    END
END

LAYER
    NAME "obj_divers_batsout15m"
    TYPE LINE
    METADATA
        "ows_title" "obj_divers_batsout15m"
        "wms_srs" "epsg:21781"
    END
    CONNECTIONTYPE POSTGIS
    CONNECTION "user=${dbuser} password=${dbpassword} dbname=${db} host=${dbhost} port=${dbport}"
    PROCESSING "CLOSE_CONNECTION=DEFER"
    DATA "geom from (SELECT
        *
        FROM mensuration.mo7_obj_divers_lineaire
        WHERE genre = 1
        ) as foo using unique idobj using srid=2056"
    STATUS ON
    MINSCALEDENOM 0
    MAXSCALEDENOM 2499
    CLASS
        NAME "Bâtiments souterrain, surf. < 15m2"
        STYLE
            COLOR 130 130 130
            PATTERN
                2 3
            END
            WIDTH 1
        END
    END
END

LAYER
    NAME "obj_divers_lineaire"
    METADATA
        "wms_title" "Objets divers lineaires"
        "wms_srs" "EPSG:2056"
    END
    TYPE LINE
    CONNECTIONTYPE POSTGIS
    CONNECTION "user=${dbuser} password=${dbpassword} dbname=${db} host=${dbhost} port=${dbport}"
    PROCESSING "CLOSE_CONNECTION=DEFER"
    DATA "geom from (SELECT
        *
        FROM mensuration.mo7_obj_divers_lineaire
        WHERE genre not in (1, 14, 27, 44)
        ) as foo using unique idobj using srid=2056"
    STATUS ON
    MINSCALEDENOM 0
    MAXSCALEDENOM 2499
    CLASSITEM "typline"
    CLASS
        # DISCONTINU2
        EXPRESSION "3"
        STYLE
            COLOR 80 80 80
            PATTERN 7 7 END
            WIDTH 0.5
        END
    END
    CLASS
        # CONTINU
        EXPRESSION "0"
        STYLE
          WIDTH 0.5
          COLOR 100 100 100
        END
    END
    CLASS
        # POINTILLE
        EXPRESSION "5"
        STYLE
            COLOR 80 80 80
            PATTERN 2 2 END
            WIDTH 0.5
        END
    END
    CLASS
        # MIXTE 1
        EXPRESSION "6"
        STYLE
            COLOR 80 80 80
            PATTERN 28 4 4 4 END
            WIDTH 0.5
        END
    END
    CLASS
        # MIXTE 2
        EXPRESSION "7"
        STYLE
            COLOR 80 80 80
            PATTERN 28 4 4 4 4 4 END
            WIDTH 0.5
        END
    END
END

LAYER
    NAME "obj_divers_surface_lig"
    METADATA
        "wms_title" "Objets divers surfaciques (lignes)"
        "wms_srs" "EPSG:2056"
    END
    TYPE LINE
    CONNECTIONTYPE POSTGIS
    CONNECTION "user=${dbuser} password=${dbpassword} dbname=${db} host=${dbhost} port=${dbport}"
    PROCESSING "CLOSE_CONNECTION=DEFER"
    DATA "geom from (SELECT
        *
        FROM mensuration.mo7_obj_divers_surface_lig
        WHERE genre not in (1, 14, 27, 44)
        ) as foo using unique idobj using srid=2056"
    STATUS ON
    MINSCALEDENOM 0
    MAXSCALEDENOM 25001
    CLASSITEM "typline"
CLASS
        # DISCONTINU2
        EXPRESSION "3"
        STYLE
            COLOR 80 80 80
            PATTERN 7 7 END
            WIDTH 0.5
        END
    END
    CLASS
        # CONTINU
        EXPRESSION "0"
        STYLE
          WIDTH 0.5
          COLOR 100 100 100
        END
    END
    CLASS
        # POINTILLE
        EXPRESSION "5"
        STYLE
            COLOR 80 80 80
            PATTERN 2 2 END
            WIDTH 0.5
        END
    END
    CLASS
        # MIXTE 1
        EXPRESSION "6"
        STYLE
            COLOR 80 80 80
            PATTERN 28 4 4 4 END
            WIDTH 0.5
        END
    END
    CLASS
        # MIXTE 2
        EXPRESSION "7"
        STYLE
            COLOR 80 80 80
            PATTERN 28 4 4 4 4 4 END
            WIDTH 0.5
        END
    END
END

LAYER
    NAME "obj_divers_ponctuels"
    METADATA
        "wms_title" "Objets divers ponctuels"
        "wms_srs" "EPSG:2056"
    END
    TYPE POINT
    CONNECTIONTYPE POSTGIS
    CONNECTION "user=${dbuser} password=${dbpassword} dbname=${db} host=${dbhost} port=${dbport}"
    PROCESSING "CLOSE_CONNECTION=DEFER"
    DATA "geom from mensuration.mo7_obj_divers_ponctuels using unique idobj using srid=2056"
    STATUS ON
    CLASSITEM "genre_txt"
    CLASS
        NAME "Arbre isolé important"
        EXPRESSION "arbre_isole_important"
        STYLE
            MINSCALEDENOM 0
            MAXSCALEDENOM 1001
            COLOR 0 0 0
            SYMBOL "arbre_isole_important"
            SIZE 18
        END
        STYLE
            MINSCALEDENOM 1001
            MAXSCALEDENOM 2499
            COLOR 0 0 0
            SYMBOL "arbre_isole_important"
            SIZE 10
        END
    END
    CLASS
        NAME "Bloc erratique"
        EXPRESSION "bloc_erratique"
        STYLE
            MINSCALEDENOM 0
            MAXSCALEDENOM 1001
            SYMBOL "bloc_erratique"
            SIZE 18
            COLOR 0 0 0
        END
        STYLE
            MINSCALEDENOM 1001
            MAXSCALEDENOM 2499
            SYMBOL "bloc_erratique"
            SIZE 10
            COLOR 0 0 0
        END
    END
    CLASS
        NAME "Grotte - entrée de caverne"
        EXPRESSION "grotte_entree_de_caverne"
        STYLE
            MINSCALEDENOM 0
            MAXSCALEDENOM 1001
            COLOR 0 0 0
            SYMBOL "grotte_entree_de_caverne"
            SIZE 15
        END
        STYLE
            MINSCALEDENOM 1001
            MAXSCALEDENOM 2499
            COLOR 0 0 0
            SYMBOL "grotte_entree_de_caverne"
            SIZE 9
        END
    END
    CLASS
        NAME "Mât / antenne"
        EXPRESSION "mat_antenne"
        STYLE
            MINSCALEDENOM 0
            MAXSCALEDENOM 1001
            COLOR 0 0 0
            SYMBOL "mat_antenne"
            SIZE 18
        END
        STYLE
            MINSCALEDENOM 1001
            MAXSCALEDENOM 2499
            COLOR 0 0 0
            SYMBOL "mat_antenne"
            SIZE 10
        END
    END
    CLASS
        NAME "Monument"
        EXPRESSION "monument"
        STYLE
            MINSCALEDENOM 0
            MAXSCALEDENOM 1001
            COLOR 0 0 0
            SYMBOL "monument_2"
            SIZE 18
        END
        STYLE
            MINSCALEDENOM 1001
            MAXSCALEDENOM 2499
            COLOR 0 0 0
            SYMBOL "monument_2"
            SIZE 10
        END
    END
    CLASS
        NAME "Piscine"
        EXPRESSION "piscine"
        STYLE
            MINSCALEDENOM 0
            MAXSCALEDENOM 1001
            COLOR 0 0 0
            SYMBOL "piscine"
            SIZE 18
        END
        STYLE
            MINSCALEDENOM 1001
            MAXSCALEDENOM 2499
            COLOR 0 0 0
            SYMBOL "piscine"
            SIZE 10
        END
    END
    CLASS
        NAME "Point de référence"
        EXPRESSION "point_de_reference"
        STYLE
            MINSCALEDENOM 0
            MAXSCALEDENOM 1001
            COLOR 0 0 0
            SYMBOL "point_de_reference"
            SIZE 18
        END
        STYLE
            MINSCALEDENOM 1001
            MAXSCALEDENOM 2499
            COLOR 0 0 0
            SYMBOL "point_de_reference"
            SIZE 10
        END
    END
    CLASS
        NAME "Source"
        EXPRESSION "source"
        STYLE
            MINSCALEDENOM 0
            MAXSCALEDENOM 1001
            COLOR 0 0 0
            SYMBOL "source_new"
            SIZE 18
        END
        STYLE
            MINSCALEDENOM 1001
            MAXSCALEDENOM 2499
            COLOR 0 0 0
            SYMBOL "source_new"
            SIZE 10
        END
    END
    CLASS
        NAME "Statue / crucifix"
        EXPRESSION "statue_crucifix"
        STYLE
            MINSCALEDENOM 0
            MAXSCALEDENOM 1001
            COLOR 0 0 0
            SYMBOL "statue_crucifix"
            SIZE 18
        END
        STYLE
            MINSCALEDENOM 1001
            MAXSCALEDENOM 2499
            COLOR 0 0 0
            SYMBOL "statue_crucifix"
            SIZE 10
        END
    END
END

LAYER
    NAME "pts_fixes"
    METADATA
        "wms_title" "Points fixes"
        "wms_srs" "EPSG:2056"
    END
    TYPE POINT
    CONNECTIONTYPE POSTGIS
    CONNECTION "user=${dbuser} password=${dbpassword} dbname=${db} host=${dbhost} port=${dbport}"
    PROCESSING "CLOSE_CONNECTION=DEFER"
    DATA "geom from mensuration.v_pts_fixes using unique nopoin using srid=2056"
    STATUS ON
    CLASSITEM "valeur"
    CLASS
        NAME "PFP3"
        EXPRESSION /22/	
        STYLE
            SYMBOL "circle"
            SIZE 7
            COLOR 255 255 255
        END
        STYLE
            SYMBOL "pfp_3"
            SIZE 7
            COLOR 0 0 0
        END
        MINSCALEDENOM 0
        MAXSCALEDENOM 5100
    END  
    CLASS
        NAME "PFP1/2"
        EXPRESSION /11/
        STYLE    
            SYMBOL "triangle"
            SIZE 8
            COLOR 255 255 255 
        END
        STYLE    
            SYMBOL "triangle"
            SIZE 8
            OUTLINECOLOR 0 0 0
            WIDTH 1
        END
        STYLE    
            SYMBOL "triangle"
            SIZE 2.5
            COLOR 0 0 0
            OFFSET 0 1.2
        END
        MINSCALEDENOM 0
        MAXSCALEDENOM 50000
    END
    TOLERANCE 5
    TOLERANCEUNITS pixels
END

LAYER
    NAME "mo25_lieux_dits"
    METADATA
        "wms_title" "mo25_lieux_dits"
        "wms_srs" "EPSG:2056"
    END
    TYPE POINT
    CONNECTIONTYPE POSTGIS
    CONNECTION "user=${dbuser} password=${dbpassword} dbname=${db} host=${dbhost} port=${dbport}"
    PROCESSING "CLOSE_CONNECTION=DEFER"
    DATA "geom from mensuration.mo25_lieux_dits using unique idobj using srid=2056"
    STATUS ON
    MAXSCALEDENOM 7499
    LABELITEM "nomloc"
    LABELMAXSCALEDENOM 2500
    SYMBOLSCALEDENOM 2500
    CLASSITEM "nomloc"
    CLASS
        EXPRESSION /./
        LABEL
            TYPE TRUETYPE
            FONT arialbi
            MAXSIZE 12
            SIZE 11
            MINSIZE 9
            ANGLE AUTO
            ANTIALIAS TRUE
            COLOR 130 130 130
            OUTLINECOLOR 255 255 255    
        END
    END
END

LAYER
    NAME "noms_locaux_canton"
    METADATA
        "wms_title" "Noms locaux"
        "wms_srs" "EPSG:2056"
    END
    TYPE POINT
    CONNECTIONTYPE POSTGIS
    CONNECTION "user=${dbuser} password=${dbpassword} dbname=${db} host=${dbhost} port=${dbport}"
    PROCESSING "CLOSE_CONNECTION=DEFER"
    DATA "geom from situation.noms_locaux_canton_points using unique idobj using srid=2056"
    STATUS ON
    MAXSCALEDENOM 7499
    LABELITEM "nomloc"
    LABELMAXSCALEDENOM 2500
    SYMBOLSCALEDENOM 2500
    CLASSITEM "nomloc"
    OPACITY 100    
    CLASS
        EXPRESSION /./
        LABEL
            TYPE TRUETYPE
            FONT arialbi
            MAXSIZE 11
            SIZE 10
            MINSIZE 8
            ANGLE AUTO
            ANTIALIAS TRUE
            COLOR 130 130 130
            OUTLINECOLOR 255 255 255    
        END
    END
END

LAYER
    NAME "point_adresse"
    METADATA
        "wms_title" "Points adresses"
        "wms_srs" "EPSG:2056"
    END
    TYPE POINT
    CONNECTIONTYPE POSTGIS
    CONNECTION "user=${dbuser} password=${dbpassword} dbname=${db} host=${dbhost} port=${dbport}"
    PROCESSING "CLOSE_CONNECTION=DEFER"
    DATA "geom from mensuration.mo02_adresses_sitn using unique idobj using srid=2056"
    STATUS ON
    LABELITEM "numuni"
    MAXSCALEDENOM 5001
    LABELMAXSCALEDENOM 2500
    CLASSITEM "numuni"
    CLASS
        EXPRESSION /1|2|3|4|5|6|7|8|9/ #([numuni]="1")
        LABEL
            TYPE TRUETYPE
            FONT verdanab
            MAXSIZE 8
            SIZE 6
            MINSIZE 6
            ANGLE AUTO
            COLOR 0 0 0 
            OUTLINECOLOR 240 240 240   
        END
    END
END

LAYER
    NAME "voie_adresse"
    METADATA
        "wms_title" "Voie adresses"
        "wms_srs" "EPSG:2056"
    END
    TYPE LINE
    CONNECTIONTYPE POSTGIS
    CONNECTION "user=${dbuser} password=${dbpassword} dbname=${db} host=${dbhost} port=${dbport}"
    PROCESSING "CLOSE_CONNECTION=DEFER"
    DATA "geom from situation.troncon_rue using unique idobj using srid=2056"
    STATUS ON
    MAXSCALEDENOM 5001
    LABELITEM "feat_name"
    LABELMAXSCALEDENOM 5001
    SYMBOLSCALE 2000
    OPACITY 100
    CLASS
        LABEL
            TYPE TRUETYPE
            FONT arialn
            MAXSIZE 10
            SIZE 10
            MINSIZE 8
            ANGLE follow
            ANTIALIAS TRUE
            COLOR 0 0 0
            OUTLINECOLOR 255 255 255
        END
    END
END

LAYER
    NAME "nomenclature_lieux"
    METADATA  
        "wms_title" "Nomenclature des lieux dits - localités"
        "wms_srs" "EPSG:2056"
    END
    TYPE POINT
    STATUS ON
    CONNECTIONTYPE POSTGIS
    CONNECTION "user=${dbuser} password=${dbpassword} dbname=${db} host=${dbhost} port=${dbport}"
    PROCESSING "CLOSE_CONNECTION=DEFER"
    DATA "geom from situation.noms_lieux using unique idobj using srid=2056"  
    LABELITEM "libgeo"
    CLASS
        LABEL
            TYPE TRUETYPE
            FONT verdanabi
            MAXSIZE 10
            SIZE 9
            MINSIZE 9
            PRIORITY 8
            POSITION uc
            ANTIALIAS TRUE
            COLOR 40 40 40 
            OUTLINECOLOR 240 240 240   
        END
        MINSCALEDENOM 0
        MAXSCALEDENOM 20000
    END
    CLASS
        LABEL
            TYPE TRUETYPE
            FONT verdanai
            MAXSIZE 9
            SIZE 9
            MINSIZE 7
            PRIORITY 8
            POSITION uc
            ANTIALIAS TRUE
            COLOR 120 120 120 
            OUTLINECOLOR 240 240 240   
       END
       MINSCALEDENOM 20000
       MAXSCALEDENOM 80000
    END
END

LAYER
    NAME "nomenclature_communes"
    METADATA
        "wms_title" "Situation nomenclature communes"
        "wms_srs" "EPSG:2056"
    END
    TYPE POINT
    CONNECTIONTYPE POSTGIS
    CONNECTION "user=${dbuser} password=${dbpassword} dbname=${db} host=${dbhost} port=${dbport}"
    PROCESSING "CLOSE_CONNECTION=DEFER"
    DATA "geom from situation.situ_nomenclature1 using unique idobj using srid=2056"  
    STATUS ON
    LABELITEM "libgeo"
    MINSCALEDENOM 2001
    MAXSCALEDENOM 250000
    CLASS
        LABEL
            TYPE TRUETYPE
            FONT verdanab
            MAXSIZE 9
            SIZE 9
            MINSIZE 8
            ANGLE AUTO
            ANTIALIAS TRUE
            PRIORITY 9
            POSITION uc
            COLOR 90 90 90 
            OUTLINECOLOR 240 240 240   
        END
    END
END

LAYER
    NAME "nomenclature_villes"
    METADATA
        "wms_title" "Situation nomenclature villes"
        "wms_srs" "EPSG:2056"
    END
    TYPE POINT
    CONNECTIONTYPE POSTGIS
    CONNECTION "user=${dbuser} password=${dbpassword} dbname=${db} host=${dbhost} port=${dbport}"
    PROCESSING "CLOSE_CONNECTION=DEFER"
    DATA "geom from situation.situ_nomenclature3 using unique idobj using srid=2056"  
    STATUS ON
    LABELITEM "libgeo"
    MINSCALEDENOM 2001
    MAXSCALEDENOM 250000
    CLASS
        LABEL
            TYPE TRUETYPE
            FONT verdanabi
            MAXSIZE 12
            SIZE 10
            MINSIZE 10
            ANGLE AUTO
            PRIORITY 10
            ANTIALIAS TRUE
            COLOR 70 70 70 
            OUTLINECOLOR 240 240 240
        END
    END
END

LAYER
    NAME "mo6_couverture_du_sol_nomenclature"
    METADATA
        "wms_title" "mo6_couverture_du_sol_nomenclature"
        "wms_srs" "EPSG:2056"
    END
    TYPE POINT
    STATUS ON
    CONNECTIONTYPE POSTGIS
    CONNECTION "user=${dbuser} password=${dbpassword} dbname=${db} host=${dbhost} port=${dbport}"
    PROCESSING "CLOSE_CONNECTION=DEFER"
    DATA "geom from mensuration.mo6_couverture_du_sol_nomenclature using unique idobj using srid=2056"
    MINSCALEDENOM 0
    MAXSCALEDENOM 1500
    LABELITEM "nom"
    CLASSITEM "label_position_mapserver"
    CLASS
        EXPRESSION "ul"
        STYLE
            # NEEDED, OTHERWISE MAPSERVER THROWS AN ERROR
            # ANNOTATION COULD BE USED, DEPRECATED IN V6.2
        END
        LABEL
            TYPE TRUETYPE
            FONT verdana
            SIZE 6
            FORCE TRUE
            POSITION ul
            ANGLE [ori_mapserver]
            COLOR 0 0 0
            OUTLINECOLOR 255 255 255
        END
    END
    CLASS
        EXPRESSION "uc"
        STYLE
            # NEEDED, OTHERWISE MAPSERVER THROWS AN ERROR
            # ANNOTATION COULD BE USED, DEPRECATED IN V6.2
        END
        LABEL
            TYPE TRUETYPE
            FONT verdana
            SIZE 6
            FORCE TRUE
            POSITION uc
            ANGLE [ori_mapserver]
            COLOR 0 0 0
            OUTLINECOLOR 255 255 255
        END
    END
    CLASS
        EXPRESSION "ur"
        STYLE
            # NEEDED, OTHERWISE MAPSERVER THROWS AN ERROR
            # ANNOTATION COULD BE USED, DEPRECATED IN V6.2
        END
        LABEL
            TYPE TRUETYPE
            FONT verdana
            SIZE 6
            FORCE TRUE
            POSITION ur
            ANGLE [ori_mapserver]
            COLOR 0 0 0
            OUTLINECOLOR 255 255 255
        END
    END
    CLASS
        EXPRESSION "cl"
        STYLE
            # NEEDED, OTHERWISE MAPSERVER THROWS AN ERROR
            # ANNOTATION COULD BE USED, DEPRECATED IN V6.2
        END
        LABEL
            TYPE TRUETYPE
            FONT verdana
            SIZE 6
            FORCE TRUE
            POSITION cl
            ANGLE [ori_mapserver]
            COLOR 0 0 0
            OUTLINECOLOR 255 255 255
        END
    END
    CLASS
        EXPRESSION "cc"
        STYLE
            # NEEDED, OTHERWISE MAPSERVER THROWS AN ERROR
            # ANNOTATION COULD BE USED, DEPRECATED IN V6.2
        END
        LABEL
            TYPE TRUETYPE
            FONT verdana
            SIZE 6
            FORCE TRUE
            POSITION cc
            ANGLE [ori_mapserver]
            COLOR 0 0 0
            OUTLINECOLOR 255 255 255
        END
    END
    CLASS
        EXPRESSION "cr"
        STYLE
            # NEEDED, OTHERWISE MAPSERVER THROWS AN ERROR
            # ANNOTATION COULD BE USED, DEPRECATED IN V6.2
        END
        LABEL
            TYPE TRUETYPE
            FONT verdana
            SIZE 6
            FORCE TRUE
            POSITION cr
            ANGLE [ori_mapserver]
            COLOR 0 0 0
            OUTLINECOLOR 255 255 255
        END
    END
    CLASS
        EXPRESSION /ll/
        STYLE
            # NEEDED, OTHERWISE MAPSERVER THROWS AN ERROR
            # ANNOTATION COULD BE USED, DEPRECATED IN V6.2
        END
        LABEL
            TYPE TRUETYPE
            FONT verdana
            SIZE 6
            FORCE TRUE
            POSITION ll
            ANGLE [ori_mapserver]
            COLOR 0 0 0
            OUTLINECOLOR 255 255 255
        END
    END
    CLASS
        EXPRESSION "lc"
        STYLE
            # NEEDED, OTHERWISE MAPSERVER THROWS AN ERROR
            # ANNOTATION COULD BE USED, DEPRECATED IN V6.2
        END
        LABEL
            TYPE TRUETYPE
            FONT verdana
            SIZE 6
            FORCE TRUE
            POSITION lc
            ANGLE [ori_mapserver]
            COLOR 0 0 0
            OUTLINECOLOR 255 255 255
        END
    END
    CLASS
        EXPRESSION "lr"
        STYLE
            # NEEDED, OTHERWISE MAPSERVER THROWS AN ERROR
            # ANNOTATION COULD BE USED, DEPRECATED IN V6.2
        END
        LABEL
            TYPE TRUETYPE
            FONT verdana
            SIZE 6
            FORCE TRUE
            POSITION lr
            ANGLE [ori_mapserver]
            COLOR 0 0 0
            OUTLINECOLOR 255 255 255
        END
    END
END

END
