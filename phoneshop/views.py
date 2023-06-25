from cmath import log
from django.shortcuts import render,redirect
from .models import Order,Spareparts
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import OrderForm
from django.contrib.auth.decorators import login_required
from . import forms

from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from smtplib import SMTPException

from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt 

import stripe
stripe.api_key="sk_test_51MYNGcJ6hbMus0QRH78fmV9wpJQKgiVgtk7rh6bZIrEO3mrdTZcw0WvYRteImm8Y5y9Gvv4L3UvV7PgLzeRJpkd200yqC2V29F"

def home(request):
    return render(request, 'phoneshop/home.html')


def about(request):
    return render(request, 'phoneshop/about.html', {'title': 'About'}) 


def contacts(request):
    return render(request,'phoneshop/contacts.html')


def payments(request):
    return render(request,'phoneshop/payments.html')

def spareparts(request):
    if request.method=='POST':
        first_name=request.POST.get("first_name")
        telephone=request.POST.get("telephone")
        email=request.POST.get("email")
        phone_model=request.POST.get("phone_model")
        spare=request.POST.get("spare")

        Spareparts.objects.create(
            first_name=first_name,
            telephone=telephone,
            phone_model=phone_model,
            email=email,
            spare=spare
        )
        subject="New Sparepart Request"
        email_template_name="phoneshop/sparepart.txt"
        context_data={
            "user": first_name,
            "phone_number": telephone,
            "phone_model": phone_model,
            "spare": spare,
            "email": email
        }
        email_message=render_to_string(email_template_name,context_data)
        to_address=email
        email=EmailMessage(
            subject,
            email_message,
            settings.EMAIL_HOST_USER,
            [to_address],
            reply_to=[settings.EMAIL_HOST_USER],
        )
        try:
            email.send(fail_silently=False)
            messages.info(request, f'{first_name}, Your Sparepart Request has been received. Check your email', extra_tags="info")
        except SMTPException as send_failed:
            print(f'Email not sent to {to_address}, due to {send_failed}')
    return render(request, 'phoneshop/spareparts.html')

def order(request):
    if request.method=='POST':
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        telephone=request.POST.get("telephone")
        phone_model=request.POST.get("phone_model")
        textmsg=request.POST.get("textmsg")
        date_brought=request.POST.get("date_brought")
        email=request.POST.get("email")

        Order.objects.create(
            email=email,
             first_name=first_name,
             last_name=last_name,
             telephone_number=telephone,
             date_brought=date_brought,
             phone_model=phone_model,
             description=textmsg

        )
        subject="New Order"
        email_template_name="phoneshop/email.txt"
        context_data={
        "user": first_name,
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "telephone":telephone,
        "phone_model": phone_model,
        "description": textmsg,
        "date_brought": date_brought
        }
        email_message=render_to_string(email_template_name, context_data)
        to_address=email
        email = EmailMessage(
                subject,
                email_message,
                settings.EMAIL_HOST_USER,
                [to_address],
                reply_to=[settings.EMAIL_HOST_USER],
            )
        try:
            email.send(fail_silently=False)
            messages.info(request, f'We have received your order {first_name} Check your email!' , extra_tags="info")
        except SMTPException as send_failed:
            print(f'Email not sent to {to_address} due to {send_failed}')
    return render(request,'phoneshop/order.html')


def  index(request):
    return render(request, 'phoneshop/landing.html')


def initiate_payment(request):
    if request.method=="POST":
        payment_form=forms.PaymentForm(request.POST)
        if payment_form.is_valid():
            payment=payment_form.save()
            render(request, 'phoneshop/make_payment.html', {'payment': payment})

    else:
        payment_form=forms.PaymentForm()
    return render(request,'phoneshop/initiate_payment.html', {'payment_form': payment_form})


@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)#returns publishable key to our html

@csrf_exempt
def create_checkout_session(request):
    session = stripe.checkout.Session.create(
    payment_method_types=['card'],
    line_items=[{
    'price_data': {
    'currency': 'kes',
    'product_data': {
    'name': 'Phone repair',
    },
    'unit_amount': 20000,
    },
    'quantity': 1,
    }],
    mode='payment',
    success_url=settings.API_TEST_URL + '/pay_success/',
    cancel_url=settings.API_TEST_URL + '/pay_cancel/',
    )
    return JsonResponse({'id': session.id})

 
def stripe_success(request):
    return render(request, 'phoneshop/pay_success.html')


def stripe_cancel(request):
    return render(request, 'phoneshop/pay_cancel.html')

