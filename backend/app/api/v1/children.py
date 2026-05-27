import uuid

from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from app.api.deps import CurrentParent, DbSession
from app.api.schemas.child import ChildCreate, ChildResponse, ChildUpdate
from app.models.child import Child

router = APIRouter()


@router.get("", response_model=list[ChildResponse])
async def list_children(parent: CurrentParent, db: DbSession):
    result = await db.execute(select(Child).where(Child.parent_id == parent.id))
    return result.scalars().all()


@router.post("", response_model=ChildResponse, status_code=201)
async def create_child(req: ChildCreate, parent: CurrentParent, db: DbSession):
    child = Child(parent_id=parent.id, **req.model_dump())
    db.add(child)
    await db.commit()
    await db.refresh(child)
    return child


@router.put("/{child_id}", response_model=ChildResponse)
async def update_child(child_id: uuid.UUID, req: ChildUpdate, parent: CurrentParent, db: DbSession):
    child = await db.get(Child, child_id)
    if not child or child.parent_id != parent.id:
        raise HTTPException(status_code=404, detail="Child not found")
    for key, value in req.model_dump(exclude_unset=True).items():
        setattr(child, key, value)
    await db.commit()
    await db.refresh(child)
    return child
