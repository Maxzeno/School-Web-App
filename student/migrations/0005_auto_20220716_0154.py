# Generated by Django 3.2.13 on 2022-07-16 00:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0004_auto_20220716_0151'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='address',
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AddField(
            model_name='student',
            name='blood_group',
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AddField(
            model_name='student',
            name='phone',
            field=models.CharField(blank=True, max_length=150),
        ),
    ]
