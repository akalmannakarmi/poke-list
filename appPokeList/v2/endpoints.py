from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from ..database import get_session
from ..schemas import PokemonCreate, PokemonRead
from .. import crud
from . import router

@router.post("/pokemons", response_model=PokemonRead)
async def create_pokemon(pokemon: PokemonCreate, session: AsyncSession = Depends(get_session)):
    return await crud.create_pokemon(session, pokemon)

@router.get("/pokemons", response_model=List[PokemonRead])
async def read_pokemons(session: AsyncSession = Depends(get_session)):
    return await crud.get_pokemons(session)

@router.get("/pokemons/{pokemon_id}", response_model=PokemonRead)
async def read_pokemon(pokemon_id: int, session: AsyncSession = Depends(get_session)):
    pokemon = await crud.get_pokemon(session, pokemon_id)
    if not pokemon:
        raise HTTPException(status_code=404, detail="Pokemon not found")
    return pokemon
