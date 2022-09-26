from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from ... import models as semiadmin_model
from student import models as student_model
from datetime import date
from utils import help as help_tool


class SchoolSettings(View):
	def get(self, request):
		school_setting = semiadmin_model.SchoolSettings.objects.last()
		return render(request, 'semiadmin/settings/school_settings.html', {'school_setting':school_setting,
		 'sessions':help_tool.sessioner()})
		
	def post(self, request):
		school_name = request.POST.get("school_name")
		phone = request.POST.get("phone")
		address = request.POST.get("address")
		category = request.POST.getlist("category[]")
		mark_format = request.POST.getlist("mark_format[]")
		session_years = request.POST.getlist("session[]")

		def sesser(ses):
			try:
				left = ses.split('-')[0]
				right = ses.split('-')[1]
			except:
				return False
			else:
				if left.isdigit() and right.isdigit():
					return True
				return False

		session = []
		for ses in session_years:
			if sesser(ses):
				ses_found = student_model.Session.objects.filter(session=ses).first()

				if ses_found:
					session.append(ses_found)
				else:
					ses_create = student_model.Session.objects.create(session=ses)
					session.append(ses_create)
			else:
				session.append(None)



		school_setting = semiadmin_model.SchoolSettings.objects.first()
		if school_setting:
			school_setting.school_name = school_name
			school_setting.phone = phone
			school_setting.address = address
			school_setting.save()
		else:
			school_setting = semiadmin_model.SchoolSettings.objects.create(school_name=school_name, phone=phone, address=address)


		marksheet_format_entrys = school_setting.marksheet_format_entrys.all()
		length = len(marksheet_format_entrys)
		length_update = len(category)


		if marksheet_format_entrys and length <= length_update:
			for i in range(length_update):
				if length > i:
					if not category[i] and not mark_format[i] and not session[i] :
						continue
					marksheet_format_entrys[i].category = category[i]
					marksheet_format_entrys[i].mark_format = mark_format[i]
					if session[i]:
						marksheet_format_entrys[i].session = session[i]
					marksheet_format_entrys[i].save()


				else:
					if not category[i] and not mark_format[i] and not session[i] :
						continue
					if not session[i]:
						school_setting.marksheet_format_entrys.create(category=category[i], mark_format=mark_format[i])
					else:
						school_setting.marksheet_format_entrys.create(category=category[i], mark_format=mark_format[i], session=session[i])

		elif marksheet_format_entrys and length > length_update:
			for i in range(length):
				if length_update > i:
					if not category[i] and not mark_format[i] and not session[i] :
						continue
					marksheet_format_entrys[i].category = category[i]
					marksheet_format_entrys[i].mark_format = mark_format[i]
					if session[i]:
						marksheet_format_entrys[i].session = session[i]
					marksheet_format_entrys[i].save()
				else:
					marksheet_format_entrys[i].delete()


		else:
			for i in range(len(category)):
				if not category[i] and not mark_format[i] and not session[i] :
						continue
				if not session[i]:
					school_setting.marksheet_format_entrys.create(category=category[i], mark_format=mark_format[i])
				else:
					school_setting.marksheet_format_entrys.create(category=category[i], mark_format=mark_format[i], session=session[i])

		return JsonResponse({"status": True, "notification": "Setting updated successfully"})