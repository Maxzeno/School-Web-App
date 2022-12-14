# Generated by Django 3.2.13 on 2022-08-03 19:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0017_session'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exam',
            name='exam_session',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='student.session'),
        ),
        migrations.AlterField(
            model_name='passmark',
            name='session',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='student.session'),
        ),
    ]
