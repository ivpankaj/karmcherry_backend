from celery import shared_task
from django.contrib.auth import get_user_model
from django.http import HttpRequest
from .utils import send_verification_email
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_verification_email_task(user_id, request_data):
    try:
        User = get_user_model()
        user = User.objects.get(id=user_id)
        request = HttpRequest()
        request.META['HTTP_HOST'] = request_data.get('host', 'localhost:8000')
        send_verification_email(user, request)
    except Exception as e:
        logger.exception("Error sending verification email for user_id %s", user_id)
