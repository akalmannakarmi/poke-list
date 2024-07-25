from ..database import get_session
from ..schemas import PokemonRead
from .. import crud
from . import router

@router.get("/pokemons", response_model=list[PokemonRead])
async def read_pokemons(
	type: str|None = None,
	name: str|None = None,
	limit: int = 20,
	offset: int = 0
	):
	if offset<0:
		offset=0
	async with get_session() as session:
		return await crud.get_pokemons_filtered(session,type,name,limit,offset)