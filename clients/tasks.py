from celery import shared_task
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib import messages



@shared_task
def add(x, y):
    return x + y


@shared_task    
def send_vaccination_pre_exp(mail_subject, mail_template, context):
    
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = context['to_email']
        message = render_to_string(mail_template, context)
        mail = EmailMessage(mail_subject, message, from_email, to=[to_email])
        mail.content_subtype = "html"
        mail.send()
    
  
@shared_task    
def send_vaccination_on_exp(mail_subject, mail_template2, context):
   
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = context['to_email']
        message = render_to_string(mail_template2, context)
        mail = EmailMessage(mail_subject, message, from_email, to=[to_email])
        mail.content_subtype = "html"
        mail.send()
        
        
        
