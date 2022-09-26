from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse

from student import models as student_model
from ... import models as semiadmin_model
from utils import help as help_tools




""" Noticeboard SECTION """

class NoticeboardCreateDate(View):
	def get(self, request, the_date):
		year, month, day = the_date.split('-')
		reform_date = f'{month}/{day}/{year}'
		html = render(request, 'semiadmin/back_office/modal/noticeboard.html', {'the_date': reform_date})
		return HttpResponse(html)


class NoticeboardCreate(View):
	def get(self, request):
		html = render(request, 'semiadmin/back_office/modal/noticeboard.html', {})
		return HttpResponse(html)

	def post(self, request):
		data = {
			'notice_title': request.POST.get('notice_title'),
			'the_date': help_tools.date_converter(request.POST.get('date')),
			'excerpts': request.POST.get('excerpts'),
			'notice': request.POST.get('notice'),
			'show_on_website': request.POST.get('show_on_website'),
			'notice_photo': request.FILES.get('notice_photo'),
		}

		new_data = {}
		for k in data:
			if data[k]:
				 new_data[k] = data[k]

		semiadmin_model.Noticeboard.objects.create(**new_data)
		return JsonResponse({"status": True, "notification": "Noticeboard Created Successfully"})


class NoticeboardEdit(View):
	def get(self, request, id):
		noticeboard = semiadmin_model.Noticeboard.objects.filter(pk=id).first()
		html = render(request, 'semiadmin/back_office/modal/noticeboard_edit.html', {'noticeboard': noticeboard})
		return HttpResponse(html)
	
	def post(self, request, id):
		data = {
			'notice_title': request.POST.get('notice_title'),
			'the_date': help_tools.date_converter(request.POST.get('date')),
			'excerpts': request.POST.get('excerpts'),
			'notice': request.POST.get('notice'),
			'show_on_website': request.POST.get('show_on_website'),
			'notice_photo': request.FILES.get('notice_photo'),
		}

		new_data = {}
		for k in data:
			if data[k]:
				 new_data[k] = data[k]

		semiadmin_model.Noticeboard.objects.filter(pk=id).update(**new_data)
		return JsonResponse({"status": True, "notification": "Noticeboard Updated Successfully"})


class NoticeboardDelete(View):
	def post(self, request, id):
		semiadmin_model.Noticeboard.objects.filter(pk=id).first().delete()
		return JsonResponse({"status": True, "notification": "Noticeboard Deleted Successfully"})

""" END Noticeboard SECTION """

""" Book Issue SECTION """

class BookIssueCreate(View):
	def get(self, request):
		the_classes = student_model.JustClass.objects.all()
		books = semiadmin_model.Book.objects.all()
		html = render(request, 'semiadmin/back_office/modal/book_issue.html', {'the_classes': the_classes, 'books': books})
		return HttpResponse(html)

	def post(self, request):
		def model_getter(model, field):
			field = request.POST.get(field)
			found = model.objects.filter(pk=field).first()
			return found

		just_class = student_model.JustClass.objects.filter(pk=request.POST.get('class_id')).first()
		the_class = student_model.Class.objects.filter(the_class=just_class).first()

		data = {
			'issue_date': help_tools.date_converter(request.POST.get('issue_date')),
			'student': model_getter(student_model.Student, 'student_id'),
			'book': model_getter(semiadmin_model.Book, 'book_id'),
			'the_class': the_class,
		}

		new_data = {}
		for k in data:
			if data[k]:
				 new_data[k] = data[k]

		semiadmin_model.BookIssue.objects.create(**new_data)
		return JsonResponse({"status": True, "notification": "Book issue Created Successfully"})


class BookIssueEdit(View):
	def get(self, request, id):
		book_issue = semiadmin_model.BookIssue.objects.filter(pk=id).first()
		books = semiadmin_model.Book.objects.all()

		def check_class():
			just_the_classes = student_model.JustClass.objects.all()
			new = []  # list of tuples
			found = None
			try:
				for just_class in just_the_classes:
					if just_class.pk == book_issue.the_class.the_class.pk:
						new.append((just_class.the_class, True))
						found = just_class

					else:
						new.append((just_class.the_class, False))
				return new, found
			except:
				return [('', False)], found

		try:
			classes, the_specific_class = check_class()
			new_students = [] # list containing tuple of shape(1, 2)
			the_classes = student_model.Class.objects.filter(the_class=the_specific_class).all()
			for the_class in the_classes:
				students = student_model.Student.objects.filter(student_class_room=the_class.pk).values_list('pk', 'name')
				for student in students:
					if book_issue.student.pk == student[0]:
						new_students.append([*student, True])
					else:
						new_students.append([*student, False])
		except:
			new_students = [('', '', False)]


		html = render(request, 'semiadmin/back_office/modal/book_issue_edit.html', {'book_issue': book_issue, 'books': books,
		 'classes': classes, 'students': new_students})
		return HttpResponse(html)

	def post(self, request, id):
		def model_getter(model, field):
			field = request.POST.get(field)
			found = model.objects.filter(pk=field).first()
			return found

		just_class = student_model.JustClass.objects.filter(pk=request.POST.get('class_id')).first()
		the_class = student_model.Class.objects.filter(the_class=just_class).first()
		data = {
			'issue_date': help_tools.date_converter(request.POST.get('issue_date')),
			'student': model_getter(student_model.Student, 'student_id'),
			'book': model_getter(semiadmin_model.Book, 'book_id'),
			'the_class': the_class,
		}

		new_data = {}
		for k in data:
			if data[k]:
				 new_data[k] = data[k]

		semiadmin_model.BookIssue.objects.filter(pk=id).update(**new_data)
		return JsonResponse({"status": True, "notification": "Book issue Updated Successfully"})


class BookIssueDelete(View):
	def post(self, request, id):
		semiadmin_model.BookIssue.objects.filter(pk=id).first().delete()
		return JsonResponse({"status": True, "notification": "Book issue Deleted Successfully"})

""" END Book SECTION """




""" Book SECTION """

class BookCreate(View):
	def get(self, request):
		html = render(request, 'semiadmin/back_office/modal/book.html', {})
		return HttpResponse(html)

	def post(self, request):
		data = {
			'book_name':request.POST.get('name'),
			'author':request.POST.get('author'),
			'number_of_copy':request.POST.get('copies'),
		}

		new_data = {}
		for k in data:
			if data[k]:
				 new_data[k] = data[k]

		semiadmin_model.Book.objects.create(**new_data)
		return JsonResponse({"status": True, "notification": "Book Created Successfully"})


class BookEdit(View):
	def get(self, request, id):
		book = semiadmin_model.Book.objects.filter(pk=id).first()
		html = render(request, 'semiadmin/back_office/modal/book_edit.html', {'book': book})
		return HttpResponse(html)

	def post(self, request, id):
		data = {
			'book_name':request.POST.get('name'),
			'author':request.POST.get('author'),
			'number_of_copy':request.POST.get('copies'),
		}

		new_data = {}
		for k in data:
			if data[k]:
				 new_data[k] = data[k]

		semiadmin_model.Book.objects.filter(pk=id).update(**new_data)
		return JsonResponse({"status": True, "notification": "Book Updated Successfully"})


class BookDelete(View):
	def post(self, request, id):
		semiadmin_model.Book.objects.filter(pk=id).first().delete()
		return JsonResponse({"status": True, "notification": "Book Deleted Successfully"})

""" END Book SECTION """

