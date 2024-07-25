from fastapi import HTTPException
from typing import List
from ..database import get_session
from ..schemas import PokemonCreate, PokemonRead
from .. import crud
from . import router

@router.post("/pokemons", response_model=PokemonRead)
async def create_pokemon(pokemon: PokemonCreate):
	async with get_session() as session:
   		return await crud.create_pokemon(session, pokemon)

@router.get("/pokemons", response_model=List[PokemonRead])
async def read_pokemons():
	async with get_session() as session:
		return await crud.get_pokemons(session)

@router.get("/pokemons/{pokemon_id}", response_model=PokemonRead)
async def read_pokemon(pokemon_id: int):
	async with get_session() as session:
		pokemon = await crud.get_pokemon(session, pokemon_id)
	if not pokemon:
		raise HTTPException(status_code=404, detail="Pokemon not found")
	return pokemon