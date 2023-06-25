from unicodedata import name
from django.urls import path
from . import views

    
urlpatterns=[
    path('', views.home, name='home'),
    path ('about/', views.about, name='about'),
    path('contacts/', views.contacts, name='contacts'),
    path('order/', views.order, name='order'),
    path('payments/', views.payments, name="payments"),
    path('spareparts/', views.spareparts, name='spareparts'),
    path('config/', views.stripe_config, name='stripe_key'),
    path('create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),
    path('pay_success/', views.stripe_success, name='stripe_success'),
    path('pay_cancel/', views.stripe_cancel, name='stripe_cancel'),
]