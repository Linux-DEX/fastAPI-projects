import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content
from config import settings

sg = sendgrid.SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)

async def send_email(subject: str, recipient: str, body: str):
    from_email = Email(settings.SENDGRID_FROM_EMAIL)
    to_email = To(recipient)
    content = Content("text/html", body)
    mail = Mail(from_email, to_email, subject, content)
    
    response = sg.send(mail)
    print(f"Status Code: {response.status_code}, Body: {response.body}, Headers: {response.headers}")

