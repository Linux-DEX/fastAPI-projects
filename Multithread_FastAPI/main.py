# import random
# import string
#
# from fastapi import FastAPI
#
# app = FastAPI()
#
#
# @app.get("/")
# async def index():
#     mystr = "".join(random.choices(string.ascii_lowercase, k=5))
#     return {"data": mystr}
#
#
# @app.get("/items/{item_id}")
# async def read(item_id: int):
#     return {"item_id": item_id}

import time
from concurrent.futures import ThreadPoolExecutor

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Initialize a ThreadPoolExecutor with a desired number of threads
executor = ThreadPoolExecutor(max_workers=4)


# Define a data model for the request
class CalculationRequest(BaseModel):
    number: int


# Simulate a CPU-bound task with time measurement
def compute_heavy_task(number: int) -> tuple:
    start_time = time.time()  # Record the start time
    time.sleep(2)  # Simulate a delay
    result = number**2  # Example computation
    end_time = time.time()  # Record the end time
    time_taken = end_time - start_time  # Calculate the time taken
    return result, time_taken


@app.post("/compute")
def compute(request: CalculationRequest):
    # Submit the compute_heavy_task to the thread pool executor
    future = executor.submit(compute_heavy_task, request.number)
    result = future.result()  # Wait for the result
    return {"result": result}
