from fastapi import Body, APIRouter, HTTPException, UploadFile, File, Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from passlib.context import CryptContext

import os
import uuid
import shutil

from auth.jwt_handler import sign_jwt
from config.config import Settings

router = APIRouter()
settings = Settings()

hash_helper = CryptContext(schemes=["bcrypt"])


@router.post("/surrounding")
async def surroundings(request: Request, image: UploadFile = File(...), question: str = "Describe my surroundings."):
    try:
        if not os.path.exists("uploads"):
            os.makedirs("uploads")

        file_extension = image.filename.split(".")[-1]
        filename = f"{uuid.uuid4()}.{file_extension}"
        file_path = os.path.join("uploads", filename)
        print(file_path)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)


    except Exception as e:
        return JSONResponse(content=jsonable_encoder({"error": str(e)}), status_code=500)
    result = request.app.state.moondream.predict(
            "https://localhost:8000/uploads/"+filename,	# filepath  in 'Upload or Drag an Image' Image component
            question,
            api_name="/answer_question"
    ).strip()

    os.remove(file_path)
    return result

