from fastapi import APIRouter

from app.services.email import send_email

router = APIRouter(
    prefix="/email",
    tags=["Email"]
)


@router.get("/test")
async def test_email():

    await send_email(
        recipients=["nandan04in@gmail.com"],
        subject="AegisOps AI Test Email",
        body="🎉 Congratulations! Your email service is working successfully."
    )

    return {
        "message": "Email sent successfully!"
    }