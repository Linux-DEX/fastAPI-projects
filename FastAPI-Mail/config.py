from pydantic import BaseSettings

class Settings(BaseSettings):
    # sendgrid api key from website
    SENDGRID_API_KEY: str = ""
    # email address here
    SENDGRID_FROM_EMAIL: str = "" 

settings = Settings()

