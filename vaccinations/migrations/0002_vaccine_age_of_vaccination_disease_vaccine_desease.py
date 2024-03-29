# Generated by Django 4.1.7 on 2023-03-23 14:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0004_appointment_symptoms'),
        ('vaccinations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vaccine',
            name='age_of_vaccination',
            field=models.IntegerField(default=6),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Disease',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, null=True)),
                ('animal_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clients.animaltype')),
                ('symptoms', models.ManyToManyField(blank=True, to='clients.symptom')),
            ],
        ),
        migrations.AddField(
            model_name='vaccine',
            name='desease',
            field=models.ManyToManyField(blank=True, to='vaccinations.disease'),
        ),
    ]
