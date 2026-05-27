import uuid

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy import select

from app.api.deps import CurrentParent, DbSession
from app.models.learning_goal import LearningGoal

router = APIRouter()


class GoalCreate(BaseModel):
    child_id: uuid.UUID
    goal_type: str
    target: str
    priority: int = 5


class GoalUpdate(BaseModel):
    target: str | None = None
    priority: int | None = None
    status: str | None = None


@router.get("")
async def list_goals(parent: CurrentParent, db: DbSession, child_id: uuid.UUID | None = None):
    query = select(LearningGoal)
    if child_id:
        query = query.where(LearningGoal.child_id == child_id)
    result = await db.execute(query)
    return result.scalars().all()


@router.post("", status_code=201)
async def create_goal(req: GoalCreate, parent: CurrentParent, db: DbSession):
    goal = LearningGoal(**req.model_dump())
    db.add(goal)
    await db.commit()
    await db.refresh(goal)
    return goal


@router.put("/{goal_id}")
async def update_goal(goal_id: uuid.UUID, req: GoalUpdate, parent: CurrentParent, db: DbSession):
    goal = await db.get(LearningGoal, goal_id)
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    for key, value in req.model_dump(exclude_unset=True).items():
        setattr(goal, key, value)
    await db.commit()
    await db.refresh(goal)
    return goal


@router.delete("/{goal_id}", status_code=204)
async def delete_goal(goal_id: uuid.UUID, parent: CurrentParent, db: DbSession):
    goal = await db.get(LearningGoal, goal_id)
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    await db.delete(goal)
    await db.commit()
