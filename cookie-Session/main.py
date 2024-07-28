from fastapi import FastAPI, Depends, HTTPException, Cookie, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta

app = FastAPI()

fake_users_db = {
    "user": {
        "username": "user",
        "full_name": "Test User",
        "email": "testuser@example.com",
        "hashed_password": "password",
    }
}

class User(BaseModel):
    username: str
    email: str

@app.post("/signup")
async def signup(user: User):
    return JSONResponse(content={"message": "User signed up successfully."})

@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_users_db.get(form_data.username)
    if not user or user['hashed_password'] != form_data.password:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    data = {
        "user": form_data.username,
        "role": ["user"],
        "id": "any id"
    }

    response = JSONResponse(content={"message": "Login successful!"})
    response.set_cookie(key="session", value=data, httponly=True)
    return response

# @app.get("/user")
# async def read_user(session: Optional[str] = Cookie(None)):
#     print(f"session before -> {session}")
#     # if not session or session not in fake_users_db:
#     #     raise HTTPException(status_code=401, detail="User not logged in")
#
#     if not session:
#         raise HTTPException(status_code=401, detail="User not logged in")
#
#     print(f"session after -> {session}")
#     # return {"user": fake_users_db[session]}
#     return {"user": session}

@app.get("/user")
async def read_user(request: Request):
    result = request.cookies.get("session")
    result = eval(result)
    return result

@app.get("/logout")
async def logout():
    response = JSONResponse(content={"message": "Logged out"})
    response.delete_cookie(key="session")
    return response


