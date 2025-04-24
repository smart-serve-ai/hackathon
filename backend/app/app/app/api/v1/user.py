import os

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from telethon import TelegramClient

from app.api import deps
from app.models import User
from app.schemas import SendOTPRequestSchema, VerifyOTPRequestSchema
from app.settings import settings

router = APIRouter()
os.makedirs("/tmp/tg-sessions", exist_ok=True)


@router.post("/send-otp")
async def send_otp(body: SendOTPRequestSchema):
    client = TelegramClient(
        f"/tmp/tg-sessions/{body.phone.replace('+', '')}",
        settings.tg_api_id,
        settings.tg_api_hash,
    )

    await client.connect()

    if not await client.is_user_authorized():
        phone_code_hash = await client.send_code_request(str(body.phone))

        return {
            "status": "success",
            "message": "Code sent successfully",
            "phone_code_hash": phone_code_hash.phone_code_hash,
        }

    await client.disconnect()
    return {"status": "already_authorized"}


@router.post("/verify-otp")
async def verify_otp(
    body: VerifyOTPRequestSchema,
    db_session: AsyncSession = Depends(deps.get_db_session),
):
    client = TelegramClient(
        f"/tmp/tg-sessions/{body.phone.replace('+', '')}",
        settings.tg_api_id,
        settings.tg_api_hash,
    )

    await client.connect()

    try:
        await client.sign_in(phone=body.phone, code=body.code, phone_code_hash=body.phone_code_hash)

        user = (await db_session.execute(select(User).where(User.phone == body.phone))).scalar_one_or_none()

        if not user:
            user = User(
                phone=body.phone,
            )

            db_session.add(user)
            await db_session.commit()

        return {"status": "success", "message": "Successfully authenticated", "user_id": user.id}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    finally:
        await client.disconnect()
