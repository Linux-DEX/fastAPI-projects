# from fastapi import FastAPI, Request
# from fastapi.responses import JSONResponse 
#
# app = FastAPI()
#
# usersession = {
#     "name": "linuxdex",
#     "linux": "Arch Linux"
# }
#
# @app.middleware("http")
# async def add_custom_headers(request: Request, call_next):
#
#     request.headers.__dict__["_list"].append(
#         (b"new-header", b"new-value")
#     )
#
#     # request.state.custom_field = "customeValue"
#     request.state.custom_field = usersession
#
#     response = await call_next(request)
#     return response
#
# @app.get("/")
# async def read_root(request: Request):
#     return JSONResponse( content={
#         "message": "Request received",
#         "modified_headers": dict(request.headers),
#         "custom_field": request.state.custom_field
#     })


# NOTE: this is different method 

from fastapi import FastAPI, Response, Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware 
# from starlette.requests import Request 
# from starlette.responses import Response 
from fastapi.responses import JSONResponse

app = FastAPI()

class AddHeaderMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response: Response = await call_next(request)

        try:
            val = request.cookies.get("Name")
            print(f"cookie value {val}")
        except:
            pass
        # if not val:
        #     raise HTTPException(status_code=400, detail="Cookie is missing")
        # response.headers["name"] = "linuxdex"

        # test 
        body = request.query_params
        body = dict(body)
        body["usersession"] = val
        print(f"middleware body -> {body}")


        return response 

app.add_middleware(AddHeaderMiddleware)

@app.get("/")
async def read_root():
    return { "Hello": "FastAPI" }

@app.post("/set-cookie")
async def create_cookie(response: Response):
    cookie_body = {
        "name": "linux dex",
        "project": "hyperland",
        "role": "full stack developer"
    }
    response.set_cookie(key="Name", value=cookie_body)
    return { "message": "Cookie has been set" }

@app.get("/remove-cookie")
async def remove_cookie(response: Response):
    response.delete_cookie(key="Name")
    return { "message": "Cookie has been removed" }

@app.get("/get-cookie")
async def remove_cookie(request: Request):
    cookie_value = request.cookies.get("Name", "Cookie not found")
    return { "Cookie value": cookie_value }

@app.get("/list")
async def list_value( request: Request ):
    body = request.query_params

    result = dict(body)
    try:
        print(f"usersession in api -> {result["usersession"]}")
    except:
        pass
    return {
        "message": body
    }



