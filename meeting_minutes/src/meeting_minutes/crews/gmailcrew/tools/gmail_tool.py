from typing import Type

from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from .gmail_utility import authenticate_gmail, create_message, create_draft

class GmailToolInput(BaseModel):
    """Input schema for MyCustomTool."""

    body: str = Field(..., description="The body of the email to send.")


class GmailTool(BaseTool):
    name: str = "Gmail Tool"
    description: str = (
        "Clear description for what this tool is useful for, your agent will need this information to use it."
    )
    args_schema: Type[BaseModel] = GmailToolInput

    def _run(self, body) -> str:
        # Implementation goes here
        try:
            service = authenticate_gmail()
            sender = "ishaangg12@gmail.com"
            to = "gishaan701@gmail.com"
            subject = "Meeting Minutes"
            message_text = body
            message = create_message(sender, to, subject, message_text)
            draft = create_draft(service, "me", message)
            return "Successfully sent email."
        except Exception as e:
            return f"Error sending email: {e}"
