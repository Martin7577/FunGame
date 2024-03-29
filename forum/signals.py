from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.conf import settings
from .models import Comment
from django.core.mail import send_mail
from django.contrib.auth.models import User
