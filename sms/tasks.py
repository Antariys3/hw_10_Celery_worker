from celery import shared_task
from django.conf import settings
from twilio.rest import Client

client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)


@shared_task
def send_sms(receiver, message):
    print("Hello from server")
    message = client.messages \
        .create(
        body=message,
        # body="Your verification code is 1234",
        from_='+13366456233',
        to=receiver
    )

    print(message.sid)
    return message.sid
