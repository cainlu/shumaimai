from django.dispatch import *

email_confirmed = Signal(providing_args=["confirmation"])
email_confirmation_sent = Signal(providing_args=["confirmation"])
