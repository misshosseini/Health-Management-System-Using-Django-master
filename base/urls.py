from django.urls import path
from base import views

app_name = "base"

urlpatterns = [
    path("", views.index, name="index"),
    path("service/<service_id>/", views.service_detail, name="service_detail"),
    path("book-appointment/<service_id>/<doctor_id>/", views.book_appointment, name="book_appointment"),
    path("checkout/<int:billing_id>/", views.checkout, name="checkout"),


    #zarinpal
    path('request/', views.send_request, name='request'),
    path('verify/', views.verify, name='verify'),


    path('pages/about.html', views.about, name='about'),
    path('pages/contact.html', views.contact, name='contact'),
    path('pages/privacy_policy.html', views.privacy_policy, name='privacy_policy'),
    path('pages/terms_conditions.html', views.terms_conditions, name='terms_conditions'),

]