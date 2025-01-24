import os
import base64
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from email.message import EmailMessage

import markdown
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

SCOPES = ['https://mail.google.com/"']

HTML_TEMPLATE = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body>
        {final_email_body}
    </body>
    </html>
"""

def authenticate_gmail():
    """Authenticate to the Gmail API using credentials from environment variables."""
    client_id = os.getenv('GMAIL_CLIENT_ID')
    client_secret = os.getenv('GMAIL_CLIENT_SECRET')
    refresh_token = os.getenv('GMAIL_REFRESH_TOKEN')

    if not all([client_id, client_secret, refresh_token]):
        raise EnvironmentError(
            "CLIENT_ID, CLIENT_SECRET, and REFRESH_TOKEN must be set in the .env file."
        )

    creds = Credentials(
        None,
        refresh_token=refresh_token,
        token_uri='https://oauth2.googleapis.com/token',
        client_id=client_id,
        client_secret=client_secret,
        scopes=SCOPES
    )

    try:
        # Refresh the access token if necessary
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
    except Exception as e:
        print(f"Failed to refresh credentials: {e}")
        raise

    service = build('gmail', 'v1', credentials=creds)
    return service

def create_message(sender, to, subject, message_text):
    """Create a message for an email.
    
    Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email.
    message_text: The text of the email.

    Returns:
        An object containing a base64url encoded email object.
    """

    md = markdown.Markdown(extensions=['tables', 'fenced_code', 'nl2br'])
    
    # Format the HTML content
    formatted_html = HTML_TEMPLATE.format(
        final_email_body=md.convert(message_text)
    )

    msg = EmailMessage()
    content = formatted_html

    msg['To'] = to
    msg['From'] = sender
    msg['Subject'] = subject
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(content)

    encodedMsg = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    
    # The API expects a dictionary with a 'raw' key containing the encoded message
    return {'raw': encodedMsg}

def create_draft(service, user_id, message_body):
    """Create and insert a draft email.

    Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
             can be used to indicate the authenticated user.
    message_body: The body of the draft email.

    Returns:
        The created draft.
    """
    try:
        draft = service.users().drafts().create(userId=user_id, body={'message': message_body}).execute()
        print(f'Draft id: {draft["id"]}\nDraft message: {draft["message"]}')
        return draft
    except Exception as error:
        print(f'An error occurred: {error}')
        return None 

