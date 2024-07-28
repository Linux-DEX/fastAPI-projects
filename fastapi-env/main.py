from fastapi import FastAPI, Depends, Request, Response
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

@app.get("/")
async def root_fn():
    return {
        "message": "Fastapi is running"
    }

@app.get("/test")
async def test_fn():
    anime = os.getenv("ANIME_URI")
    github = os.getenv("GITHUB_URI")
    return {
        "anime": anime,
        "github": github
    }
