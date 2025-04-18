from django.core.mail import EmailMessage
from django.template.loader import render_to_string


def send_confirmation_email(confirmation_link, user=None):
    subject = "Confirm your email address"
    context = {
        'site_name': 'vocavolt.com',
        'confirmation_link': confirmation_link,
    }
    context['user'] = user
    message = render_to_string("emails/account_confirmation.html", context)
    email = EmailMessage(subject, message, to=[user.email])
    email.content_subtype = "html"
    email.send()


def send_password_reset_email(reset_link, user):
    subject = 'Reset Your Vocavolt Password'

    context = {
        'site_name': 'vocavolt.com',
        'confirmation_link': reset_link,
    }
    context['user'] = user
    message = render_to_string("emails/password_reset_email.html", context)
    email = EmailMessage(subject, message, to=[user.email])
    email.content_subtype = "html"
    email.send()