# Generated by Django 3.2.13 on 2022-08-08 10:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0020_alter_passmark_subject'),
        ('semiadmin', '0017_rename_subject_code_principalsubjectcode_subject_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resumption_test10', models.FloatField(blank=True)),
                ('resumption_test15', models.FloatField(blank=True)),
                ('mid_test10', models.FloatField(blank=True)),
                ('mid_test15', models.FloatField(blank=True)),
                ('project10', models.FloatField(blank=True)),
                ('assignment10', models.FloatField(blank=True)),
                ('exam70', models.FloatField(blank=True)),
                ('exam60', models.FloatField(blank=True)),
                ('exam', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='student.exam')),
                ('mark_sheet_format', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='semiadmin.marksheetformat')),
                ('student', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='student.student')),
                ('subject', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='student.subject')),
                ('the_class', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='student.class')),
            ],
        ),
    ]
