# Generated by Django 3.2.13 on 2022-08-08 12:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0021_alter_entrydetails_session'),
        ('semiadmin', '0018_mark'),
    ]

    operations = [
        migrations.AlterField(
            model_name='marksheetformat',
            name='session',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='student.session'),
        ),
    ]
