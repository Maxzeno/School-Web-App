from django.shortcuts import render
from django.views import View

from .filter import *
from .modal import *
from utils import help as help_tools
from ...utils import DEFAULT_IMAGE_THE_URL


class StudentFeeManager(View):
	def get(self, request):
		the_classes = student_model.JustClass.objects.all()
		expense_categorys = semiadmin_model.ExpenseCategory.objects.all()
		return render(request, 'semiadmin/accounting/invoice.html', {'expense_categorys': expense_categorys, 
			'the_classes': the_classes, 'date_range': help_tools.date_range()})
		

class ExpenseCategory(View):
	def get(self, request):
		expense_categorys = semiadmin_model.ExpenseCategory.objects.all()
		return render(request, 'semiadmin/accounting/expense_category.html', {'expense_categorys': expense_categorys})
			

class ExpenseManager(View):
	def get(self, request):
		expense_categorys = semiadmin_model.ExpenseCategory.objects.all()
		return render(request, 'semiadmin/accounting/expense.html', {'expense_categorys': expense_categorys, 
			'date_range': help_tools.date_range()})
			
