from django.urls import path
from utils.auth import teacher_required as login_required


from ..views import (
   	Student, StudentFilter, Teacher, Marksheet, MarksheetFilter, ResultFilter, 
    )

login_url = '/portal/login/'


urlpatterns = [
    path('portal/teacher/student/result/filter/<str:id>/<int:exam>', login_required(ResultFilter.as_view(), login_url=login_url), name='result_filter'),
    path('portal/teacher/student/marksheet/<str:id>', login_required(Marksheet.as_view(), login_url=login_url), name='student_marksheet'),
    path('portal/teacher/student', login_required(Student.as_view(), login_url=login_url), name='student'),
    path('portal/teacher/student/filter/<str:student_class>/<str:student_class_room>', login_required(StudentFilter.as_view(), login_url=login_url), name='teacher_filter'),
    path('portal/teacher/student/marksheet/filter/<str:id>/<str:session>', login_required(MarksheetFilter.as_view(), login_url=login_url), name='teacher_filter'),
    path('portal/teacher/teacher', login_required(Teacher.as_view(), login_url=login_url), name='teacher'),
]

