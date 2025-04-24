import asyncio
import json
from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.api import deps
from app.models import Goal
from app.schemas import AddGoalRequestSchema, GoalsResponseSchema
from app.bot import start_goal

router = APIRouter()


@router.post("/add-goal")
async def add_goal(
    body: AddGoalRequestSchema,
    db_session: AsyncSession = Depends(deps.get_db_session),
):
    goal = Goal(
        title=body.title,
        description=body.description,
        user_id=body.user_id,
    )

    db_session.add(goal)
    await db_session.commit()

    asyncio.create_task(start_goal(goal.id, body.user_id))
    return {"status": "success", "goal_id": goal.id}


@router.get("/goals")
async def get_goals(
    db_session: AsyncSession = Depends(deps.get_db_session),
    user_id: str = Query(),
) -> GoalsResponseSchema:
    goals = list(
        await db_session.scalars(
            select(Goal)
            .options(
                selectinload(Goal.results),
            )
            .where(Goal.user_id == user_id)
        )
    )

    return GoalsResponseSchema(
        goals=[
            {
                "id": goal.id,
                "title": goal.title,
                "description": goal.description,
                "conversation_history": json.loads(goal.conversation_history or "[]"),
            }
            for goal in goals
        ]
    )
