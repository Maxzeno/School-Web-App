# Generated by Django 3.2.13 on 2022-09-16 01:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('semiadmin', '0049_remove_semiadmin_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='semiadmin',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='semiadmin', to=settings.AUTH_USER_MODEL),
        ),
    ]
