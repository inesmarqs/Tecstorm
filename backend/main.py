import asyncio
import os
import shutil
from pathlib import Path
import ai_services
from database import SessionLocal
from fastapi import Depends, FastAPI, File, HTTPException, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, StreamingResponse
from database.models import Client, Product, Allergen, Ingredient, NutricionalInformation
from sqlalchemy.orm import Session

from database.commands_database import (
    add_client,
    add_allergen,
    add_ingredient,
    add_nutricional_info,
    add_product,
    get_allergens_by_client,
    get_client,
    get_ingredients_by_product,
    get_nutricional_info,
    get_product
)

app = FastAPI()

def get_db():
    """_get_db_.

    Yields:
        Session: SQLAlchemy session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/video/{video_id}/claim/{claim_id}")
async def get_clip(video_id: str, claim_id: int):
    """_Send video file to client based on video_id and claim_id_."""
    video_path = f"{video_id}/clips/claim_{claim_id}.mp4"
    if not os.path.exists(upload_directory/video_path):
        raise HTTPException(status_code=404, detail="Video not found")
    print(upload_directory/video_path)
    return StreamingResponse(open(upload_directory/video_path, "rb"), media_type="video/mp4")  # noqa: SIM115







