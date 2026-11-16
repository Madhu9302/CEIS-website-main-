import logging
from fastapi import BackgroundTasks
from app.repositories.submission_repo import SubmissionRepository
from app.repositories.notification_repo import NotificationRepository
from app.schemas.submission import ContactRequest, QuoteRequest
from app.models.submission import Submission
from app.models.notification import Notification

logger = logging.getLogger(__name__)

def send_admin_email_alert(subject: str, body: str):
    # Background email task hook (configure SMTP credentials in .env later)
    logger.info(f"[BACKGROUND EMAIL SENT] Subject: {subject} | Body: {body}")

class SubmissionService:
    def __init__(self, sub_repo: SubmissionRepository, notif_repo: NotificationRepository):
        self.sub_repo = sub_repo
        self.notif_repo = notif_repo

    async def submit_contact(self, data: ContactRequest, bg_tasks: BackgroundTasks) -> dict:
        if data.website_url:  # Honeypot triggered by bot
            return {"message": "Thank you! Your inquiry has been received."}

        submission = Submission(
            type="contact",
            name=data.name.strip(),
            email=data.email.lower().strip(),
            phone=data.phone.strip() if data.phone else None,
            message=data.message.strip(),
        )
        saved = await self.sub_repo.create(submission)

        notif = Notification(
            title=f"New Contact Inquiry from {saved.name}",
            message=f"Email: {saved.email} | Message: {saved.message[:100]}...",
            submission_id=saved.id,
        )
        await self.notif_repo.create(notif)

        bg_tasks.add_task(
            send_admin_email_alert,
            subject=f"New Contact Inquiry: {saved.name}",
            body=f"Name: {saved.name}\nEmail: {saved.email}\nMessage: {saved.message}"
        )
        return {"message": "Thank you! Your inquiry has been received."}

    async def submit_quote(self, data: QuoteRequest, bg_tasks: BackgroundTasks) -> dict:
        if data.website_url:  # Honeypot triggered by bot
            return {"message": "Thank you! Your quote request has been received."}

        submission = Submission(
            type="quote",
            name=data.name.strip(),
            email=data.email.lower().strip(),
            phone=data.phone.strip() if data.phone else None,
            company=data.company.strip() if data.company else None,
            service_interest=data.service_interest.strip(),
            budget_range=data.budget_range.strip() if data.budget_range else None,
            message=data.message.strip(),
        )
        saved = await self.sub_repo.create(submission)

        notif = Notification(
            title=f"New Quote Request: {saved.service_interest} ({saved.name})",
            message=f"Company: {saved.company or 'N/A'} | Budget: {saved.budget_range or 'N/A'}",
            submission_id=saved.id,
        )
        await self.notif_repo.create(notif)

        bg_tasks.add_task(
            send_admin_email_alert,
            subject=f"New Quote Request from {saved.name}",
            body=f"Service: {saved.service_interest}\nBudget: {saved.budget_range}\nEmail: {saved.email}"
        )
        return {"message": "Thank you! Your quote request has been received."}