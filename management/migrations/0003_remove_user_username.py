# Generated by Django 3.2.13 on 2022-07-13 22:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0002_user_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='username',
        ),
    ]
