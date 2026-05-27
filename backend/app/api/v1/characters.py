import uuid

from fastapi import APIRouter, HTTPException
from sqlalchemy import or_, select

from app.api.deps import CurrentParent, DbSession
from app.api.schemas.character import CharacterCreate, CharacterResponse, CharacterUpdate
from app.models.character import Character

router = APIRouter()


@router.get("", response_model=list[CharacterResponse])
async def list_characters(parent: CurrentParent, db: DbSession):
    result = await db.execute(
        select(Character).where(
            or_(Character.parent_id == parent.id, Character.parent_id.is_(None))
        )
    )
    return result.scalars().all()


@router.post("", response_model=CharacterResponse, status_code=201)
async def create_character(req: CharacterCreate, parent: CurrentParent, db: DbSession):
    character = Character(parent_id=parent.id, **req.model_dump())
    db.add(character)
    await db.commit()
    await db.refresh(character)
    return character


@router.put("/{character_id}", response_model=CharacterResponse)
async def update_character(
    character_id: uuid.UUID, req: CharacterUpdate, parent: CurrentParent, db: DbSession
):
    character = await db.get(Character, character_id)
    if not character or (character.parent_id and character.parent_id != parent.id):
        raise HTTPException(status_code=404, detail="Character not found")
    for key, value in req.model_dump(exclude_unset=True).items():
        setattr(character, key, value)
    await db.commit()
    await db.refresh(character)
    return character


@router.delete("/{character_id}", status_code=204)
async def delete_character(character_id: uuid.UUID, parent: CurrentParent, db: DbSession):
    character = await db.get(Character, character_id)
    if not character or character.parent_id != parent.id:
        raise HTTPException(status_code=404, detail="Character not found")
    await db.delete(character)
    await db.commit()
