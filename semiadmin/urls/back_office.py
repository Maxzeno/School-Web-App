from django.urls import path
from utils.auth import semiadmin_required as login_required

from ..views import (
	Book, BookIssue, Noticeboard,
	BookAll, BookDelete, BookEdit, BookCreate,
    BookIssueFilter, BookIssueDelete, BookIssueEdit, BookIssueCreate,
	NoticeboardAll, NoticeboardDelete, NoticeboardEdit, NoticeboardCreate, NoticeboardCreateDate, NoticeboardCalendarEvent,
    ClassStudent
    )

login_url = '/portal/login/'




modal = [
    path('portal/admin/noticeboard/all/', login_required(NoticeboardAll.as_view(), login_url=login_url), name='noticeboard_all'),
    path('portal/admin/noticeboard/delete/<int:id>', login_required(NoticeboardDelete.as_view(), login_url=login_url), name='noticeboard_delete'),
    path('portal/admin/noticeboard/edit/<int:id>', login_required(NoticeboardEdit.as_view(), login_url=login_url), name='noticeboard_edit'),
    path('portal/admin/noticeboard/create', login_required(NoticeboardCreate.as_view(), login_url=login_url), name='noticeboard_create'),
    path('portal/admin/noticeboard/create/<str:the_date>', login_required(NoticeboardCreateDate.as_view(), login_url=login_url), name='noticeboard_create_date'),

    path('portal/admin/book_issue/filter', login_required(BookIssueFilter.as_view(), login_url=login_url), name='book_issue_filter'),
    path('portal/admin/book_issue/delete/<int:id>', login_required(BookIssueDelete.as_view(), login_url=login_url), name='book_issue_delete'),
    path('portal/admin/book_issue/edit/<int:id>', login_required(BookIssueEdit.as_view(), login_url=login_url), name='book_issue_edit'),
    path('portal/admin/book_issue/create', login_required(BookIssueCreate.as_view(), login_url=login_url), name='book_issue_create'),

    path('portal/admin/book/all/', login_required(BookAll.as_view(), login_url=login_url), name='book_all'),
    path('portal/admin/book/delete/<int:id>', login_required(BookDelete.as_view(), login_url=login_url), name='book_delete'),
    path('portal/admin/book/edit/<int:id>', login_required(BookEdit.as_view(), login_url=login_url), name='book_edit'),
    path('portal/admin/book/create', login_required(BookCreate.as_view(), login_url=login_url), name='book_create'),
]


filter_ = [
    path('portal/admin/class_student/<str:class_id>', login_required(ClassStudent.as_view(), login_url=login_url), name='class_student'),
    path('portal/admin/noticeboard_calendar/event', login_required(NoticeboardCalendarEvent.as_view(), login_url=login_url), name='noticeboard_calendar'),
]


urlpatterns = [
    path('portal/admin/book', login_required(Book.as_view(), login_url=login_url), name='book'),
    path('portal/admin/book_issue', login_required(BookIssue.as_view(), login_url=login_url), name='book_issue'),
    path('portal/admin/noticeboard', login_required(Noticeboard.as_view(), login_url=login_url), name='noticeboard'),
]


urlpatterns += filter_
urlpatterns += modal



