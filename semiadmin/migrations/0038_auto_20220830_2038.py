# Generated by Django 3.2.13 on 2022-08-30 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('semiadmin', '0037_studentdomainscore'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentdomainscore',
            name='subject_code',
        ),
        migrations.AddField(
            model_name='studentdomainscore',
            name='subject_code',
            field=models.ManyToManyField(null=True, to='semiadmin.PrincipalSubjectCode'),
        ),
    ]
