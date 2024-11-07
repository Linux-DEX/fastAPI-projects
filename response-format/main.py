import httpx
from fastapi import FastAPI, HTTPException, Request, Response
from pydantic import BaseModel, Field

app = FastAPI()


class UserResponse(BaseModel):
    id: int
    name: str
    email: str = Field(None, alias="gmail")


@app.get("/")
async def home_root():
    return {"message": "Fastapi home root"}


@app.get("/get-user/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    url = f"https://jsonplaceholder.typicode.com/users/{user_id}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="User not found")

    user_data = response.json()
    user = UserResponse(**user_data)

    return user
