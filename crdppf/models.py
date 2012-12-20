from sqlalchemy import (
    Column,
    Integer,
    Text,
    )

from zope.sqlalchemy import ZopeTransactionExtension

import sqlahelper

Base = sqlahelper.get_base()
DBSession = sqlahelper.get_session()

from papyrus.geo_interface import GeoInterface
from geoalchemy import GeometryColumn, Geometry, Polygon, GeometryDDL

class Prod(Base):
    __tablename__ = 'product'
    __table_args__ = {'schema': 'public', 'autoload': True}
    id_product = Column('id_product', Integer, primary_key=True)

class Commune(GeoInterface, Base):
    __tablename__ = 'communes'
    __table_args__ = {'schema': 'public', 'autoload': True}
    numcom = Column('numcom', Integer, primary_key=True)
    geom = GeometryColumn(Geometry(srid=21781))

