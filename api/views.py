from django.shortcuts import render
from inbound_email.signals import email_received

from .models import Trial

@email_received
def on_email_received(sender, **kwargs):
    """Handle inbound emails."""
    email = kwargs.pop('email')
    request = kwargs.pop('request')

    Trial.objects.create(
        name = email.subject,
        period = 30,
    )