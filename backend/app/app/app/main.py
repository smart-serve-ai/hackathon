from fastapi import FastAPI

from app.api.v1 import api_router as v1_api_router


app = FastAPI(title="SmartServe Backend API", debug=True)


@app.get("/ping", tags=["General"])
async def ping():
    return {"message": "pong"}


app.include_router(v1_api_router, prefix="/v1", tags=["v1"])
