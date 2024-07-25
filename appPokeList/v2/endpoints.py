from fastapi.templating import Jinja2Templates
from fastapi import Request
from ..database import get_session
from ..schemas import PokemonRead
from .. import crud
from . import router

templates = Jinja2Templates(directory="templates/v2")

@router.get("/pokemons", response_model=list[PokemonRead])
async def read_pokemons(
	request: Request,
	type: str|None = None,
	name: str|None = None,
	limit: int = 20,
	offset: int = 0
	):
	if offset<0:
		offset=0
	async with get_session() as session:
		pokemons = await crud.get_pokemons_filtered(session,type,name,limit,offset)
	pokemons_list = []
	for pokemon in pokemons:
		pokemons_list.append({
			"id":pokemon.id,
			"name":pokemon.name,
			"types":[type.name for type in pokemon.types],
			"url":pokemon.url
		})
	return templates.TemplateResponse("pokemons.html",{"request": request, "pokemons":pokemons_list,"type":type,"name":name,"limit":limit,"offset":offset },)