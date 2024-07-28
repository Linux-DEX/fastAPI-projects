from fastapi import FastAPI, BackgroundTasks
from email_utils import send_email

app = FastAPI()

@app.post("/send/")
async def send_mail(subject: str, recipient: str, body: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(send_email, subject, recipient, body)
    return {"message": "Email sent"}

