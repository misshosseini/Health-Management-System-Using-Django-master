# Generated by Django 4.2 on 2024-08-16 18:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0005_alter_notification_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notification',
            old_name='doctor',
            new_name='patient',
        ),
    ]
