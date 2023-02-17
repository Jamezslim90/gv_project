from django.urls import path
from .views import AboutPageView, ContactPageView, FAQPageView, TermsPageView
from . import views



urlpatterns = [

path('',   views.home_page, name='home'),
path('about/',  AboutPageView.as_view() , name='about'),
path('contact/',  ContactPageView.as_view() , name='contact'),
path('faq/',  FAQPageView.as_view() , name='faq'),
path('terms/',  TermsPageView.as_view() , name='terms'),

]
