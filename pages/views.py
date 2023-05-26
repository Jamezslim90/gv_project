from django.shortcuts import render
import logging
import datetime
from django.conf import settings
from django.http.response import HttpResponseRedirect
from django.core.mail import EmailMessage
from django.views.generic import TemplateView 
from django.shortcuts import render
from django.contrib import messages
#from blog.models import Post
#from django.core.mail import EmailMessage


def home_page(request):
    """
    post_list = Post.published.all()
    
    #Latest Post
    latest_posts = Post.published.order_by('-publish')[:4]

    # This object belongs to the render function {'latest_posts': latest_posts}

    """
    
    return render(request,
                 'pages/home.html')



class AboutPageView(TemplateView):
    
    template_name = 'pages/about.html'



class ContactPageView(TemplateView):
    
    template_name = 'pages/contact.html'


    def post(self, request):
        firstName = request.POST.get("firstName") 
        lastName = request.POST.get("lastName")
        phoneNumber = request.POST.get("phoneNumber")
        email = request.POST.get("email")
        message = request.POST.get("message")

        email = EmailMessage(
            subject= f"{firstName} {lastName} {phoneNumber} Enquiries.",
            body=message,
            from_email=email,
            to=[settings.EMAIL_HOST_USER],
            reply_to=[email]
        )
        email.send()
        messages.add_message(request, messages.SUCCESS, f"Thank you {firstName} for contacting. We will contact you ASAP!")
        return HttpResponseRedirect(request.path)




class FAQPageView(TemplateView):
    
    template_name = 'pages/faq.html'

class TermsPageView(TemplateView):
    
    template_name = 'pages/terms.html'
