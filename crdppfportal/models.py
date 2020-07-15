# -*- coding: utf-8 -*-

from sqlalchemy import(
    Column,
    Integer,
    String,
    ForeignKey)

from sqlalchemy.orm import relationship, backref

from papyrus.geo_interface import GeoInterface

from geoalchemy2 import Geometry

from crdppf import db_config
srid_ = db_config['srid']

from crdppf.models import Base

# Specific model definition here
class Users(Base):
    __tablename__ = 'users'
    __table_args__ = {'schema': db_config['schema'], 'autoload': True}

if 'road_building_lines' in db_config['restrictions']:
    class RoadBuildingLines(GeoInterface, Base):
        __tablename__ = 'r078ne_alignements'
        __table_args__ = {'schema': db_config['schema'], 'autoload': True}
        idobj = Column(Integer, primary_key=True)
        geom = Column(Geometry("MULTILINE", srid=srid_))
else:
    class RoadBuildingLines():
        pass
