# Generated by Django 3.2.13 on 2022-09-04 00:38

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0028_alter_exam_comment'),
        ('semiadmin', '0042_syllabus_the_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('the_date', models.DateField(blank=True, default=django.utils.timezone.now)),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='student.student')),
                ('the_class', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='student.class')),
            ],
        ),
    ]
