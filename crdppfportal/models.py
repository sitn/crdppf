# -*- coding: utf-8 -*-

from sqlalchemy import(
    Column, 
    Sequence, 
    Integer, 
    Text,
    String,
    Float)
    
from sqlalchemy.orm import relationship, backref, deferred
from zope.sqlalchemy import ZopeTransactionExtension
import sqlahelper

from crdppf import db_config

Base = sqlahelper.get_base()

# Specific model definition here
