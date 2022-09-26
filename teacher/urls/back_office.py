from django.urls import path
from utils.auth import teacher_required as login_required

from ..views import (
	Book
    )

login_url = '/portal/login/'


urlpatterns = [
    path('portal/teacher/book', login_required(Book.as_view(), login_url=login_url), name='book'),
]

