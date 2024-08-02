from fastapi import FastAPI, Response, Request, Depends, Cookie
# from starlette.middleware.base import BaseHTTPMiddleware 
# from starlette.requests import Request 
# from starlette.responses import Response 
from pydantic import BaseModel, Field
from typing import Optional, Any, Dict

app = FastAPI()

# class AddHeaderMiddleware(BaseHTTPMiddleware):
#     async def dispatch(self, request: Request, call_next):
#
#         # val = request.cookies.get("Name")
#         # print(f"cookie value {val}")
#         # if not val:
#         #     raise HTTPException(status_code=400, detail="Cookie is missing")
#         # response.headers["name"] = "linuxdex"
#
#         headers = dict(request.headers)
#
#         headers["X-Custom-Header"] = "CustomValue"
#
#         modified_request = Request(
#             scope=request.scope,
#             receive=request.receive,
#             headers=headers
#         )
#
#         response = await call_next(modified_request)
#
#         # response = await call_next(request)
#         return response 
#
# app.add_middleware(AddHeaderMiddleware)

class FilterSortModel(BaseModel):
    filter: Optional[Dict] = Field(None, description="Filter criteria")
    sort: Optional[str] = Field(None, description="Sort order")
    cookie_value: Optional[Dict] = Field(None, description="Cookie value")

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
    cookie_value = eval(cookie_value)
    return { "Cookie value": cookie_value }

async def process_request(request: Request):
    cookie_value = request.cookies.get("Name", "cookie not found")
    cookie_value = eval(cookie_value)
    return cookie_value

@app.get("/list")
async def list_value( request: Request , cookie_value: str = Depends(process_request)):
    body = request.query_params

    return {
        "message": body,
        "cookie": cookie_value
    }

async def get_filter_sort_data(request: Request, cookie_value: str = Depends(process_request) ) -> FilterSortModel:
    query_params = request.query_params
    filter_param = eval(query_params.get('filter', None))
    sort_param = query_params.get('sort', None)

    return FilterSortModel(
        filter=filter_param,
        sort=sort_param,
        cookie_value=cookie_value
    )

# async def get_filter_sort_data(request: Request ) -> FilterSortModel:
#
#     cookie_value = request.cookies.get("Name")
#     query_params = request.query_params
#     filter_param = query_params.get('filter', None)
#     sort_param = query_params.get('sort', None)
#
#     return FilterSortModel(
#         filter=filter_param,
#         sort=sort_param,
#         cookie_value=cookie_value
#     )

@app.get("/items/")
async def read_items(data: FilterSortModel = Depends(get_filter_sort_data)):
    filter_value = data.filter
    sort_value = data.sort
    cookie_value = data.cookie_value
    
    # return {
    #     "filter": filter_value,
    #     "sort": sort_value,
    #     "cookie_value": cookie_value
    # }
    return data
