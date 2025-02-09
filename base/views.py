from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.http import JsonResponse , HttpResponse
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

#zarinpal
from django.conf import settings
import requests
import json


from base import models as base_models
from doctor import models as doctor_models
from patient import models as patient_models

def index(request):
    services = base_models.Service.objects.all()
    context = {
        "services": services
    }
    return render(request, "base/index.html", context)

def service_detail(request, service_id):
    service = base_models.Service.objects.get(id=service_id)

    context = {
        "service": service
    }
    return render(request, "base/service_detail.html", context)

@login_required
def book_appointment(request, service_id, doctor_id):
    service = base_models.Service.objects.get(id=service_id)
    doctor = doctor_models.Doctor.objects.get(id=doctor_id)
    patient = patient_models.Patient.objects.get(user=request.user)

    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        gender = request.POST.get("gender")
        address = request.POST.get("address")
        dob = request.POST.get("dob")
        issues = request.POST.get("issues")
        symptoms = request.POST.get("symptoms")

        # Update patient bio data
        patient.full_name = full_name
        patient.email = email
        patient.mobile = mobile
        patient.gender = gender
        patient.address = address
        patient.dob = dob
        patient.save()

        # Create appointment object
        appointment = base_models.Appointment.objects.create(
            service=service,
            doctor=doctor,
            patient=patient,
            appointment_date=doctor.next_available_appointment_date,
            issues=issues,
            symptoms=symptoms,
        )

        # Create a billing objects
        billing = base_models.Billing()
        billing.patient = patient
        billing.appointment = appointment
        billing.sub_total = appointment.service.cost
        billing.tax = appointment.service.cost * 5 / 100
        billing.total = billing.sub_total + billing.tax # مجموع با مالیات
        billing.status = "Unpaid"
        billing.save()

        return redirect("base:checkout", billing.billing_id)

    context = {
        "service": service,
        "doctor": doctor,
        "patient": patient,
    }
    return render(request, "base/book_appointment.html", context)


@login_required
def checkout(request, billing_id):
    billing = base_models.Billing.objects.get(billing_id=billing_id)

    # ارسال درخواست پرداخت به زرین‌پال
    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": int(billing.total),  # مبلغ بر حسب ریال
        "Description": f"پرداخت برای نوبت {billing.appointment.id}",
        "CallbackURL": request.build_absolute_uri("/verify/"),
    }
    headers = {'content-type': 'application/json'}
    try:
        response = requests.post(url=ZP_API_REQUEST, data=json.dumps(req_data), headers=req_header)
        response_data = response.json()

        if "errors" not in response_data or len(response_data["errors"]) == 0:
            authority = response_data["data"]["authority"]
            return redirect(ZP_API_STARTPAY.format(authority=authority))

        else:
            e_code = response_data["errors"]["code"]
            e_message = response_data["errors"]["message"]
            return JsonResponse({"error": f"پرداخت ناموفق بود - کد: {e_code}, پیام: {e_message}"}, status=400)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": f"خطا در ارسال درخواست: {str(e)}"}, status=500)



MERCHANT = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
ZP_API_REQUEST = "https://api.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = "https://api.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = "https://www.zarinpal.com/pg/StartPay/{authority}"
amount = 11000  # Rial / Required
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
email = 'email@example.com'  # Optional
mobile = '09123456789'  # Optional
# Important: need to edit for realy server.
CallbackURL = 'http://localhost:8000/verify'


def send_request(request):
    open_order: Order = Order.objects.filter(user_id=request.user.id, paid=False).first()
    if open_order is not None:
        total_price = open_order.total_price()
        print(total_price)
        req_data = {
            "merchant_id": MERCHANT,
            "amount": total_price,
            "callback_url": f"{CallbackURL}/{open_order.id}",
            "description": description,
            "metadata": {"mobile": mobile, "email": email}
        }
        req_header = {"accept": "application/json", "content-type": "application/json'"}
        req = requests.post(url=ZP_API_REQUEST, data=json.dumps(req_data), headers=req_header)
        authority = req.json()['data']['authority']
        if len(req.json()['errors']) == 0:
            return redirect(ZP_API_STARTPAY.format(authority=authority))
        else:
            e_code = req.json()['errors']['code']
            e_message = req.json()['errors']['message']
            return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")


def verify(request, *args, **kwargs):
    order_id = kwargs['order_id']
    t_status = request.GET.get('Status')
    t_authority = request.GET['Authority']
    if request.GET.get('Status') == 'OK':
        req_header = {"accept": "application/json",
                      "content-type": "application/json'"}
        req_data = {
            "merchant_id": MERCHANT,
            "amount": amount,
            "authority": t_authority
        }
        req = requests.post(url=ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)
        if len(req.json()['errors']) == 0:
            t_status = req.json()['data']['code']
            if t_status == 100:
                order = Order.objects.get_queryset().get(id=order_id)
                order.paid = True
                order.pay_date = time.time()
                order.save()
                context = {
                    'refID': str(req.json()['data']['ref_id'])
                }
                return render(request, '', context)
            elif t_status == 101:
                return HttpResponse('Transaction submitted : ' + str(
                    req.json()['data']['message']
                ))
            else:
                return HttpResponse('Transaction failed.\nStatus: ' + str(
                    req.json()['data']['message']
                ))
        else:
            e_code = req.json()['errors']['code']
            e_message = req.json()['errors']['message']
            return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")
    else:
        return HttpResponse('Transaction failed or canceled by user')





def about(request):
    return render(request, 'base/pages/about.html')

def contact(request):
    return render(request, 'base/pages/contact.html')

def privacy_policy(request):
    return render(request, 'base/pages/privacy_policy.html')

def terms_conditions(request):
    return render(request, 'base/pages/terms_conditions.html')
