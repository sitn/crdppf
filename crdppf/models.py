from sqlalchemy import (
    Column, 
    Sequence, 
    Integer, 
    Text,
    String, 
    Boolean, 
    ForeignKey, 
    Float
    )
    
from sqlalchemy.orm import relationship, backref

from zope.sqlalchemy import ZopeTransactionExtension

import sqlahelper

DBSession = sqlahelper.get_session()

from papyrus.geo_interface import GeoInterface
from geoalchemy import (
    GeometryColumn, 
    Geometry, 
    Polygon
    )

Base = sqlahelper.get_base()

# START models used for static extraction and general models

class Topics(Base):
    __tablename__ = 'topic'
    __table_args__ = {'schema': 'crdppf', 'autoload': True}
    
class Authority(Base):
    __tablename__ = 'authority'
    __table_args__ = {'schema': 'crdppf', 'autoload': True}
    
class Cadastre(Base):
    __tablename__ = 'la02_cadastres'
    __table_args__ = {'schema': 'general', 'autoload': True}
    idobj = Column(Integer, primary_key=True)
    geom =GeometryColumn(Geometry(2,srid=21781))

class ImmeublesCanton(Base):
    __tablename__ = 'immeubles_canton'
    __table_args__ = {'schema': 'public', 'autoload': True}
    noobj = Column(Integer, primary_key=True)
    geom =GeometryColumn(Geometry(2,srid=21781))

class NomLocalLieuDit(Base):
    __tablename__ = 'nom_local_lieu_dit'
    __table_args__ = {'schema': 'public', 'autoload': True}
    idcnlo = Column(String(30), primary_key=True)
    geom =GeometryColumn(Geometry(2,srid=21781))
    
class Zoneprotection(Base):
    __tablename__ = 'en01_zone_sect_protection_eaux'
    __table_args__ = {'schema': 'environnement', 'autoload': True}
    idobj = Column(String(40), primary_key=True)
    geom = GeometryColumn(Geometry(srid=21781))
    
# STOP models used for static extraction and general models

# START models used for GetFeature queries
    
# models for theme: pedestrian ways

class PedestrianWays(Base):
    __tablename__ = 'at39_itineraires_pedestres'
    __table_args__ = {'schema': 'amenagement', 'autoload': True}
    idobj = Column(Integer, primary_key=True)
    geom =GeometryColumn(Geometry(2,srid=21781))

# models for theme: allocation plan

class CommunalArea(Base):
    __tablename__ = 'at14_zones_communales'
    __table_args__ = {'schema': 'amenagement', 'autoload': True}
    idobj = Column(Integer, primary_key=True)
    geom =GeometryColumn(Geometry(2,srid=21781))
    
class StateArea(Base):
    __tablename__ = 'at08_zones_cantonales'
    __table_args__ = {'schema': 'amenagement', 'autoload': True}
    idobj = Column(Integer, primary_key=True)
    geom =GeometryColumn(Geometry(2,srid=21781))

# models for obstacles to navigation

class Corridors(Base):
    __tablename__ = 'clo_couloirs'
    __table_args__ = {'schema': 'amenagement', 'autoload': True}
    idobj = Column(Integer, primary_key=True)
    geom =GeometryColumn(Geometry(2,srid=21781))
    
class AltitudeRatings(Base):
    __tablename__ = 'clo_cotes_altitude_surfaces'
    __table_args__ = {'schema': 'amenagement', 'autoload': True}
    idobj = Column(Integer, primary_key=True)
    geom =GeometryColumn(Geometry(2,srid=21781))

# models for theme: register of polluted sites

class PollutedSitesAccidents(Base):
    __tablename__ = 'en07_canepo_accidents'
    __table_args__ = {'schema': 'environnement', 'autoload': True}
    idobj = Column(Integer, primary_key=True)
    geom =GeometryColumn(Geometry(2,srid=21781))
    
class PollutedSitesLandDumps(Base):
    __tablename__ = 'en07_canepo_decharges'
    __table_args__ = {'schema': 'environnement', 'autoload': True}
    idobj = Column(Integer, primary_key=True)
    geom =GeometryColumn(Geometry(2,srid=21781))
    
class PollutedSitesLandDumpsPts(Base):
    __tablename__ = 'en07_canepo_decharges_points'
    __table_args__ = {'schema': 'environnement', 'autoload': True}
    idobj = Column(Integer, primary_key=True)
    geom =GeometryColumn(Geometry(2,srid=21781))
    
class PollutedSitesLandDumpsPoly(Base):
    __tablename__ = 'en07_canepo_decharges_polygones'
    __table_args__ = {'schema': 'environnement', 'autoload': True}
    idobj = Column(Integer, primary_key=True)
    geom =GeometryColumn(Geometry(2,srid=21781))

class PollutedSitesCompanies(Base):
    __tablename__ = 'en07_canepo_entreprises'
    __table_args__ = {'schema': 'environnement', 'autoload': True}
    idobj = Column(Integer, primary_key=True)
    geom =GeometryColumn(Geometry(2,srid=21781))
    
class PollutedSitesCompaniesPts(Base):
    __tablename__ = 'en07_canepo_entreprises_points'
    __table_args__ = {'schema': 'environnement', 'autoload': True}
    idobj = Column(Integer, primary_key=True)
    geom =GeometryColumn(Geometry(2,srid=21781))
    
class PollutedSitesCompaniesPoly(Base):
    __tablename__ = 'en07_canepo_entreprises_polygones'
    __table_args__ = {'schema': 'environnement', 'autoload': True}
    idobj = Column(Integer, primary_key=True)
    geom =GeometryColumn(Geometry(2,srid=21781))
    
# STOP models used for GetFeature queries