# Generated by Django 4.2 on 2023-04-08 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0010_alter_meeting_options_remove_meeting_date_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meeting',
            name='date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='time',
            field=models.TimeField(),
        ),
    ]
