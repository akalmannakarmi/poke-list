from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship
from .database import Base

# Association table
pokemon_type_association = Table(
    'pokemon_type_association',
    Base.metadata,
    Column('pokemon_id', Integer, ForeignKey('pokemons.id'), primary_key=True),
    Column('type_id', Integer, ForeignKey('types.id'), primary_key=True)
)

class Pokemon(Base):
    __tablename__ = "pokemons"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)

    types = relationship("Type", secondary=pokemon_type_association, back_populates="pokemons")

class Type(Base):
    __tablename__ = "types"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)

    pokemons = relationship("Pokemon", secondary=pokemon_type_association, back_populates="types")
