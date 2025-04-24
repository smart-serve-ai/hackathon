from pydantic import BaseModel


class BaseModelORM(BaseModel):
    class Config:
        from_attributes = True


class SendOTPRequestSchema(BaseModel):
    phone: str


class VerifyOTPRequestSchema(BaseModel):
    phone: str
    phone_code_hash: str
    code: str


class AddGoalRequestSchema(BaseModel):
    title: str
    description: str
    user_id: str


class ResultSchema(BaseModelORM):
    details: dict


class GoalSchema(BaseModelORM):
    id: str
    title: str
    description: str
    conversation_history: list[dict]


class GoalsResponseSchema(BaseModel):
    goals: list[GoalSchema]
