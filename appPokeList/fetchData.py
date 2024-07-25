import aiohttp
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from . import crud,database,schemas,models
from sqlalchemy import select, func

fullyUpdated = False

async def get_pokemons_count(db: AsyncSession) -> int:
    query = select(func.count(models.Pokemon.id))
    result = await db.execute(query)
    return result.scalar_one()

async def fetch_pokemon(session, url):
	async with session.get(url) as response:
		return await response.json()

async def allAdded() -> bool:
    async with aiohttp.ClientSession() as session:
        async with session.get("https://pokeapi.co/api/v2/pokemon?limit=1") as response:
            data = await response.json()
            external_count = data["count"]

    async with database.get_session() as db:
        internal_count = await get_pokemons_count(db)
        
    return external_count == internal_count


async def fetch_all_pokemon():
	global fullyUpdated
	pokemon_list={"next":"https://pokeapi.co/api/v2/pokemon?limit=10"}

	if fullyUpdated:
		return
	if await allAdded():
		fullyUpdated=True
		return

	while pokemon_list["next"]:
		async with aiohttp.ClientSession() as session:
			async with session.get(pokemon_list["next"]) as response:
				pokemon_list = await response.json()
			print("Got List")
			
			async with database.get_session() as db:
				for pokemon in pokemon_list["results"]:
					pokemon_details = await fetch_pokemon(session,pokemon["url"])
					
					pokemon = schemas.PokemonCreate(
						name=pokemon_details["name"],
						types = [schemas.TypeCreate(name=type_info['type']['name']) for type_info in pokemon_details['types']],
						url = pokemon_details["sprites"]["other"]["home"]["front_default"] if pokemon_details["sprites"]["other"]["home"]["front_default"] else pokemon_details["sprites"]["front_default"]
					)
					print(f"Id:{pokemon_details['id']}, Name: {pokemon.name}, Types: {pokemon.types}, URL: {pokemon.url}")
					await crud.create_pokemon(db,pokemon)
	fullyUpdated = True


if __name__ == "__main__":
	asyncio.run(fetch_all_pokemon())
