from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse
from django.db.models import Q

from student import models as student_model
from ... import models as semiadmin_model
from utils.html import HTML
from utils import help as help_tools
from datetime import datetime



""" Invoice SECTION """

class InvoiceCreate(View):
	def get(self, request):
		the_classes = student_model.JustClass.objects.all()
		
		if 'mass' in request.path:
			html = render(request, 'semiadmin/accounting/modal/invoice_mass.html', {'the_classes': the_classes})
		else:
			html = render(request, 'semiadmin/accounting/modal/invoice_single.html', {'the_classes': the_classes})
		return HttpResponse(html)

	def post(self, request):
		data = {
			'invoice_title': request.POST.get('title'),
			'total_amount': int(request.POST.get('total_amount')),
			'paid_amount': int(request.POST.get('paid_amount')),
			'status': request.POST.get('status'),
		}

		class_id = request.POST.get('class_id')
		section_id = request.POST.get('section_id')
		exact_class = student_model.Class.objects.filter(the_class=class_id, the_section=section_id).first()

		if exact_class:
			data['the_class'] = exact_class

		if 'single' in request.path:
			student_id = request.POST.get('student_id')
			exact_student = student_model.Student.objects.filter(pk=student_id).first()

			if exact_student:
				data['student'] = exact_student

		new_data = {}
		for k in data:
			if data[k] != '':
				 new_data[k] = data[k]

		semiadmin_model.Invoice.objects.create(**new_data)
		return JsonResponse({"status": True, "notification": "Invoice Created Successfully"})


class InvoiceEdit(View):
	def get(self, request, id):
		the_classes = student_model.JustClass.objects.all()
		invoice = semiadmin_model.Invoice.objects.filter(pk=id).first()
		the_sections = student_model.Class.objects.filter(the_class=invoice.the_class.the_class.the_class).all()
		exact_class = student_model.Class.objects.filter(the_class=invoice.the_class.the_class.the_class, 
			the_section=invoice.the_class.the_section).first()

		students = student_model.Student.objects.filter(student_class_room=exact_class).all()

		if 'mass' in request.path:
			html = render(request, 'semiadmin/accounting/modal/invoice_mass_edit.html', {'invoice': invoice, 
				'the_sections': the_sections, 'the_classes': the_classes})
		else:
			html = render(request, 'semiadmin/accounting/modal/invoice_single_edit.html', {'invoice': invoice, 
				'the_sections': the_sections, 'the_classes': the_classes,
				'students': students})
		return HttpResponse(html)

	def post(self, request, id):
		data = {
			'invoice_title': request.POST.get('title'),
			'total_amount': int(request.POST.get('total_amount')),
			'paid_amount': int(request.POST.get('paid_amount')),
			'status': request.POST.get('status'),
		}

		class_id = request.POST.get('class_id')
		section_id = request.POST.get('section_id')
		exact_class = student_model.Class.objects.filter(the_class=class_id, the_section=section_id).first()

		if exact_class:
			data['the_class'] = exact_class

		if 'single' in request.path:
			student_id = request.POST.get('student_id')
			exact_student = student_model.Student.objects.filter(pk=student_id).first()

			if exact_student:
				data['student'] = exact_student

		new_data = {}
		for k in data:
			if data[k] != '':
				 new_data[k] = data[k]

		semiadmin_model.Invoice.objects.filter(pk=id).update(**new_data)
		return JsonResponse({"status": True, "notification": "Invoice Updated Successfully"})


class InvoiceDelete(View):
	def post(self, request, id):
		semiadmin_model.Invoice.objects.filter(pk=id).first().delete()
		return JsonResponse({"status": True, "notification": "Invoice Deleted Successfully"})

""" END Invoice SECTION """


""" Expense SECTION """

class ExpenseCreate(View):
	def get(self, request):
		expense_categorys = semiadmin_model.ExpenseCategory.objects.all()
		html = render(request, 'semiadmin/accounting/modal/expense.html', {'expense_categorys': expense_categorys})
		return HttpResponse(html)

	def post(self, request):
		data = {
			'the_date': datetime.strptime(request.POST.get('date').strip(), '%m/%d/%Y'),
			'amount': int(request.POST.get('amount')),
		}

		expense_category_id = request.POST.get('expense_category_id')
		expense_category = semiadmin_model.ExpenseCategory.objects.filter(pk=expense_category_id).first()

		if expense_category:
			data['expense_category'] = expense_category

		new_data = {}
		for k in data:
			if data[k] != '':
				 new_data[k] = data[k]

		semiadmin_model.Expense.objects.create(**new_data)
		return JsonResponse({"status": True, "notification": "Expense Created Successfully"})


class ExpenseEdit(View):
	def get(self, request, id):
		expense_categorys = semiadmin_model.ExpenseCategory.objects.all()
		expense = semiadmin_model.Expense.objects.filter(pk=id).first()
		html = render(request, 'semiadmin/accounting/modal/expense_edit.html', {'expense': expense, 'expense_categorys': expense_categorys})
		return HttpResponse(html)

	def post(self, request, id):
		data = {
			'the_date': datetime.strptime(request.POST.get('date').strip(), '%m/%d/%Y'),
			'amount': int(request.POST.get('amount')),
		}

		expense_category_id = request.POST.get('expense_category_id')
		expense_category = semiadmin_model.ExpenseCategory.objects.filter(pk=expense_category_id).first()

		if expense_category:
			data['expense_category'] = expense_category

		new_data = {}
		for k in data:
			if data[k] != '':
				 new_data[k] = data[k]

		semiadmin_model.Expense.objects.filter(pk=id).update(**new_data)
		return JsonResponse({"status": True, "notification": "Expense Updated Successfully"})


class ExpenseDelete(View):
	def post(self, request, id):
		semiadmin_model.Expense.objects.filter(pk=id).first().delete()
		return JsonResponse({"status": True, "notification": "Expense Deleted Successfully"})

""" END Expense SECTION """


""" ExpenseCategory SECTION """

class ExpenseCategoryCreate(View):
	def get(self, request):
		html = render(request, 'semiadmin/accounting/modal/expense_category.html', {})
		return HttpResponse(html)

	def post(self, request):
		data = {
			'name':request.POST.get('name'),
		}

		new_data = {}
		for k in data:
			if data[k] != '':
				 new_data[k] = data[k]

		semiadmin_model.ExpenseCategory.objects.create(**new_data)
		return JsonResponse({"status": True, "notification": "Expense category Created Successfully"})


class ExpenseCategoryEdit(View):
	def get(self, request, id):
		expense_category = semiadmin_model.ExpenseCategory.objects.filter(pk=id).first()
		html = render(request, 'semiadmin/accounting/modal/expense_category_edit.html', {'expense_category': expense_category})
		return HttpResponse(html)

	def post(self, request, id):
		data = {
			'name':request.POST.get('name'),
		}

		new_data = {}
		for k in data:
			if data[k] != '':
				 new_data[k] = data[k]

		semiadmin_model.ExpenseCategory.objects.filter(pk=id).update(**new_data)
		return JsonResponse({"status": True, "notification": "Expense category Updated Successfully"})


class ExpenseCategoryDelete(View):
	def post(self, request, id):
		semiadmin_model.ExpenseCategory.objects.filter(pk=id).first().delete()
		return JsonResponse({"status": True, "notification": "Expense category Deleted Successfully"})

""" END ExpenseCategory SECTION """

