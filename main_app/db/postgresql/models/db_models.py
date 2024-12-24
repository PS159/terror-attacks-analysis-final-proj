from sqlalchemy import Column, Integer, String, Float, ForeignKey, DATE, Boolean
from sqlalchemy.orm import relationship
from .base_model import Base


class AttackType(Base):
    __tablename__ = 'attack_types'
    id = Column(Integer, primary_key=True, autoincrement=False)
    attack_type = Column(String, nullable=False)
    count = Column(Integer)

    terror_attack = relationship('TerrorAttack', backref='attack_types')


class Region(Base):
    __tablename__ = 'regions'
    id = Column(Integer, primary_key=True, autoincrement=False)
    region = Column(String, nullable=False)
    count = Column(Integer)

    countries = relationship('Country', backref='regions')


class Country(Base):
    __tablename__ = 'countries'
    id = Column(Integer, primary_key=True, autoincrement=False)
    name = Column(String, nullable=False)
    count = Column(Integer)

    region_id = Column(Integer, ForeignKey('regions.id'))
    terror_attacks = relationship('TerrorAttack', backref='countries')


class TargetType(Base):
    __tablename__ = 'target_types'
    id = Column(Integer, primary_key=True, autoincrement=False)
    target_type = Column(String, nullable=False)
    count = Column(Integer)

    terror_attacks = relationship('TerrorAttack', backref='target_types')


class TerrorOrg(Base):
    __tablename__ = 'terror_organizations'
    id = Column(Integer, primary_key=True, autoincrement=False)
    name = Column(String, nullable=False)
    count = Column(Integer)

    terror_attacks = relationship('TerrorAttack', backref='terror_organizations')


class TerrorAttack(Base):
    __tablename__ = 'terror_attacks'
    id = Column(Integer, primary_key=True, autoincrement=False)
    date = Column(DATE)
    lat = Column(Float)
    lon = Column(Float)
    killed = Column(Float)
    injured = Column(Float)
    successful = Column(Boolean)
    description = Column(String)

    attack_type_id = Column(Integer, ForeignKey('attack_types.id'))
    country_id = Column(Integer, ForeignKey('countries.id'))
    terror_organization_id = Column(Integer, ForeignKey('terror_organizations.id'))
    target_type_id = Column(Integer, ForeignKey('target_types.id'))




