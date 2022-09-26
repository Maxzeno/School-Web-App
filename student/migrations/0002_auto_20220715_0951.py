# Generated by Django 3.2.13 on 2022-07-15 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='student_class',
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AddField(
            model_name='student',
            name='student_class_room',
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AlterField(
            model_name='student',
            name='student_id',
            field=models.CharField(max_length=100, primary_key=True, serialize=False, unique=True),
        ),
    ]
