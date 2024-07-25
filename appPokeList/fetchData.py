import aiohttp
import asyncio

async def fetch_pokemon(session, url):
	async with session.get(url) as response:
		return await response.json()

async def fetch_all_pokemon():
	pokemon_list={"next":"https://pokeapi.co/api/v2/pokemon?limit=100"}
	while pokemon_list["next"]:
		async with aiohttp.ClientSession() as session:
			async with session.get(pokemon_list["next"]) as response:
				pokemon_list = await response.json()
			print("Got List")
			print(pokemon_list)
			
			for pokemon in pokemon_list["results"]:
				pokemon_details = await fetch_pokemon(session,pokemon["url"])
				id = pokemon_details["id"]
				name = pokemon_details["name"]
				types = [type_info['type']['name'] for type_info in pokemon_details['types']]
				print(f"Id: {id} ,Name: {name}, Types: {', '.join(types)}")


if __name__ == "__main__":
	asyncio.run(fetch_all_pokemon())
