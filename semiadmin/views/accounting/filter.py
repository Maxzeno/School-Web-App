from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse
from django.db.models import Q

from student import models as student_model
from ... import models as semiadmin_model
from utils.html import HTML
from utils import help as help_tools


class ClassSectionStudent(View):
	def get(self, request, class_id, section_id):
		just_class = student_model.JustClass.objects.filter(the_class=class_id).first()
		exact_class = student_model.Class.objects.filter(the_class=just_class, the_section=section_id).first()
		students = student_model.Student.objects.filter(student_class_room=exact_class.pk).values_list('pk', 'name')

		html = HTML()
		select = html.select(name="section", id="section_id", klass="form-control select2 select2-hidden-accessible", data_toggle="select2", required="", data_select2_id="section_id", tabindex="-1", aria_hidden="true")
		for student in students:
			select.option(student[1].upper(), value=student[0], data_select2_id=student[1].upper())
		return HttpResponse(html)



class InvoiceFilter(View):
	def get(self, request):
		selected_class = request.GET.get('selectedClass')
		section_id = request.GET.get('selectedSection')

		if section_id.lower() == 'all':
			just_class = student_model.JustClass.objects.filter(the_class=selected_class).first()
			class_ids = student_model.Class.objects.filter(the_class=just_class).all()
			status = request.GET.get('selectedStatus')
			the_date = request.GET.get('date')
			new_tbodys = []
			for class_id in class_ids:
				less, great = help_tools.date_range_from_string(the_date)
				if selected_class.lower() == 'all' and status.lower() == 'all':
					tbodys = semiadmin_model.Invoice.objects.filter(\
						Q(the_date__gte=less) & Q(the_date__lte=great)).all()

				elif selected_class.lower() == 'all':
					tbodys = semiadmin_model.Invoice.objects.filter(\
						Q(status=status) & Q(the_date__gte=less) & Q(the_date__lte=great)).all()

				elif status.lower() == 'all':
					tbodys = semiadmin_model.Invoice.objects.filter(\
						Q(the_class=class_id) & Q(the_date__gte=less) & Q(the_date__lte=great)).all()
				else:
					tbodys = semiadmin_model.Invoice.objects.filter(\
						Q(the_class=class_id) & Q(status=status) & Q(the_date__gte=less) & Q(the_date__lte=great)).all()
				new_tbodys.extend(tbodys)
				print(new_tbodys)
			html = render(request, 'semiadmin/accounting/filter/invoice.html', {'invoices': new_tbodys})
			return HttpResponse(html)

		else:
			try:
				just_class = student_model.JustClass.objects.filter(the_class=selected_class).first()
				class_id = student_model.Class.objects.filter(the_class=just_class, the_section=section_id).first()
			except:
				just_class = ''
				class_id = ''
			status = request.GET.get('selectedStatus')
			the_date = request.GET.get('date')

			less, great = help_tools.date_range_from_string(the_date)
			if selected_class.lower() == 'all' and status.lower() == 'all':
				tbodys = semiadmin_model.Invoice.objects.filter(\
					Q(the_date__gte=less) & Q(the_date__lte=great)).all()

			elif selected_class.lower() == 'all':
				tbodys = semiadmin_model.Invoice.objects.filter(\
					Q(status=status) & Q(the_date__gte=less) & Q(the_date__lte=great)).all()

			elif status.lower() == 'all':
				tbodys = semiadmin_model.Invoice.objects.filter(\
					Q(the_class=class_id) & Q(the_date__gte=less) & Q(the_date__lte=great)).all()
			else:
				tbodys = semiadmin_model.Invoice.objects.filter(\
					Q(the_class=class_id) & Q(status=status) & Q(the_date__gte=less) & Q(the_date__lte=great)).all()
			html = render(request, 'semiadmin/accounting/filter/invoice.html', {'invoices': tbodys})
			return HttpResponse(html)


class ExpenseFilter(View):
	def get(self, request):
		expense_category_id = request.GET.get('expense_category_id')
		the_date = request.GET.get('date')

		less, great = help_tools.date_range_from_string(the_date)
		if expense_category_id.lower() == 'all':
			tbodys = semiadmin_model.Expense.objects.filter(\
				Q(the_date__gte=less) & Q(the_date__lte=great)).all()
		else:
			tbodys = semiadmin_model.Expense.objects.filter(\
				Q(expense_category=expense_category_id) & Q(the_date__gte=less) & Q(the_date__lte=great)).all()
		html = render(request, 'semiadmin/accounting/filter/expense.html', {'expenses': tbodys})
		return HttpResponse(html)


class ExpenseCategoryAll(View):
	def get(self, request):
		tbodys = semiadmin_model.ExpenseCategory.objects.all()
		html = render(request, 'semiadmin/accounting/filter/expense_category.html', {'expense_categorys': tbodys})
		return HttpResponse(html)


