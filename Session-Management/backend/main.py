from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# @app.post("/receive-data")
# async def receive_data(data: dict):
#     # Process the received data here
#     print(f"Received data: {data['data']}")
#     return {"status": "success", "received_data": data['data']}


@app.post("/receive-data")
async def receive_data(request: Request):
    print(request.headers.get("usersession"))
    return request.headers
