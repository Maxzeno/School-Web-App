from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import REDIRECT_FIELD_NAME

from shortuuid import ShortUUID
# from management.models import User


def teacher_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
	actual_decorator = user_passes_test(
		lambda u: u.is_authenticated and u.is_teacher is True,
		login_url=login_url,
		redirect_field_name=redirect_field_name
	)
	if function:
		return actual_decorator(function)
	return actual_decorator


def student_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
	actual_decorator = user_passes_test(
		lambda u: u.is_authenticated and u.is_student is True,
		login_url=login_url,
		redirect_field_name=redirect_field_name
	)
	if function:
		return actual_decorator(function)
	return actual_decorator


def semiadmin_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
	actual_decorator = user_passes_test(
		lambda u: u.is_authenticated and u.is_semiadmin is True,
		login_url=login_url,
		redirect_field_name=redirect_field_name
	)
	if function:
		return actual_decorator(function)
	return actual_decorator

