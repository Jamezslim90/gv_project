# Generated by Django 4.1.7 on 2023-03-23 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0003_animal_last_vaccination_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='Symptoms',
            field=models.ManyToManyField(blank=True, to='clients.symptom'),
        ),
    ]
