# Generated by Django 3.2.13 on 2022-08-08 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('semiadmin', '0021_mark_test30'),
    ]

    operations = [
        migrations.AddField(
            model_name='mark',
            name='comment',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
