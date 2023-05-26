# Generated by Django 4.2 on 2023-04-08 17:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0008_meeting'),
    ]

    operations = [
        migrations.AddField(
            model_name='meeting',
            name='doctor',
            field=models.ForeignKey(default=1996, on_delete=django.db.models.deletion.CASCADE, to='doctors.doctor'),
            preserve_default=False,
        ),
    ]
