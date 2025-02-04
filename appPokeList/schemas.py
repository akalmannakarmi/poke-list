from pydantic import BaseModel

class TypeBase(BaseModel):
    name: str

class TypeCreate(TypeBase):
    pass

class TypeRead(TypeBase):
    id: int

    class Config:
        from_attributes = True

class PokemonBase(BaseModel):
    name: str
    url: str|None

class PokemonCreate(PokemonBase):
    types: list[TypeCreate]

class PokemonRead(PokemonBase):
    id: int
    types: list[TypeRead]

    class Config:
        from_attributes = True
