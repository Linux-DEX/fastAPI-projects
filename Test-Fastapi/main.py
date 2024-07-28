
from fastapi import FastAPI, Response, Request

app = FastAPI()

@app.post("/cookie-and-object/")
def create_cookie(response: Response):
    response.set_cookie(key="Name", value="fake-cookie-session-value")
    return {"message": "Come to the dark side, we have cookies"}

@app.get("/remove-cookie")
async def remove_cookie(response: Response):
    response.delete_cookie(key="Name")
    return { "message": "Cookie has been removed" }

@app.get("/get-cookie")
async def remove_cookie(request: Request):
    cookie_value = request.cookies.get("Name", "Cookie not found")
    return { "Cookie value": cookie_value }
