from django.shortcuts import render, redirect
from django.views import View

from .models import Contact as ContactModel
from management.models import User
from student.models import (
		Student, Siblings, EntryDetails, 
		Parent, Guardian, EmergencyContactDetail,
		PreviousSchoolDetail, HowDidYouHearAboutCDSSE
	)

# Create your views here.
# request.META.get('HTTP_REFERER')

class Index(View):
	def get(self, request):
		return render(request, 'main/index.html', {})


class Management(View):
	def get(self, request):
		return render(request, 'main/management.html', {})


class Gallery(View):
	def get(self, request):
		return render(request, 'main/gallery.html', {})


class Admissions(View):
	def get(self, request):
		return render(request, 'main/admissions.html', {})

	def post(self, request):
		data = dict(request.POST)
		data.pop('csrfmiddlewaretoken', None)
		data = {k: v[0] for k, v in data.items()}
		return render(request, 'main/admissions.html', {})


class Contact(View):
	def get(self, request):
		return render(request, 'main/contact.html', {'display':'none'})

	def post(self, request):
		data = dict(request.POST)
		data.pop('csrfmiddlewaretoken', None)
		data.pop('first_name', None)
		data.pop('app_source_id', None)
		data = {k: v[0] for k, v in data.items()}
		ContactModel.objects.create(**data)
		return render(request, 'main/contact.html', {'display':'block'})




