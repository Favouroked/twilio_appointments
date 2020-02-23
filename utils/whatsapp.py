import os

from twilio.rest import Client

ACCOUNT_SID = os.getenv('ACCOUNT_SID')
AUTH_TOKEN = os.getenv('AUTH_TOKEN')
TWILIO_NUMBER = os.getenv('TWILIO_NUMBER')
client = Client(ACCOUNT_SID, AUTH_TOKEN)


def format_message(appointment):
    message = "You have an appointment\n"
    message += f"Title: {appointment['title']}\n"
    message += f"Description: {appointment['description']}\n"
    message += f"Time: {appointment['time']}"
    return message


def send_message(appointment):
    message = client.messages.create(
        from_=f'whatsapp:{TWILIO_NUMBER}',
        body=format_message(appointment),
        to=f"whatsapp:{appointment['phone']}"
    )
    return message.sid
