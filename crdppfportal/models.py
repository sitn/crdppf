# -*- coding: utf-8 -*-

from sqlalchemy import(
    Column, 
    Sequence, 
    Integer, 
    Text,
    String,
    Float)
    
from crdppf import db_config

from crdppf.models import Base

# Specific model definition here
class Users(Base):
    __tablename__ = 'users'
    __table_args__ = {'schema': db_config['schema'], 'autoload': True}
