from fastapi import FastAPI
from celery_app import add  
from celery.result import AsyncResult

app = FastAPI()

@app.post("/add")
async def add_numbers(x: int, y: int):
    task = add.delay(x, y)
    return {"task_id": task.id}

@app.get("/task/{task_id}")
async def get_task_result(task_id: str):
    task = AsyncResult(task_id)
    
    if task.state == 'PENDING':
        return {"status": "Task is pending"}
    elif task.state == 'SUCCESS':
        return {"status": "Task completed", "result": task.result}
    elif task.state == 'FAILURE':
        return {"status": "Task failed", "error": str(task.info)}
    else:
        return {"status": "Unknown state"}