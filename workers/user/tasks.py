from celery import shared_task
from celery_singleton import Singleton

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth import  get_user_model
from django.conf import settings
from django.db import transaction

User = get_user_model()


@shared_task(base=Singleton)
def send_activated_code(email):
    with transaction.atomic():
        user = User.objects.select_for_update().get(email=email)
        user.get_new_activate_code()
        activated_code = user.activate_code.code
    title, from_email = "Служба технической поддержки учетных записей MyPharm", settings.EMAIL_HOST_USER
    title_send = 'Разовый код'
    to_form, headers = f'{user.get_full_name()} <{email}>', {'From': f'{title} <{from_email}>'}
    html_content = render_to_string(
        'sends_email/password_reset_mail.html',
        {
            "user": user,
            'activate_code': activated_code,
            'site': settings.FRONT_END_SITE,
        }
    )
    text_content = strip_tags(html_content)
    msg = EmailMultiAlternatives(title_send, text_content, from_email, [to_form], headers=headers)
    msg.attach_alternative(html_content, "text/html")
    msg.send(fail_silently=False)
    return str(f'Sent to {email}')
