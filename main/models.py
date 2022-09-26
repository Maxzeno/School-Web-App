from django.db import models

# Create your models here.

class ImagePosition(models.Model):
	photo = models.FileField(upload_to='images/', blank=True, null=True)
	position = models.CharField(max_length=255, blank=True, choices=[('welcome', 'welcome'), ('under nav', 'under nav')])
	

class News(models.Model):
	photo = models.FileField(upload_to='images/', blank=True, null=True)
	subject = models.CharField(max_length=255, blank=True)
	description = models.TextField(max_length=1000, blank=True)
	

class Announcements(models.Model):
	photo = models.FileField(upload_to='images/', blank=True, null=True)
	subject = models.CharField(max_length=255, blank=True)
	description = models.TextField(max_length=1000, blank=True)
	

class HomePageSlider(models.Model):
	photo = models.FileField(upload_to='images/', blank=True, null=True)
	alt_text = models.CharField(max_length=150, blank=True)
	

class Testimonials(models.Model):
	name = models.CharField(max_length=255, blank=True)
	testimony = models.TextField(max_length=1000, blank=True)
	relationship_to_child = models.CharField(max_length=150, blank=True)


class Gallery(models.Model):
	photo = models.FileField(upload_to='images/', blank=True, null=True)
	description = models.TextField(max_length=1000, blank=True)
	

class Contact(models.Model):
	firstname = models.CharField(max_length=150, blank=True)
	lastname = models.CharField(max_length=150, blank=True)
	email = models.CharField(max_length=150, blank=True)
	phone_number = models.CharField(max_length=150, blank=True)
	subject = models.CharField(max_length=150, blank=True)
	message = models.TextField(max_length=1000, blank=True)
	is_resolved = models.BooleanField(default=False)
	is_attended_to = models.BooleanField(default=False)
