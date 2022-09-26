# Generated by Django 3.2.13 on 2022-07-24 02:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('semiadmin', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ManagementTeam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=150)),
                ('gender', models.CharField(blank=True, max_length=150)),
                ('password', models.CharField(blank=True, max_length=150)),
                ('designation', models.CharField(blank=True, max_length=150)),
                ('department', models.CharField(blank=True, max_length=150)),
                ('email', models.CharField(blank=True, max_length=150)),
                ('phone', models.CharField(blank=True, max_length=150)),
                ('blood_group', models.CharField(blank=True, max_length=5)),
                ('facebook_link', models.TextField(blank=True, max_length=2000)),
                ('twitter_link', models.TextField(blank=True, max_length=2000)),
                ('linkedin_link', models.TextField(blank=True, max_length=2000)),
                ('address', models.TextField(blank=True, max_length=3000)),
                ('about', models.TextField(blank=True, max_length=3000)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('show_on_website', models.BooleanField(default=True)),
                ('left_school', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='MarkSheet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(blank=True, max_length=255)),
                ('format', models.CharField(blank=True, max_length=255)),
                ('session', models.CharField(blank=True, max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='schoolsettings',
            name='marksheet_format_entrys',
            field=models.ManyToManyField(blank=True, to='semiadmin.MarkSheet'),
        ),
    ]
