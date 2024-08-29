# import asyncio
#
# import httpx
# from fastapi import FastAPI
# from pymongo import MongoClient
#
# app = FastAPI()
#
# # MongoDB client setup
# client = MongoClient("mongodb://localhost:27017/")
# db = client["your_database_name"]
#
#
# async def fetch_from_mongodb(collection_name: str, query: dict):
#     collection = db[collection_name]
#     document = collection.find_one(query)
#     return document
#
#
# async def fetch_from_api(url: str) -> dict:
#     async with httpx.AsyncClient() as client:
#         response = await client.get(url)
#         response.raise_for_status()  # Ensure we raise an error for bad responses
#         return response.json()
#
#
# @app.get("/combined-data/")
# async def get_combined_data():
#     # Define MongoDB queries and collection names
#     mongo_queries = [
#         ("collection1", {"field": "value1"}),
#         ("collection2", {"field": "value2"}),
#     ]
#
#     # Define API endpoints
#     api_urls = ["https://api.example.com/data1", "https://api.example.com/data2"]
#
#     # Create tasks for MongoDB queries
#     mongo_tasks = [
#         fetch_from_mongodb(collection, query) for collection, query in mongo_queries
#     ]
#
#     # Create tasks for API requests
#     api_tasks = [fetch_from_api(url) for url in api_urls]
#
#     # Run all tasks concurrently
#     mongo_results = await asyncio.gather(*mongo_tasks)
#     api_results = await asyncio.gather(*api_tasks)
#
#     # Combine results
#     combined_data = {"mongodb_data": mongo_results, "api_data": api_results}
#
#     return combined_data


# below code is for post method


import asyncio

import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


# Define Pydantic models for request data
class PostData(BaseModel):
    key1: str = None
    key2: str = None


# Asynchronous methods to post data
async def post_method_1(url: str, data: dict):
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=data)
        response.raise_for_status()
        return response.json()


async def post_method_2(url: str, data: dict):
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=data)
        response.raise_for_status()
        return response.json()


# Endpoint to handle POST requests
@app.post("/run-posts/")
async def run_posts(data: PostData):
    url1 = "https://httpbin.org/post"
    url2 = "https://httpbin.org/post"

    # Prepare the data for each POST method
    data1 = {"key1": data.key1} if data.key1 else {}
    data2 = {"key2": data.key2} if data.key2 else {}

    try:
        # Run both POST methods concurrently
        response1, response2 = await asyncio.gather(
            post_method_1(url1, data1), post_method_2(url2, data2)
        )
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))

    return {"response_from_method_1": response1, "response_from_method_2": response2}
