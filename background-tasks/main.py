from fastapi import FastAPI, Request, Response, BackgroundTasks

app = FastAPI()

@app.get("/")
async def root_func():
    return {"message": "Background task"}

def write_log(message: str):
    with open("log.txt", mode="a") as log:
        log.write(message + '\n')

@app.post("/send-notification/")
async def send_notification(background_tasks: BackgroundTasks, message: str):
    background_tasks.add_task(write_log, message)
    return {"message": "Notification sent in the background"}
