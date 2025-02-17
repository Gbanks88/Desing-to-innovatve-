import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from typing import List, Optional
from fastapi import HTTPException

class EmailService:
    def __init__(self):
        self.smtp_server = "ssl0.ovh.net"
        self.smtp_port = 587
        self.username = os.getenv('OVH_EMAIL')
        self.password = os.getenv('OVH_EMAIL_PASSWORD')
        self.from_email = os.getenv('OVH_EMAIL')

    async def send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        text_content: Optional[str] = None,
        attachments: Optional[List[tuple]] = None
    ) -> bool:
        """
        Send an email using OVH Email Pro
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            html_content: HTML content of the email
            text_content: Plain text content (optional)
            attachments: List of tuples (filename, file_data, content_type)
        """
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.from_email
            msg['To'] = to_email

            # Add plain text version
            if text_content:
                msg.attach(MIMEText(text_content, 'plain'))

            # Add HTML version
            msg.attach(MIMEText(html_content, 'html'))

            # Add attachments
            if attachments:
                for filename, file_data, content_type in attachments:
                    if content_type.startswith('image/'):
                        attachment = MIMEImage(file_data)
                    else:
                        attachment = MIMEText(file_data)
                    attachment.add_header(
                        'Content-Disposition',
                        'attachment',
                        filename=filename
                    )
                    msg.attach(attachment)

            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.send_message(msg)

            return True

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to send email: {str(e)}"
            )

    async def send_welcome_email(self, to_email: str, username: str) -> bool:
        """Send welcome email to new users"""
        subject = "Welcome to John Allen's Fashion Platform!"
        html_content = f"""
        <html>
            <body>
                <h1>Welcome to John Allen's Fashion Platform, {username}!</h1>
                <p>We're excited to have you join our community of fashion enthusiasts.</p>
                <p>Here's what you can do on our platform:</p>
                <ul>
                    <li>Explore latest fashion trends</li>
                    <li>Watch educational videos</li>
                    <li>Apply for scholarships</li>
                    <li>Connect with other fashion enthusiasts</li>
                </ul>
                <p>If you have any questions, feel free to reach out to our support team.</p>
                <p>Best regards,<br>John Allen's Fashion Team</p>
            </body>
        </html>
        """
        text_content = f"""
        Welcome to John Allen's Fashion Platform, {username}!
        
        We're excited to have you join our community of fashion enthusiasts.
        
        Here's what you can do on our platform:
        - Explore latest fashion trends
        - Watch educational videos
        - Apply for scholarships
        - Connect with other fashion enthusiasts
        
        If you have any questions, feel free to reach out to our support team.
        
        Best regards,
        John Allen's Fashion Team
        """
        return await self.send_email(to_email, subject, html_content, text_content)

    async def send_password_reset(self, to_email: str, reset_token: str) -> bool:
        """Send password reset email"""
        reset_link = f"https://yourfashionapp.com/reset-password?token={reset_token}"
        subject = "Password Reset Request"
        html_content = f"""
        <html>
            <body>
                <h1>Password Reset Request</h1>
                <p>You have requested to reset your password.</p>
                <p>Click the link below to reset your password:</p>
                <p><a href="{reset_link}">Reset Password</a></p>
                <p>If you didn't request this, please ignore this email.</p>
                <p>Best regards,<br>John Allen's Fashion Team</p>
            </body>
        </html>
        """
        text_content = f"""
        Password Reset Request
        
        You have requested to reset your password.
        
        Click the link below to reset your password:
        {reset_link}
        
        If you didn't request this, please ignore this email.
        
        Best regards,
        John Allen's Fashion Team
        """
        return await self.send_email(to_email, subject, html_content, text_content)
