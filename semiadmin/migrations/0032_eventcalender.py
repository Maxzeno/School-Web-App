# Generated by Django 3.2.13 on 2022-08-15 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('semiadmin', '0031_invoice_the_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventCalender',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255)),
                ('starting_date', models.DateField(auto_now_add=True)),
                ('ending_date', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
