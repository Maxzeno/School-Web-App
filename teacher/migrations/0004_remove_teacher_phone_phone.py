# Generated by Django 3.2.13 on 2022-07-24 02:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0003_auto_20220718_0143'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teacher',
            name='phone_phone',
        ),
    ]
