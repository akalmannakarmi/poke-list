from typing import Optional
from fastapi import Query
from ..database import get_session
from ..schemas import PokemonRead
from .. import crud
from . import router

@router.get("/pokemons", response_model=list[PokemonRead])
async def read_pokemons(
    name: Optional[str] = Query(None, description="Filter by name"),
    type: Optional[str] = Query(None, description="Filter by type"),
	limit: int = Query(20, description="Max No of Items"),
	offset: int = Query(0, description="Skip No of Items")
	):
	if offset<0:
		offset=0
	async with get_session() as session:
		return await crud.get_pokemons_filtered(session,type,name,limit,offset)