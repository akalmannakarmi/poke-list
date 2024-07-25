from typing import Optional
from fastapi.templating import Jinja2Templates
from fastapi import Request,Query
from ..database import get_session
from ..schemas import PokemonRead
from .. import crud
from . import router

templates = Jinja2Templates(directory="templates/v2")

@router.get("/pokemons", response_model=list[PokemonRead])
async def read_pokemons(
	request: Request,
    name: Optional[str] = Query(None, description="Filter by name"),
    type: Optional[str] = Query(None, description="Filter by type"),
	limit: int = Query(20, description="Max No of Items"),
	offset: int = Query(0, description="Skip No of Items")
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
	return templates.TemplateResponse("pokemons.html",{"request": request, "pokemons":pokemons_list,"type":type or '',"name":name or '',"limit":limit,"offset":offset },)