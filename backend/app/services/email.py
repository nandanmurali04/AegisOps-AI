from fastapi_mail import FastMail, MessageSchema, MessageType

from app.core.mail import conf


async def send_email(
    recipients: list[str],
    subject: str,
    body: str,
):
    message = MessageSchema(
        subject=subject,
        recipients=recipients,
        body=body,
        subtype=MessageType.plain,
    )

    fm = FastMail(conf)
    await fm.send_message(message)