import json

import redis
import requests
from fastapi import FastAPI, Response

app = FastAPI()

rd = redis.Redis(host="localhost", port=6379, db=0)


@app.get("/")
def read_root():
    return Response("Hello world")


@app.get("/posts/{id}")
def read_post(id: str):
    cache = rd.get(id)
    if cache:
        print("cache hit")
        return json.loads(cache)
    else:
        print("cache miss")
        r = requests.get(f"https://jsonplaceholder.typicode.com/posts/{id}")
        rd.set(id, r.text)
        rd.expire(id, 5)
        return r.json()
