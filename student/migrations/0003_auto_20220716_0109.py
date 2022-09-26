# Generated by Django 3.2.13 on 2022-07-16 00:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0002_auto_20220715_0951'),
    ]

    operations = [
        migrations.CreateModel(
            name='Parent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=150)),
                ('name', models.CharField(blank=True, max_length=150)),
                ('gender', models.CharField(blank=True, max_length=150)),
                ('state_of_origin', models.CharField(blank=True, max_length=150)),
                ('birth_day', models.CharField(blank=True, max_length=150)),
                ('birth_month', models.CharField(blank=True, max_length=150)),
                ('mobile_phone', models.CharField(blank=True, max_length=150)),
                ('occupation', models.CharField(blank=True, max_length=150)),
                ('office_phone', models.CharField(blank=True, max_length=150)),
                ('full_postal_address', models.CharField(blank=True, max_length=150)),
                ('email_address', models.CharField(blank=True, max_length=150)),
                ('business_address', models.CharField(blank=True, max_length=150)),
                ('blood_group', models.CharField(blank=True, max_length=150)),
            ],
        ),
        migrations.AlterField(
            model_name='student',
            name='father',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='father', to='student.parent'),
        ),
        migrations.AlterField(
            model_name='student',
            name='mother',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mother', to='student.parent'),
        ),
        migrations.DeleteModel(
            name='Father',
        ),
        migrations.DeleteModel(
            name='Mother',
        ),
    ]
