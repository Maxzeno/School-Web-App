from django.db import models
from student.models import Class, Subject
from management.models import User

# Create your models here.

class Department(models.Model):
	name = models.CharField(max_length=150, blank=True, unique=True)
	
	def __str__(self):
		return self.name

class Teacher(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='teacher')
	name = models.CharField(max_length=150, blank=True)
	gender = models.CharField(max_length=150, blank=True)
	designation = models.CharField(max_length=150, blank=True)
	department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True) ## laboratory, administration, teaching, bursary, etc
	phone = models.CharField(max_length=150, blank=True)
	blood_group = models.CharField(max_length=5, blank=True)
	facebook_link = models.TextField(max_length=2000, blank=True)
	twitter_link = models.TextField(max_length=2000, blank=True)
	linkedin_link = models.TextField(max_length=2000, blank=True)
	address = models.TextField(max_length=3000, blank=True)
	about = models.TextField(max_length=3000, blank=True)
	image = models.ImageField(upload_to='images/', blank=True, null=True)
	show_on_website = models.BooleanField(default=True)
	left_school = models.BooleanField(default=False)
	# subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True, blank=True)
	management_team = models.BooleanField(default=False)

	def __str__(self):
		return self.name

	# def get_photo(self):
	# 	"""should reture student passport or placeholder image"""
	# 	if hasattr(self.image, 'url'):
	# 		return self.image.url
	# 	return '/static/portal/uploads/users/placeholder.jpg'



class FormTeacher(models.Model):
	teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
	form_teacher_of = models.ManyToManyField(Class, blank=True)
	# form_teacher_of = models.ForeignKey(Class, on_delete=models.CASCADE, null=True, blank=True) # to be added
	

class Staff(models.Model):
	name = models.CharField(max_length=150, blank=True)
	gender = models.CharField(max_length=150, blank=True)
	phone = models.CharField(max_length=150, blank=True)
	address = models.TextField(max_length=3000, blank=True)
	image = models.ImageField(upload_to='images/', blank=True, null=True)


