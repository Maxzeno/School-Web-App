# Generated by Django 3.2.13 on 2022-07-30 03:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('semiadmin', '0011_auto_20220730_0405'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='marksheetformat',
            name='check_mark_format',
        ),
        migrations.AlterUniqueTogether(
            name='marksheetformat',
            unique_together=set(),
        ),
    ]
