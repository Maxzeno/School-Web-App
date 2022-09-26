from django.shortcuts import render
from django.views import View

from semiadmin import models as semiadmin_model


class Book(View):
	def get(self, request):
		books = semiadmin_model.Book.objects.all()
		return render(request, 'teacher/back_office/book.html', {'books': books})
	
