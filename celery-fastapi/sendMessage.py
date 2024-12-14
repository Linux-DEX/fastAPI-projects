import time
from fastapi import FastAPI
from celery import shared_task, Celery

app = FastAPI()

celery = Celery(
    __name__,
    broker='redis://localhost:6379/0',  
    backend='redis://localhost:6379/0',  
)

@celery.task
def send_push_notification(device_token: str):
    time.sleep(10) 
    with open("notification.log", mode="a") as notification_log:
        response = f"Successfully sent push notification to: {device_token}\n"
        notification_log.write(response)

@app.get("/push/{device_token}")
async def notify(device_token: str):
    send_push_notification.delay(device_token)
    return {"message": "Notification sent"}

