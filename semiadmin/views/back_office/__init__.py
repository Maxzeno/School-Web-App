from django.shortcuts import render
from django.views import View

from .filter import *
from .modal import *
from utils import help as help_tools


class Book(View):
	def get(self, request):
		books = semiadmin_model.Book.objects.all()
		return render(request, 'semiadmin/back_office/book.html', {'books': books})
	

class BookIssue(View):
	def get(self, request):
		return render(request, 'semiadmin/back_office/book_issue.html', {'date_range': help_tools.date_range()})
		

class Noticeboard(View):
	def get(self, request):
		return render(request, 'semiadmin/back_office/noticeboard.html', {})
			
