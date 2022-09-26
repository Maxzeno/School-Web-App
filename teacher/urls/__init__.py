from django.urls import path, include
from utils.auth import teacher_required as login_required

from ..views import (
	Dashboard, TeacherAccount, Logout, TeacherChangePassword
)

app_name = 'teacher'
login_url = '/portal/login/'


urlpatterns = [
    path('portal/teacher/change_password', login_required(TeacherChangePassword.as_view(), login_url=login_url), name='semiadmin_change_password'),
    path('portal/teacher/dashboard', login_required(Dashboard.as_view(), login_url=login_url), name='dashboard'),
    path('portal/teacher/profile', login_required(TeacherAccount.as_view(), login_url=login_url), name='profile'),
    path('portal/login/logout', login_required(Logout.as_view(), login_url=login_url), name='logout'),
    path('', include('teacher.urls.academic')),
    path('', include('teacher.urls.back_office')),
    path('', include('teacher.urls.exam')),
    path('', include('teacher.urls.users')),
]
