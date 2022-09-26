from django.urls import path
# from django.contrib.auth.decorators import login_required
from utils.auth import semiadmin_required as login_required

from ..views import (
    DailyAttendance, ClassRoutine, Subject, Syllabus, Class, ClassRoom, Department, EventCalendar,
    DailyAttendanceFilter, TakeAttendance, AttendanceList,
    ClassRoutineFilter, ClassRoutineDelete, ClassRoutineEdit, ClassRoutineCreate,
    ClassRoomAll, ClassRoomDelete, ClassRoomEdit, ClassRoomCreate,
    DepartmentAll, DepartmentDelete, DepartmentEdit, DepartmentCreate,
    SubjectFilter, SubjectDelete, SubjectEdit, SubjectCreate,
    SyllabusFilter, SyllabusDelete, SyllabusCreate,
    ClassAll, ClassDelete, ClassEdit, ClassCreate,
    EventCalendarAll, EventCalendarDelete, EventCalendarEdit, EventCalendarCreate, EventCalendarEvent,

    )

login_url = '/portal/login/'



modal = [
    path('portal/admin/attendance/filter', login_required(DailyAttendanceFilter.as_view(), login_url=login_url), name='attendance_filter'),
    path('portal/admin/attendance/take_attendance', login_required(TakeAttendance.as_view(), login_url=login_url), name='take_attendance'),
    path('portal/admin/attendance/attendance_list', login_required(AttendanceList.as_view(), login_url=login_url), name='attendance_list'),

    path('portal/admin/event_calendar/all', login_required(EventCalendarAll.as_view(), login_url=login_url), name='event_calender_all'),
    path('portal/admin/event_calendar/delete/<int:id>', login_required(EventCalendarDelete.as_view(), login_url=login_url), name='event_calender_delete'),
    path('portal/admin/event_calendar/edit/<int:id>', login_required(EventCalendarEdit.as_view(), login_url=login_url), name='event_calender_edit'),
    path('portal/admin/event_calendar/create', login_required(EventCalendarCreate.as_view(), login_url=login_url), name='event_calender_create'),

    path('portal/admin/class/all', login_required(ClassAll.as_view(), login_url=login_url), name='class_all'),
    path('portal/admin/class/delete/<str:id>', login_required(ClassDelete.as_view(), login_url=login_url), name='class_delete'),
    path('portal/admin/class/edit/<str:id>', login_required(ClassEdit.as_view(), login_url=login_url), name='class_edit'),
    path('portal/admin/class/create', login_required(ClassCreate.as_view(), login_url=login_url), name='class_create'),

    path('portal/admin/subject/filter/<str:class_id>', login_required(SubjectFilter.as_view(), login_url=login_url), name='subject_filter'),
    path('portal/admin/subject/delete/<str:class_id>/<int:subject_id>', login_required(SubjectDelete.as_view(), login_url=login_url), name='subject_delete'),
    path('portal/admin/subject/edit/<str:class_id>/<int:subject_id>', login_required(SubjectEdit.as_view(), login_url=login_url), name='subject_edit'),
    path('portal/admin/subject/create', login_required(SubjectCreate.as_view(), login_url=login_url), name='subject_create'),
    
    path('portal/admin/syllabus/filter/<str:class_id>/<str:section_id>', login_required(SyllabusFilter.as_view(), login_url=login_url), name='syllabus_filter'),
    path('portal/admin/syllabus/delete/<int:id>', login_required(SyllabusDelete.as_view(), login_url=login_url), name='syllabus_delete'),
    path('portal/admin/syllabus/create', login_required(SyllabusCreate.as_view(), login_url=login_url), name='syllabus_create'),

    path('portal/admin/department/all', login_required(DepartmentAll.as_view(), login_url=login_url), name='department_all'),
    path('portal/admin/department/delete/<int:id>', login_required(DepartmentDelete.as_view(), login_url=login_url), name='department_delete'),
    path('portal/admin/department/edit/<int:id>', login_required(DepartmentEdit.as_view(), login_url=login_url), name='department_edit'),
    path('portal/admin/department/create', login_required(DepartmentCreate.as_view(), login_url=login_url), name='department_create'),

    path('portal/admin/class_room/all', login_required(ClassRoomAll.as_view(), login_url=login_url), name='class_room_all'),
    path('portal/admin/class_room/delete/<int:id>', login_required(ClassRoomDelete.as_view(), login_url=login_url), name='class_room_delete'),
    path('portal/admin/class_room/edit/<int:id>', login_required(ClassRoomEdit.as_view(), login_url=login_url), name='class_room_edit'),
    path('portal/admin/class_room/create', login_required(ClassRoomCreate.as_view(), login_url=login_url), name='class_room_create'),

    path('portal/admin/routine/filter/<str:class_id>/<str:section_id>', login_required(ClassRoutineFilter.as_view(), login_url=login_url), name='routine_filter'),
    path('portal/admin/routine/delete/<int:id>', login_required(ClassRoutineDelete.as_view(), login_url=login_url), name='routine_delete'),
    path('portal/admin/routine/edit/<int:id>', login_required(ClassRoutineEdit.as_view(), login_url=login_url), name='routine_edit'),
    path('portal/admin/routine/create', login_required(ClassRoutineCreate.as_view(), login_url=login_url), name='routine_create'),
]


filter_ = [
    path('portal/admin/event_calendar/event', login_required(EventCalendarEvent.as_view(), login_url=login_url), name='event_calendar_event'),
]


urlpatterns = [
    path('portal/admin/attendance', login_required(DailyAttendance.as_view(), login_url=login_url), name='attendance'),
    path('portal/admin/routine', login_required(ClassRoutine.as_view(), login_url=login_url), name='routine'),
    path('portal/admin/subject', login_required(Subject.as_view(), login_url=login_url), name='subject'),
    path('portal/admin/syllabus', login_required(Syllabus.as_view(), login_url=login_url), name='syllabus'),
    path('portal/admin/manage_class', login_required(Class.as_view(), login_url=login_url), name='manage_class'),
    path('portal/admin/class_room', login_required(ClassRoom.as_view(), login_url=login_url), name='class_room'),
    path('portal/admin/department', login_required(Department.as_view(), login_url=login_url), name='department'),
    path('portal/admin/event_calendar', login_required(EventCalendar.as_view(), login_url=login_url), name='event_calendar'),
]


urlpatterns += filter_
urlpatterns += modal



