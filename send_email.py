from typing import List

import jwt
from fastapi import BackgroundTasks, Form, UploadFile, File, Depends, HTTPException, status
from fastapi_mail import FastMail, ConnectionConfig, MessageSchema
from dotenv import dotenv_values
from pydantic import BaseModel, EmailStr

from models import User

config_credentials = dotenv_values(".env")

conf = ConnectionConfig(
    MAIL_USERNAME=config_credentials["EMAIL"],
    MAIL_PASSWORD=config_credentials["PASS"],
    MAIL_FROM=config_credentials["EMAIL"],
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,    # Enable STARTTLS
    MAIL_SSL_TLS=False,    # Disable SSL/TLS
    USE_CREDENTIALS=True
)


class EmailSchema(BaseModel):
    email: List[EmailStr]


async def send_email(email: EmailSchema, instance: User):
    token_data = {
        "id": instance.id,
        "username": instance.username,
    }

    token = jwt.encode(token_data, config_credentials["SECRET"], algorithm="HS256")

    template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Account Verification</title>
    </head>
    <body style="font-family: Arial, sans-serif; background-color: #f5f5f5; padding: 20px;">
        <div style="max-width: 600px; margin: auto; background-color: #ffffff; padding: 30px; border-radius: 8px; text-align: center;">
            <h2>Account Verification</h2>
            <p>Please click on the button below to verify your account.</p>
            <a href="http://localhost:8000/verification/?token={token}" style="display: inline-block; padding: 10px 20px; color: white; background-color: #007BFF; text-decoration: none; border-radius: 5px;">
                Verify Your Email
            </a>
        </div>
    </body>
    </html>
    """

    message = MessageSchema(
        subject="EasyShops Account verification Email",
        recipients=email,
        body=template,
        subtype="html"
    )

    fm = FastMail(conf)
    await fm.send_message(message=message)
