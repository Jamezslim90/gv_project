# Generated by Django 4.2.1 on 2023-05-24 13:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0005_chatroom_chat'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Chat',
        ),
        migrations.DeleteModel(
            name='ChatRoom',
        ),
    ]