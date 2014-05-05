from sqlalchemy import(
    Column, 
    Sequence, 
    Integer, 
    Text,
    String, 
    Boolean, 
    ForeignKey, 
    Float)
    
from sqlalchemy.orm import relationship, backref, deferred

from zope.sqlalchemy import ZopeTransactionExtension

import sqlahelper

DBSession = sqlahelper.get_session()

from papyrus.geo_interface import GeoInterface
from geoalchemy import (
    GeometryColumn, 
    Geometry, 
    Polygon,
    WKTSpatialElement,
    GeometryDDL#,
#    WKBSpatialElement
    )

from crdppf import db_config

srid_ = db_config['srid']

Base = sqlahelper.get_base()

# Models for the configuration of the application
class AppConfig(Base):
    __tablename__ = 'appconfig'
    __table_args__ = {'schema': db_config['schema'], 'autoload': True}
    
# START models used for static extraction and general models
class Topics(Base):
    __tablename__ = 'topic'
    __table_args__ = {'schema': db_config['schema'], 'autoload': True}
    layers = relationship("Layers", backref=backref("layers"),lazy="joined")
    authorityfk = Column(Integer, ForeignKey('crdppf.authority.authorityid'))
    authority = relationship("Authority", backref=backref("authority"),lazy="joined")
    legalbases = relationship("LegalBases", backref=backref("legalbases"),lazy="joined")
    legalprovisions = relationship("LegalProvisions", backref=backref("legalprovisions"),lazy="joined")
    temporaryprovisions = relationship("TemporaryProvisions", backref=backref("temporaryprovisions"),lazy="joined")
    references = relationship("References", backref=backref("references"),lazy="joined")
    
class Layers(Base):
    __tablename__ = 'layers'
    __table_args__ = {'schema': db_config['schema'], 'autoload': True}
    topicfk = Column(String(10), ForeignKey('crdppf.topic.topicid'))
    topic = relationship("Topics", backref=backref("topic"),lazy="joined")

class Documents(Base):
    __tablename__ = 'documents_saisies'
    __table_args__ = {'schema': db_config['schema'], 'autoload': True}
    
class Authority(Base):
    __tablename__ = 'authority'
    __table_args__ = {'schema': db_config['schema'], 'autoload': True}

class LegalBases(Base):
    __tablename__ = 'legalbases'
    __table_args__ = {'schema': db_config['schema'], 'autoload': True}
    topicfk = Column(String(10), ForeignKey('crdppf.topic.topicid'))

class LegalProvisions(Base):
    __tablename__ = 'legalprovisions'
    __table_args__ = {'schema': db_config['schema'], 'autoload': True}
    topicfk = Column(String(10), ForeignKey('crdppf.topic.topicid')) 

class TemporaryProvisions(Base):
    __tablename__ = 'temporaryprovisions'
    __table_args__ = {'schema': db_config['schema'], 'autoload': True}
    topicfk = Column(String(10), ForeignKey('crdppf.topic.topicid'))

class References(Base):
    __tablename__ = 'references'
    __table_args__ = {'schema': db_config['schema'], 'autoload': True}
    topicfk = Column(String(10), ForeignKey('crdppf.topic.topicid'))

class PaperFormats(Base):
    __tablename__ = 'paperformats'
    __table_args__ = {'schema': db_config['schema'], 'autoload': True}

class Translations(Base):
    __tablename__ = 'translations'
    __table_args__ = {'schema': db_config['schema'], 'autoload': True}
    
class Themes(Base):
    __tablename__ = 'themes'
    __table_args__ = {'schema': db_config['schema'], 'autoload': True}


# DATA SECTION

if 'town' in db_config['tables']:
    table_def_ = db_config['tables']['town']
    if 'att_cadastre_number' in table_def_:
        class Town(GeoInterface,Base):
            __tablename__ = table_def_['tablename']
            __table_args__ = {'schema': table_def_['schema'], 'autoload': True}
            idobj = Column(table_def_['att_id'], Integer, primary_key=True)
            numcad = Column(table_def_['att_cadastre_number'], Integer)
            numcom = Column(table_def_['att_commune_number'], Integer)
            comnom = Column(table_def_['att_commune_name'], String)
            cadnom = Column(table_def_['att_cadastre_name'], String)
            nufeco = Column(table_def_['att_federal_number'], Integer)
            geom =GeometryColumn(Geometry(2, srid=srid_))
    else:
        class Town(GeoInterface,Base):
            __tablename__ = table_def_['tablename']
            __table_args__ = {'schema': table_def_['schema'], 'autoload': True}
            idobj = Column(table_def_['att_id'], Integer, primary_key=True)
            numcom = Column(table_def_['att_commune_number'], Integer)
            comnom = Column(table_def_['att_commune_name'], String)
            nufeco = Column(table_def_['att_federal_number'], Integer)
            geom =GeometryColumn(Geometry(2, srid=srid_))
else:
    class Town():
        fake_attr = True

if 'property' in db_config['tables']:
    table_def_ = db_config['tables']['property']
    class Property(GeoInterface,Base):
        __tablename__ = table_def_['tablename']
        __table_args__ = {'schema': table_def_['schema'], 'autoload': True}
        noobj = Column(table_def_['att_id'], Integer, primary_key=True)
        idemai = Column(table_def_['att_id_property'], String)
        nummai = Column(table_def_['att_property_number'], String)
        typimm = Column(table_def_['att_property_type'], String)
        source = Column(table_def_['att_property_source'], String)
        geom =GeometryColumn(Geometry(2, srid=srid_))
else:
    class Property():
        pass

if 'local_names' in db_config['tables']:
    table_def_ = db_config['tables']['local_names']
    class LocalName(GeoInterface,Base):
        __tablename__ = table_def_['tablename']
        __table_args__ = {'schema': table_def_['schema'], 'autoload': True}
        idcnlo = Column(table_def_['att_id'], String, primary_key=True)
        nomloc = Column(table_def_['att_local_name'], String)
        geom =GeometryColumn(Geometry(2, srid=srid_))
else:
    class LocalName():
        pass
    
# STOP models used for static extraction and general models

# START models used for GetFeature queries

# models for theme: allocation plan

class PrimaryLandUseZones(GeoInterface,Base):
    __table_args__ = {'schema': db_config['schema'], 'autoload': True}
    __tablename__ = 'r73_affectations_primaires'
    idobj = Column(Integer, primary_key=True)
    geom =GeometryColumn(Geometry(2,srid=srid_))

class SecondaryLandUseZones(GeoInterface,Base):
    __table_args__ = {'schema': db_config['schema'], 'autoload': True}
    __tablename__ = 'r73_zones_superposees'
    idobj = Column(Integer, primary_key=True)
    geom =GeometryColumn(Geometry(2,srid=srid_))

class ComplementaryLandUsePerimeters(GeoInterface,Base):
    __table_args__ = {'schema': db_config['schema'], 'autoload': True}
    __tablename__ = 'r73_perimetres_superposes'
    idobj = Column(Integer, primary_key=True)
    geom =GeometryColumn(Geometry(2,srid=srid_))

class LandUseLinearConstraints(GeoInterface,Base):
    __tablename__ = 'r73_contenus_lineaires'
    __table_args__ = {'schema': db_config['schema'], 'autoload': True}
    idobj = Column(Integer, primary_key=True)
    geom =GeometryColumn(Geometry(2,srid=srid_))

class LandUsePointConstraints(GeoInterface,Base):
    __tablename__ = 'r73_contenus_ponctuels'
    __table_args__ = {'schema': db_config['schema'], 'autoload': True}
    idobj = Column(Integer, primary_key=True)
    geom =GeometryColumn(Geometry(2,srid=srid_))

# models for the topic national roads

# None yet

# models for the national railways

# None yet

# models for airports

class CHAirportSecurityZones(GeoInterface,Base):
    __tablename__ = 'r108_bazl_sicherheitszonenplan'
    __table_args__ = {'schema': db_config['schema'], 'autoload': True}
    idobj = Column(Integer, primary_key=True)
    geom = GeometryColumn(Geometry(2,srid=srid_))

class CHAirportSecurityZonesPDF(GeoInterface,Base):
    __tablename__ = 'r108_bazl_sicherheitszonenplan_pdf'
    __table_args__ = {'schema': db_config['schema'], 'autoload': True}
    idobj = Column(Integer, primary_key=True)
    geom = GeometryColumn(Geometry(2,srid=srid_))
    # ch.bazl.sicherheitszonenplan.oereb

GeometryDDL(CHAirportSecurityZonesPDF.__table__)

class CHAirportProjectZones(GeoInterface,Base):
    __tablename__ = 'r103_bazl_projektierungszonen_flughafenanlagen'
    __table_args__ = {'schema': db_config['schema'], 'autoload': True}
    idobj = Column(Integer, primary_key=True)
    geom = GeometryColumn(Geometry(2,srid=srid_))
    
class CHAirportProjectZonesPDF(GeoInterface,Base):
    __tablename__ = 'r103_bazl_projektierungszonen_flughafenanlagen_pdf'
    __table_args__ = {'schema': db_config['schema'], 'autoload': True}
    idobj = Column(Integer, primary_key=True)
    geom = GeometryColumn(Geometry(2,srid=srid_))
    # ch.bazl.projektierungszonen-flughafenanlagen.oereb

GeometryDDL(CHAirportProjectZonesPDF.__table__)

#~ class Corridors(GeoInterface,Base):
    #~ __tablename__ = 'clo_couloirs'
    #~ __table_args__ = {'schema': 'amenagement', 'autoload': True}
    #~ idobj = Column(Integer, primary_key=True)
    #~ geom =GeometryColumn(Geometry(2,srid=srid_))
    
#~ class AltitudeRatings(GeoInterface,Base):
    #~ __tablename__ = 'clo_cotes_altitude_surfaces'
    #~ __table_args__ = {'schema': 'amenagement', 'autoload': True}
    #~ idobj = Column(Integer, primary_key=True)
    #~ geom =GeometryColumn(Geometry(2,srid=srid_))

# models for theme: register of polluted sites

class PollutedSites(GeoInterface,Base):
    __tablename__ = 'r116_sites_pollues'
    __table_args__ = {'schema': db_config['schema'], 'autoload': True}
    idobj = Column(Integer, primary_key=True)
    geom =GeometryColumn(Geometry(2,srid=srid_))
    
class CHPollutedSitesPublicTransports(GeoInterface,Base):
    __tablename__ = 'r119_bav_belastete_standorte_oev'
    __table_args__ = {'schema': db_config['schema'], 'autoload': True}
    idobj = Column(Integer, primary_key=True)
    geom =GeometryColumn(Geometry(2,srid=srid_))

class CHPollutedSitesPublicTransportsPDF(GeoInterface,Base):
    __tablename__ = 'r119_bav_belastete_standorte_oev_pdf'
    __table_args__ = {'schema': db_config['schema'], 'autoload': True}
    idobj = Column(Integer, primary_key=True)
    geom =GeometryColumn(Geometry(2,srid=srid_))

GeometryDDL(CHPollutedSitesPublicTransportsPDF.__table__)
# ch.bav.kataster-belasteter-standorte-oev.oereb

# models for the topic noise

class RoadNoise(GeoInterface,Base):
    __tablename__ = 'r145_sens_bruit'
    __table_args__ = {'schema': db_config['schema'], 'autoload': True}
    idobj = Column(Integer, primary_key=True)
    geom =GeometryColumn(Geometry(2,srid=srid_))

# models for water protection

class Zoneprotection(GeoInterface,Base):
    __tablename__ = 'r131_zone_prot_eau'
    __table_args__ = {'schema': db_config['schema'], 'autoload': True}
    idobj = Column(String(40), primary_key=True)
    geom = GeometryColumn(Geometry(srid=srid_))
    
class WaterProtectionPerimeters(GeoInterface,Base):
    __tablename__ = 'r132_perimetre_prot_eau'
    __table_args__ = {'schema': db_config['schema'], 'autoload': True}
    idobj = Column(String(40), primary_key=True)
    geom = GeometryColumn(Geometry(srid=srid_))

# models for the topic Forest
class ForestLimits(GeoInterface,Base):
    __tablename__ = 'r157_lim_foret'
    __table_args__ = {'schema': db_config['schema'], 'autoload': True}
    idobj = Column(Integer, primary_key=True)
    geom =GeometryColumn(Geometry(2,srid=srid_))
    
class ForestDistances(GeoInterface,Base):
    __tablename__ = 'r159_dist_foret'
    __table_args__ = {'schema': db_config['schema'], 'autoload': True}
    idobj = Column(Integer, primary_key=True)
    geom =GeometryColumn(Geometry(2,srid=srid_))

# STOP models used for GetFeature queries