from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles

from auth.jwt_bearer import JWTBearer
from config.config import initiate_database
from routes.surrounding import router as SurroundingRouter

import gradio_client

app = FastAPI()

token_listener = JWTBearer()


@app.on_event("startup")
async def start_database():
    await initiate_database()


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app."}

app.state.moondream = gradio_client.Client("https://vikhyatk-moondream1.hf.space/--replicas/plmds/")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
app.include_router(SurroundingRouter, tags=["Surroundings"])
