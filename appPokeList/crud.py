from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from .models import Pokemon, Type , pokemon_type_association
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


async def get_pokemons_filtered(db: AsyncSession, type: str | None = None, name: str | None = None):
    query = select(Pokemon).options(selectinload(Pokemon.types))

    if name:
        query = query.where(Pokemon.name == name)
    
    if type:
        # Create a subquery to filter Pokemons by their types
        subquery = (
            select(Pokemon.id)
            .join(pokemon_type_association)
            .join(Type)
            .where(Type.name == type)
        ).subquery()
        
        query = query.where(Pokemon.id.in_(subquery))

    result = await db.execute(query)
    return result.scalars().all()
