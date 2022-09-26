from django.urls import path
from utils.auth import teacher_required as login_required

from ..views import (
	ManageMarks, ManageExamination, ManageCognitiveDomainScore, 
    ManageCognitiveDomainScoreSet, ManageCognitiveDomainScoreFilter,
    MarkFilter, MarkSet
    )

login_url = '/portal/login/'


filter_ = [
    path('portal/teacher/sb_description_score/filter', login_required(ManageCognitiveDomainScoreFilter.as_view(), login_url=login_url), name='sb_description_score_filter'),
    path('portal/teacher/sb_description_score/set', login_required(ManageCognitiveDomainScoreSet.as_view(), login_url=login_url), name='sb_description_score_set'),
    path('portal/teacher/exam/filter/mark_filter', login_required(MarkFilter.as_view(), login_url=login_url), name='mark_filter'),
    path('portal/teacher/exam/filter/mark_set', login_required(MarkSet.as_view(), login_url=login_url), name='mark_set'),
]


urlpatterns = [
    path('portal/teacher/mark', login_required(ManageMarks.as_view(), login_url=login_url), name='mark'),
    path('portal/teacher/exam', login_required(ManageExamination.as_view(), login_url=login_url), name='exam'),
    path('portal/teacher/sb_description_score', login_required(ManageCognitiveDomainScore.as_view(), login_url=login_url), name='sb_description_score_manage'),
]


urlpatterns += filter_
