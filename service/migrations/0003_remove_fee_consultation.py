# Generated by Django 4.1.7 on 2023-03-03 05:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0002_alter_fee_fee'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fee',
            name='consultation',
        ),
    ]