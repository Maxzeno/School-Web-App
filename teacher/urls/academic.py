from django.urls import path
from utils.auth import teacher_required as login_required

from ..views import (
    DailyAttendance, ClassRoutine, Subject, Syllabus, EventCalendar,
    ClassRoutineFilter,
    DailyAttendanceFilter, TakeAttendance, AttendanceList,
    SubjectFilter, 
    SyllabusFilter,
    EventCalendarAll, EventCalendarEvent,

    )

login_url = '/portal/login/'


modal = [
    path('portal/teacher/attendance/filter', login_required(DailyAttendanceFilter.as_view(), login_url=login_url), name='attendance_filter'),
    path('portal/teacher/attendance/take_attendance', login_required(TakeAttendance.as_view(), login_url=login_url), name='take_attendance'),
    path('portal/teacher/attendance/attendance_list', login_required(AttendanceList.as_view(), login_url=login_url), name='attendance_list'),
    path('portal/teacher/event_calendar/all', login_required(EventCalendarAll.as_view(), login_url=login_url), name='event_calender_all'),
    path('portal/teacher/subject/filter/<str:class_id>', login_required(SubjectFilter.as_view(), login_url=login_url), name='subject_filter'),
    path('portal/teacher/syllabus/filter/<str:class_id>/<str:section_id>', login_required(SyllabusFilter.as_view(), login_url=login_url), name='syllabus_filter'),
    path('portal/teacher/routine/filter/<str:class_id>/<str:section_id>', login_required(ClassRoutineFilter.as_view(), login_url=login_url), name='routine_filter'),
]


filter_ = [
    path('portal/teacher/event_calendar/event', login_required(EventCalendarEvent.as_view(), login_url=login_url), name='event_calendar_event'),
]


urlpatterns = [
    path('portal/teacher/attendance', login_required(DailyAttendance.as_view(), login_url=login_url), name='attendance'),
    path('portal/teacher/routine', login_required(ClassRoutine.as_view(), login_url=login_url), name='routine'),
    path('portal/teacher/subject', login_required(Subject.as_view(), login_url=login_url), name='subject'),
    path('portal/teacher/syllabus', login_required(Syllabus.as_view(), login_url=login_url), name='syllabus'),
    path('portal/teacher/event_calendar', login_required(EventCalendar.as_view(), login_url=login_url), name='event_calendar'),
]


urlpatterns += filter_
urlpatterns += modal



