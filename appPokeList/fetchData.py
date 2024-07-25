import aiohttp
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from . import crud,database,schemas,models
from sqlalchemy import select, func
from tqdm.asyncio import tqdm

fullyUpdated = False
API_URL = "https://pokeapi.co/api/v2/pokemon"

async def get_pokemons_count(db: AsyncSession) -> int:
	query = select(func.count(models.Pokemon.id))
	result = await db.execute(query)
	return result.scalar_one()

async def fetch_pokemon(session, url):
	async with session.get(url) as response:
		return await response.json()

async def allAdded(external_count) -> bool:
	async with database.get_session() as db:
		internal_count = await get_pokemons_count(db)
		
	return external_count == internal_count

async def getCount() -> int:
	async with aiohttp.ClientSession() as session:
		async with session.get(API_URL+"?limit=1") as response:
			data = await response.json()
			return data["count"]

async def fetch_all_pokemon():
	global fullyUpdated
	pokemon_list={"next":API_URL+"?limit=100&offset=0"}

	if fullyUpdated:
		return
	count = await getCount()
	if await allAdded(count):
		fullyUpdated=True
		return
	
	with tqdm(total=count, desc="Processing Pokémon", unit="pokemon") as pbar:
		while pokemon_list["next"]:
			async with aiohttp.ClientSession() as session:
				async with session.get(pokemon_list["next"]) as response:
					pokemon_list = await response.json()
				
				async with database.get_session() as db:
					for pokemon in pokemon_list["results"]:
						pokemon_details = await fetch_pokemon(session,pokemon["url"])
						pokemon = schemas.PokemonCreate(
							name=pokemon_details["name"],
							types = [schemas.TypeCreate(name=type_info['type']['name']) for type_info in pokemon_details['types']],
							url = pokemon_details["sprites"]["other"]["home"]["front_default"] if pokemon_details["sprites"]["other"]["home"]["front_default"] else pokemon_details["sprites"]["front_default"]
						)
						pbar.update(1)
						await crud.create_pokemon(db,pokemon)
	fullyUpdated = True


if __name__ == "__main__":
	asyncio.run(fetch_all_pokemon())
