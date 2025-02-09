# Generated by Django 4.2 on 2024-08-16 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0011_remove_pharmacy_patient_remove_pharmacy_pharmacist_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='status',
            field=models.CharField(choices=[('Scheduled', 'Scheduled'), ('Completed', 'Completed'), ('Pending', 'Pending'), ('Cancelled', 'Cancelled')], max_length=120),
        ),
        migrations.AlterField(
            model_name='billing',
            name='status',
            field=models.CharField(choices=[('Paid', 'Paid'), ('Unpaid', 'Unpaid')], max_length=120),
        ),
    ]
