from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse
from django.db.models import Q

from student import models as student_model
from ... import models as semiadmin_model
from utils.html import HTML
from utils import help as help_tools

class NoticeboardCalendarEvent(View):
	def get(self, request):
		events = semiadmin_model.Noticeboard.objects.all()
		json = [{'id': data.pk, 'notice_title': data.notice_title, 'date': data.the_date} for data in events]
		return JsonResponse(json, safe=False)


class NoticeboardAll(View):
	def get(self, request):
		html = render(request, 'semiadmin/back_office/filter/noticeboard.html', {})
		return HttpResponse(html)


class ClassStudent(View):
	def get(self, request, class_id):
		new_students = []
		just_class = student_model.JustClass.objects.filter(the_class=class_id).first()
		the_classes = student_model.Class.objects.filter(the_class=just_class).all()
		for the_class in the_classes:
			students = student_model.Student.objects.filter(student_class_room=the_class.pk).values_list('pk', 'name')
			new_students += students

		html = HTML()
		select = html.select(name="section", id="section_id", klass="form-control select2 select2-hidden-accessible", data_toggle="select2", required="", data_select2_id="section_id", tabindex="-1", aria_hidden="true")
		for student in new_students:
			select.option(student[1].upper(), value=student[0], data_select2_id=student[1].upper())
		return HttpResponse(html)


class BookIssueFilter(View):
	def get(self, request):
		the_date = request.GET.get('date')
		less, great = help_tools.date_range_from_string(the_date)

		tbodys = semiadmin_model.BookIssue.objects.filter(Q(issue_date__gte=less) & Q(issue_date__lte=great)).all()
		html = render(request, 'semiadmin/back_office/filter/book_issue.html', {'book_issues': tbodys})
		return HttpResponse(html)


class BookAll(View):
	def get(self, request):
		tbodys = semiadmin_model.Book.objects.all()
		html = render(request, 'semiadmin/back_office/filter/book.html', {'books': tbodys})
		return HttpResponse(html)

