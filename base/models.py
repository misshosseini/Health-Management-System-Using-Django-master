from django.db import models

from shortuuid.django_fields import ShortUUIDField

from doctor import models as doctor_models
from patient import models as patient_models

class Service(models.Model):
    image = models.FileField(upload_to="images", null=True, blank=True, verbose_name="تصویر")
    name = models.CharField(max_length=255, verbose_name="نام")
    description = models.TextField(blank=True, null=True, verbose_name="توضیحات")
    cost = models.DecimalField(max_digits=16, decimal_places=3, verbose_name="هزینه")
    available_doctors = models.ManyToManyField(doctor_models.Doctor, blank=True, verbose_name="دکترهای موجود")

    class Meta:
        verbose_name_plural = "خدمات"

    def __str__(self):
        return f"{self.name} - {self.cost}"
    


class Appointment(models.Model):
    STATUS = [
        ('Scheduled', 'برنامه‌ریزی شده'), 
        ('Completed', 'تکمیل شده'), 
        ('Pending', 'در انتظار'), 
        ('Cancelled', 'لغو شده')
    ]
    
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True, related_name='service_appointments', verbose_name="خدمت")
    doctor = models.ForeignKey(doctor_models.Doctor, on_delete=models.SET_NULL, null=True, blank=True, related_name='doctor_appointments', verbose_name="قرار ملاقات دکتر")
    patient = models.ForeignKey(patient_models.Patient, on_delete=models.SET_NULL, null=True, blank=True, related_name='appointments_patient' , verbose_name="قرار ملاقات بیمار")
    appointment_date = models.DateTimeField(null=True, blank=True, verbose_name="تاریخ نوبت")
    issues = models.TextField(blank=True, null=True, verbose_name="مشکلات")
    symptoms = models.TextField(blank=True, null=True, verbose_name="علائم")
    appointment_id = ShortUUIDField(length=6, max_length=10, alphabet="1234567890", verbose_name="شناسه نوبت")
    status = models.CharField(max_length=120, choices=STATUS, verbose_name="وضعیت")

    class Meta:
        verbose_name_plural = "نوبت‌ها"

    def __str__(self):
        return f"{self.patient.full_name}با  {self.doctor.full_name}"
    


class MedicalRecord(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, verbose_name="نوبت")
    diagnosis = models.TextField(verbose_name="تشخیص")
    treatment = models.TextField(verbose_name="درمان")

    class Meta:
        verbose_name_plural = "پرونده‌های پزشکی"

    def __str__(self):
        return f"پرونده پزشکی برای  {self.appointment.patient.full_name}"


class LabTest(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, verbose_name="نوبت")
    test_name = models.CharField(max_length=255, verbose_name="نام آزمایش")
    description = models.TextField(blank=True, null=True, verbose_name="توضیحات")
    result = models.TextField(blank=True, null=True, verbose_name="نتیجه")

    class Meta: 
        verbose_name_plural = "آزمایشات"

    def __str__(self):
        return f"{self.test_name}"


class Prescription(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, verbose_name="نوبت")
    medications = models.TextField(blank=True, null=True, verbose_name="داروها")

    class Meta:
        verbose_name_plural = "نسخه"

    def __str__(self):
        return f"نسخه برای  {self.appointment.patient.full_name}"
    

class Billing(models.Model):
    patient = models.ForeignKey(patient_models.Patient, on_delete=models.SET_NULL, null=True, blank=True,  related_name='billings', verbose_name="صورت حساب ها" )
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='billing', blank=True, null=True, verbose_name="نوبت")
    sub_total = models.DecimalField(max_digits=10, decimal_places=3 ,verbose_name="زیر مجموع")
    tax = models.DecimalField(max_digits=10, decimal_places=3 , verbose_name="مالیات")
    total = models.DecimalField(max_digits=10, decimal_places=3, verbose_name="مجموع")
    status = models.CharField(max_length=120, choices=[('Paid', 'پرداخت شده'), ('Unpaid', 'پرداخت نشده')], verbose_name="وضعیت")
    billing_id = ShortUUIDField(length=6, max_length=10, alphabet="1234567890", verbose_name="شناسه صورتحساب")

    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "صورتحساب‌ها"

    def __str__(self):
        return f"صورتحساب برای  {self.patient.full_name} - مجموع: {self.total}"

