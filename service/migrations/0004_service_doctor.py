# Generated by Django 4.1.7 on 2023-03-18 15:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0004_doctor_doctor_slug'),
        ('service', '0003_remove_fee_consultation'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='doctor',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='doctors.doctor'),
        ),
    ]