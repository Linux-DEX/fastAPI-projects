from typing import List

from fastapi import Depends, FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel

app = FastAPI()

MONGO_DETAILS = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGO_DETAILS)
database = client.mydatabase
collection = database.mycollection


class Item(BaseModel):
    name: str
    description: str


@app.on_event("startup")
async def startup_db_client():
    # we can add additional startup logic here
    pass


@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()


@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    result = await collection.insert_one(item.dict())
    new_item = await collection.find_one({"_id": result.inserted_id})
    return new_item


@app.get("/items/", response_model=List[Item])
async def read_items():
    items = await collection.find().to_list(100)
    return items
