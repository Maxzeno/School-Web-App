# Generated by Django 3.2.13 on 2022-07-13 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SchoolSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school_name', models.CharField(blank=True, max_length=255)),
                ('phone', models.CharField(blank=True, max_length=150)),
                ('address', models.TextField(blank=True, max_length=2000)),
            ],
        ),
        migrations.CreateModel(
            name='SemiAdmin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('passport_photo', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('name', models.CharField(blank=True, max_length=150)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('place_of_birth', models.CharField(blank=True, max_length=150)),
                ('nationality', models.CharField(blank=True, max_length=150)),
                ('gender', models.CharField(blank=True, max_length=150)),
                ('religion', models.CharField(blank=True, max_length=150)),
            ],
        ),
    ]
