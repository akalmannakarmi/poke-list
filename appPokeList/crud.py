from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from .models import Pokemon, Type
from .schemas import PokemonCreate, TypeCreate

async def create_pokemon(db: AsyncSession, pokemon: PokemonCreate):
    db_types = []
    for type_data in pokemon.types:
        db_type = await db.execute(select(Type).where(Type.name == type_data.name))
        db_type = db_type.scalars().first()
        if not db_type:
            db_type = Type(name=type_data.name)
            db.add(db_type)
            await db.flush()
        db_types.append(db_type)

    new_pokemon = Pokemon(name=pokemon.name, types=db_types)
    db.add(new_pokemon)
    await db.commit()
    await db.refresh(new_pokemon)
    return new_pokemon

async def get_pokemons(db: AsyncSession):
    result = await db.execute(select(Pokemon).options(selectinload(Pokemon.types)))
    return result.scalars().all()

async def get_pokemon(db: AsyncSession, pokemon_id: int):
    result = await db.execute(select(Pokemon).where(Pokemon.id == pokemon_id).options(selectinload(Pokemon.types)))
    return result.scalars().first()
