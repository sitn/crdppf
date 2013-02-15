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

class Topics(Base):
    __tablename__ = 'topics'
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