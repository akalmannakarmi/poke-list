from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_session
from ..schemas import PokemonRead
from .. import crud
from . import router

@router.get("/pokemons", response_model=list[PokemonRead])
async def read_pokemons(
	session: AsyncSession = Depends(get_session),
	type: str|None = None,
	name: str|None = None
	):
	print(type,name)

	return await crud.get_pokemons_filtered(session,type,name)