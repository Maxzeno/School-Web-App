# Generated by Django 3.2.13 on 2022-07-16 03:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0006_auto_20220716_0202'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='password',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
