from django.db import models
from django.utils import timezone

from userauths import models as userauths_models

NOTIFICATION_TYPE = (
    ("New Appointment", "نوبت جدید"),
    ("Appointment Cancelled", "لغو نوبت"),
)

class Doctor(models.Model):
    user = models.OneToOneField(userauths_models.User, on_delete=models.CASCADE , verbose_name="کاربر")
    full_name = models.CharField(max_length=100, null=True, blank=True, verbose_name="نام کامل")
    image = models.FileField(upload_to="images", null=True, blank=True, verbose_name="تصویر")
    mobile = models.CharField(max_length=100, null=True, blank=True, verbose_name="موبایل")
    country = models.CharField(max_length=100, null=True, blank=True, verbose_name="کشور")
    bio = models.CharField(max_length=100, null=True, blank=True, verbose_name="بیوگرافی")
    specialization = models.CharField(max_length=100, null=True, blank=True, verbose_name="تخصص")
    qualifications = models.CharField(max_length=100, null=True, blank=True, verbose_name="مدارک")
    years_of_experience = models.CharField(max_length=100, null=True, blank=True, verbose_name="سال‌های تجربه")
    next_available_appointment_date = models.DateTimeField(default=timezone.now, null=True, blank=True, verbose_name="تاریخ بعدی نوبت موجود")

    class Meta:
        verbose_name_plural = "دکترها"

    def __str__(self):
        return f"دکتر  {self.full_name}"
    
class Notification(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="دکتر")
    appointment = models.ForeignKey("base.Appointment", on_delete=models.CASCADE, null=True, blank=True, related_name="doctor_appointment_notification")
    type = models.CharField(max_length=100, choices=NOTIFICATION_TYPE)
    seen = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "اعلان‌ها"
    
    def __str__(self):
        return f"اعلان دکتر  {self.doctor.full_name} "

