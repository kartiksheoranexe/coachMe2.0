# Generated by Django 4.1.3 on 2022-11-27 17:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coachMe', '0019_room_message'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='user',
        ),
    ]
