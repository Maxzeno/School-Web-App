from django.urls import path
from utils.auth import semiadmin_required
from django.contrib.auth.decorators import login_required


from ..views import (
	ManageMarks, ManageExamination, Grade, PassMarks, ManageCognitiveDomain, ManageCognitiveDomainScore, PrincipalCommentCode, 
	TeacherCommentCode, PrincipalSubjectCode, CognitiveKeyDomainScore, HouseMasterCommentCode, Promotion, TabulationSheetMarks,
    ManageExaminationCreate, ManageExaminationEdit, ManageExaminationDelete, ManageExaminationAll, 
    PassMarkCreate, PassMarkEdit, PassMarkDelete, PassMarkAll, 
    ManageCognitiveDomainCreate, ManageCognitiveDomainEdit, ManageCognitiveDomainDelete, ManageCognitiveDomainAll, 
    PromotionFilter, PromotionSet,
    ManageCognitiveDomainScoreSet, ManageCognitiveDomainScoreFilter,

    PrincipalCommentCodeCreate, PrincipalCommentCodeEdit, PrincipalCommentCodeDelete, PrincipalCommentCodeAll, 
    TeacherCommentCodeCreate, TeacherCommentCodeEdit, TeacherCommentCodeDelete, TeacherCommentCodeAll,
    PrincipalSubjectCodeCreate, PrincipalSubjectCodeEdit, PrincipalSubjectCodeDelete, PrincipalSubjectCodeAll,
    CognitiveKeyDomainScoreCreate, CognitiveKeyDomainScoreEdit, CognitiveKeyDomainScoreDelete, CognitiveKeyDomainScoreAll,
    HousemasterCommentCodeCreate, HousemasterCommentCodeEdit, HousemasterCommentCodeDelete, HousemasterCommentCodeAll,
    ExamTerm, ExamTermNoAnnual,
    MarkFilter, MarkSet, GetGrade, GetGradeRemark, GradeAll, GradeDelete, GradeEdit, GradeCreate,
    TabulationSheetFilter, TabulationSheetPrintView, 
    )

login_url = '/portal/login/'


modal = [
    path('portal/admin/promotion/filter', semiadmin_required(PromotionFilter.as_view(), login_url=login_url), name='promotion_filter'),
    path('portal/admin/promotion/set', semiadmin_required(PromotionSet.as_view(), login_url=login_url), name='promotion_set'),
    
    path('portal/admin/grade/all', semiadmin_required(GradeAll.as_view(), login_url=login_url), name='grade_all'),
    path('portal/admin/grade/delete/<int:id>', semiadmin_required(GradeDelete.as_view(), login_url=login_url), name='grade_delete'),
    path('portal/admin/grade/edit/<int:id>', semiadmin_required(GradeEdit.as_view(), login_url=login_url), name='grade_edit'),
    path('portal/admin/grade/create', semiadmin_required(GradeCreate.as_view(), login_url=login_url), name='grade_create'),

    path('portal/admin/housemaster_comment_code/all', semiadmin_required(HousemasterCommentCodeAll.as_view(), login_url=login_url), name='housemaster_comment_code_all'),
    path('portal/admin/housemaster_comment_code/delete/<int:id>', semiadmin_required(HousemasterCommentCodeDelete.as_view(), login_url=login_url), name='housemaster_comment_code_delete'),
    path('portal/admin/housemaster_comment_code/edit/<int:id>', semiadmin_required(HousemasterCommentCodeEdit.as_view(), login_url=login_url), name='housemaster_comment_code_edit'),
    path('portal/admin/housemaster_comment_code/create', semiadmin_required(HousemasterCommentCodeCreate.as_view(), login_url=login_url), name='housemaster_comment_code_create'),

    path('portal/admin/cognitive_key_domain_score/all', semiadmin_required(CognitiveKeyDomainScoreAll.as_view(), login_url=login_url), name='cognitive_key_domain_score_all'),
    path('portal/admin/cognitive_key_domain_score/delete/<int:id>', semiadmin_required(CognitiveKeyDomainScoreDelete.as_view(), login_url=login_url), name='cognitive_key_domain_score_delete'),
    path('portal/admin/cognitive_key_domain_score/edit/<int:id>', semiadmin_required(CognitiveKeyDomainScoreEdit.as_view(), login_url=login_url), name='cognitive_key_domain_score_edit'),
    path('portal/admin/cognitive_key_domain_score/create', semiadmin_required(CognitiveKeyDomainScoreCreate.as_view(), login_url=login_url), name='cognitive_key_domain_score_create'),


    path('portal/admin/principal_subject_code/all', semiadmin_required(PrincipalSubjectCodeAll.as_view(), login_url=login_url), name='principal_subject_code_all'),
    path('portal/admin/principal_subject_code/delete/<int:id>', semiadmin_required(PrincipalSubjectCodeDelete.as_view(), login_url=login_url), name='principal_subject_code_delete'),
    path('portal/admin/principal_subject_code/edit/<int:id>', semiadmin_required(PrincipalSubjectCodeEdit.as_view(), login_url=login_url), name='principal_subject_code_edit'),
    path('portal/admin/principal_subject_code/create', semiadmin_required(PrincipalSubjectCodeCreate.as_view(), login_url=login_url), name='principal_subject_code_create'),

    
    path('portal/admin/teacher_comment_code/all', semiadmin_required(TeacherCommentCodeAll.as_view(), login_url=login_url), name='teacher_comment_code_all'),
    path('portal/admin/teacher_comment_code/delete/<int:id>', semiadmin_required(TeacherCommentCodeDelete.as_view(), login_url=login_url), name='teacher_comment_code_delete'),
    path('portal/admin/teacher_comment_code/edit/<int:id>', semiadmin_required(TeacherCommentCodeEdit.as_view(), login_url=login_url), name='teacher_comment_code_edit'),
    path('portal/admin/teacher_comment_code/create', semiadmin_required(TeacherCommentCodeCreate.as_view(), login_url=login_url), name='teacher_comment_code_create'),

    path('portal/admin/principal_comment_code/all', semiadmin_required(PrincipalCommentCodeAll.as_view(), login_url=login_url), name='principal_comment_code_all'),
    path('portal/admin/principal_comment_code/delete/<int:id>', semiadmin_required(PrincipalCommentCodeDelete.as_view(), login_url=login_url), name='principal_comment_code_delete'),
    path('portal/admin/principal_comment_code/edit/<int:id>', semiadmin_required(PrincipalCommentCodeEdit.as_view(), login_url=login_url), name='principal_comment_code_edit'),
    path('portal/admin/principal_comment_code/create', semiadmin_required(PrincipalCommentCodeCreate.as_view(), login_url=login_url), name='principal_comment_code_create'),

    path('portal/admin/sb_description_score/filter', semiadmin_required(ManageCognitiveDomainScoreFilter.as_view(), login_url=login_url), name='sb_description_score_filter'),
    path('portal/admin/sb_description_score/set', semiadmin_required(ManageCognitiveDomainScoreSet.as_view(), login_url=login_url), name='sb_description_score_set'),
  
    path('portal/admin/sb_description/all', semiadmin_required(ManageCognitiveDomainAll.as_view(), login_url=login_url), name='sb_description_all'),
    path('portal/admin/sb_description/delete/<int:id>', semiadmin_required(ManageCognitiveDomainDelete.as_view(), login_url=login_url), name='sb_description_delete'),
    path('portal/admin/sb_description/edit/<int:id>', semiadmin_required(ManageCognitiveDomainEdit.as_view(), login_url=login_url), name='sb_description_edit'),
    path('portal/admin/sb_description/create', semiadmin_required(ManageCognitiveDomainCreate.as_view(), login_url=login_url), name='sb_description_create'),

    path('portal/admin/pass_mark/all', semiadmin_required(PassMarkAll.as_view(), login_url=login_url), name='pass_mark_all'),
    path('portal/admin/pass_mark/delete/<int:id>', semiadmin_required(PassMarkDelete.as_view(), login_url=login_url), name='pass_mark_delete'),
    path('portal/admin/pass_mark/edit/<int:id>', semiadmin_required(PassMarkEdit.as_view(), login_url=login_url), name='pass_mark_edit'),
    path('portal/admin/pass_mark/create', semiadmin_required(PassMarkCreate.as_view(), login_url=login_url), name='pass_mark_create'),

    path('portal/admin/exam/manage_exam/all', semiadmin_required(ManageExaminationAll.as_view(), login_url=login_url), name='manage_exam_all'),
    path('portal/admin/exam/manage_exam/delete/<int:id>', semiadmin_required(ManageExaminationDelete.as_view(), login_url=login_url), name='manage_exam_delete'),
    path('portal/admin/exam/manage_exam/edit/<int:id>', semiadmin_required(ManageExaminationEdit.as_view(), login_url=login_url), name='manage_exam_edit'),
    path('portal/admin/exam/manage_exam/create', semiadmin_required(ManageExaminationCreate.as_view(), login_url=login_url), name='manage_exam_create'),
]


filter_ = [
    path('portal/admin/exam/tabulation_sheet_print_view/<str:class_id>/<str:section_id>/<str:exam_id>', semiadmin_required(TabulationSheetPrintView.as_view(), login_url=login_url), name='tabulation_sheet_print_view'),
    path('portal/admin/exam/filter/tabulation_sheet', semiadmin_required(TabulationSheetFilter.as_view(), login_url=login_url), name='tabulation_sheet_filter'),
    path('portal/admin/exam/filter/mark_filter', semiadmin_required(MarkFilter.as_view(), login_url=login_url), name='mark_filter'),
    path('portal/admin/exam/filter/exam_term_no_annual/<str:session_id>', login_required(ExamTermNoAnnual.as_view(), login_url=login_url), name='exam_term_no_annual'),
    path('portal/admin/exam/filter/exam_term/<str:session_id>', login_required(ExamTerm.as_view(), login_url=login_url), name='exam_term'),
    path('portal/admin/exam/filter/mark_set', semiadmin_required(MarkSet.as_view(), login_url=login_url), name='mark_set'),
    path('portal/admin/exam/filter/get_grade/<int:total_mark>', login_required(GetGrade.as_view(), login_url=login_url), name='get_grade'),
    path('portal/admin/exam/filter/get_grade_remark/<int:total_mark>', login_required(GetGradeRemark.as_view(), login_url=login_url), name='get_grade_remark'),
]


urlpatterns = [
    path('portal/admin/mark', semiadmin_required(ManageMarks.as_view(), login_url=login_url), name='mark'),
    path('portal/admin/exam', semiadmin_required(ManageExamination.as_view(), login_url=login_url), name='exam'),
    path('portal/admin/grade', semiadmin_required(Grade.as_view(), login_url=login_url), name='grade'),
    path('portal/admin/pass_mark', semiadmin_required(PassMarks.as_view(), login_url=login_url), name='pass_mark'),
    path('portal/admin/sb_description', semiadmin_required(ManageCognitiveDomain.as_view(), login_url=login_url), name='sb_description'),
    path('portal/admin/sb_description_score', semiadmin_required(ManageCognitiveDomainScore.as_view(), login_url=login_url), name='sb_description_score_manage'),
    path('portal/admin/principal_comment_code', semiadmin_required(PrincipalCommentCode.as_view(), login_url=login_url), name='principal_comment_codes'),
    path('portal/admin/teacher_comment_code', semiadmin_required(TeacherCommentCode.as_view(), login_url=login_url), name='teacher_comment_codes'),
    path('portal/admin/principal_subject_code', semiadmin_required(PrincipalSubjectCode.as_view(), login_url=login_url), name='principal_subject_codes'),
    path('portal/admin/cognitive_key_domain_score', semiadmin_required(CognitiveKeyDomainScore.as_view(), login_url=login_url), name='cognitive_key_domain_scores'),
    path('portal/admin/housemaster_comment_code', semiadmin_required(HouseMasterCommentCode.as_view(), login_url=login_url), name='housemaster_comment_codes'),
    path('portal/admin/promotion', semiadmin_required(Promotion.as_view(), login_url=login_url), name='promotion'),
    path('portal/admin/tabulation_sheet', semiadmin_required(TabulationSheetMarks.as_view(), login_url=login_url), name='tabulation_sheet'),
]


urlpatterns += filter_
urlpatterns += modal
