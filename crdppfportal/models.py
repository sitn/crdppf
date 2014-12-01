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

# Specific model definition
class Paper(Base):
    __tablename__ = 'paperformats'
    __table_args__ = {'schema': db_config['schema'], 'autoload': True}
 