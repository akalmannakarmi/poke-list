from fastapi.templating import Jinja2Templates
from ..database import get_session
from ..schemas import PokemonRead
from .. import crud
from . import router

templates = Jinja2Templates(directory="templates/v2")

@router.get("/pokemons", response_model=list[PokemonRead])
async def read_pokemons(
	type: str|None = None,
	name: str|None = None,
	limit: int = 20,
	offset: int = 0
	):
	print(type,name)

	async with get_session() as session:
		pokemons = await crud.get_pokemons_filtered(session,type,name,limit,offset)
	return templates.TemplateResponse()