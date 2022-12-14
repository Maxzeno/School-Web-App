# Generated by Django 3.2.13 on 2022-07-16 03:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0007_student_password'),
    ]

    operations = [
        migrations.RenameField(
            model_name='parent',
            old_name='full_postal_address',
            new_name='address',
        ),
        migrations.RenameField(
            model_name='parent',
            old_name='mobile_phone',
            new_name='phone',
        ),
        migrations.RemoveField(
            model_name='student',
            name='password',
        ),
        migrations.AddField(
            model_name='parent',
            name='password',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
