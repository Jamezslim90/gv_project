# Generated by Django 4.2 on 2023-04-08 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0007_bankaccount'),
    ]

    operations = [
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(max_length=200)),
                ('date_time', models.DateTimeField()),
                ('passcode', models.CharField(max_length=10)),
                ('customer_email', models.EmailField(max_length=254)),
                ('doctor_email', models.EmailField(max_length=254)),
                ('duration', models.IntegerField()),
                ('timezone', models.CharField(max_length=50)),
                ('zoom_id', models.CharField(max_length=50)),
            ],
            options={
                'ordering': ('-date_time',),
            },
        ),
    ]