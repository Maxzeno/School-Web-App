from django.urls import path
from utils.auth import semiadmin_required
from django.contrib.auth.decorators import login_required


from ..views import (
    SubjectPermission, Student, Admission, Teacher, ManagementTeam, TeacherPermission, Parent, Accountant, Librarian, Marksheet,
    StudentFilter, StudentSection, StudentSectionModal, StudentSectionNo, StudentSectionNoLeft, StudentSubject, 
    SubjectPermissionFilter, SubjectPermissionSet,ClassPermissionFilter, ClassPermissionSet,
    AdmissionBulk, AdmissionExcel, StudentEdit, CSVAdmissionGenerate, StudentProfile, 
    TeacherFilter, TeacherCreate, TeacherDelete, TeacherEdit, TeacherUpdatePassword, TeacherPermissionModal,
    CreateTeacherExcel, CSVTeacherGenerate,
    ReturnStudent, ManagementTeamFilter, ManagementTeamCreate, ManagementTeamEdit, ManagementTeamDelete, ManagementTeamUpdatePassword, 
    CSVManagementTeamGenerate, CreateManagementTeamExcel, 
    ParentDelete, ParentEdit, ParentFilter, ParentCreate,
    AccountantDelete, AccountantFilter, AccountantEdit, AccountantCreate,
    LibrarianDelete, LibrarianFilter, LibrarianEdit, LibrarianCreate,
    PermissionFilter, PermissionSet, 
    MarksheetFilter, ResultFilter
    )

login_url = '/portal/login/'

other = [
    path('portal/admin/student/result/filter/<str:id>/<int:exam>', semiadmin_required(ResultFilter.as_view(), login_url=login_url), name='result_filter'),
    path('portal/admin/student/marksheet/filter/<str:id>/<int:session>', semiadmin_required(MarksheetFilter.as_view(), login_url=login_url), name='marksheet_filter'),
    
    path('portal/admin/teacher/filter/permission/<str:class_id>/<str:section_id>', semiadmin_required(PermissionFilter.as_view(), login_url=login_url), name='permission'),
    path('portal/admin/teacher/permission_set', semiadmin_required(PermissionSet.as_view(), login_url=login_url), name='permission_set'),
    
    path('portal/admin/accountant/filter', semiadmin_required(AccountantFilter.as_view(), login_url=login_url), name='accountant_filter'),
    path('portal/admin/accountant/create', semiadmin_required(AccountantCreate.as_view(), login_url=login_url), name='accountant_create'),
    path('portal/admin/accountant/accountant_edit/<int:id>', semiadmin_required(AccountantEdit.as_view(), login_url=login_url), name='update_accountant'),
    path('portal/admin/accountant/delete/<int:id>', semiadmin_required(AccountantDelete.as_view(), login_url=login_url), name='accountant_delete'),
    
    path('portal/admin/librarian/filter', semiadmin_required(LibrarianFilter.as_view(), login_url=login_url), name='librarian_filter'),
    path('portal/admin/librarian/create', semiadmin_required(LibrarianCreate.as_view(), login_url=login_url), name='librarian_create'),
    path('portal/admin/librarian/librarian_edit/<int:id>', semiadmin_required(LibrarianEdit.as_view(), login_url=login_url), name='update_librarian'),
    path('portal/admin/librarian/delete/<int:id>', semiadmin_required(LibrarianDelete.as_view(), login_url=login_url), name='librarian_delete'),
   
    path('portal/admin/parent/delete/<int:id>', semiadmin_required(ParentDelete.as_view(), login_url=login_url), name='parent_delete'),
    path('portal/admin/parent/delete/<int:id>', semiadmin_required(ParentDelete.as_view(), login_url=login_url), name='parent_delete'),
    path('portal/admin/parent/parent_edit/<int:id>', semiadmin_required(ParentEdit.as_view(), login_url=login_url), name='update_parent'),
    path('portal/admin/parent/create', semiadmin_required(ParentCreate.as_view(), login_url=login_url), name='parent_create'),
    path('portal/admin/parent/filter', semiadmin_required(ParentFilter.as_view(), login_url=login_url), name='parent_filter'),

    path('portal/admin/management_team/filter', semiadmin_required(ManagementTeamFilter.as_view(), login_url=login_url), name='management_team'),
    path('portal/admin/management_team/create', semiadmin_required(ManagementTeamCreate.as_view(), login_url=login_url), name='management_team_create'),
    path('portal/admin/management_team/delete/<int:id>', semiadmin_required(ManagementTeamDelete.as_view(), login_url=login_url), name='management_team_delete'),
    path('portal/admin/management_team/management_team_edit/<int:id>', semiadmin_required(ManagementTeamEdit.as_view(), login_url=login_url), name='update_management_team'),
    path('portal/admin/management_team/management_team_password/<int:id>', semiadmin_required(ManagementTeamUpdatePassword.as_view(), login_url=login_url), name='update_teacher_password'),
    path('portal/admin/management_team/excel_management_team_create', semiadmin_required(CreateManagementTeamExcel.as_view(), login_url=login_url), name='excel_management_team_create'),
    path('portal/admin/management_team/csv_management_team_generate.generate.csv', semiadmin_required(CSVManagementTeamGenerate.as_view(), login_url=login_url), name='csv_teacher_generate'),
    
    path('portal/admin/student/filter/student_filter/<str:student_class>/<str:student_class_room>', semiadmin_required(StudentFilter.as_view(), login_url=login_url), name='student_class'),
    path('portal/admin/student/student_profile/<str:id>', login_required(StudentProfile.as_view(), login_url=login_url), name='student_profile'),
    path('portal/admin/student/csv_student_generate.generate.csv', semiadmin_required(CSVAdmissionGenerate.as_view(), login_url=login_url), name='csv_student_generate'),
    
    path('portal/admin/teacher/permission/<int:id>', semiadmin_required(TeacherPermissionModal.as_view(), login_url=login_url), name='teacher_permission'),
    path('portal/admin/teacher/filter', semiadmin_required(TeacherFilter.as_view(), login_url=login_url), name='teacher_filter'),
    path('portal/admin/teacher/csv_teacher_generate.generate.csv', semiadmin_required(CSVTeacherGenerate.as_view(), login_url=login_url), name='csv_teacher_generate'),
    path('portal/admin/teacher/excel_teacher_create', semiadmin_required(CreateTeacherExcel.as_view(), login_url=login_url), name='excel_teacher_create'),
    path('portal/admin/teacher/teacher_update_password/<int:id>', semiadmin_required(TeacherUpdatePassword.as_view(), login_url=login_url), name='update_management_team_password'),
    path('portal/admin/teacher/delete/<int:id>', semiadmin_required(TeacherDelete.as_view(), login_url=login_url), name='teacher_delete'),
    path('portal/admin/teacher/edit/<int:id>', semiadmin_required(TeacherEdit.as_view(), login_url=login_url), name='teacher_edit'),
    path('portal/admin/teacher/create', semiadmin_required(TeacherCreate.as_view(), login_url=login_url), name='teacher_create'),

    path('portal/admin/teacher/filter/class_permission/<str:class_id>/<str:section_id>', semiadmin_required(ClassPermissionFilter.as_view(), login_url=login_url), name='class_permission'),
    path('portal/admin/teacher/filter/subject_permission/<str:class_id>/<str:section_id>/<str:subject_name>', semiadmin_required(SubjectPermissionFilter.as_view(), login_url=login_url), name='subject_permission'),
    path('portal/admin/teacher/class_permission_set', semiadmin_required(ClassPermissionSet.as_view(), login_url=login_url), name='class_permission_set'),
    path('portal/admin/teacher/subject_permission_set', semiadmin_required(SubjectPermissionSet.as_view(), login_url=login_url), name='subject_permission_set'),
]


filter_ = [
    path('portal/admin/student/other/student_section_no_left/<str:student_class>', login_required(StudentSectionNoLeft.as_view(), login_url=login_url), name='student_section_no_left'),
    path('portal/admin/student/other/student_section_no/<str:student_class>', login_required(StudentSectionNo.as_view(), login_url=login_url), name='student_section_no'),
    path('portal/admin/student/other/student_section/<str:student_class>', login_required(StudentSection.as_view(), login_url=login_url), name='student_section'),
    path('portal/admin/student/other/student_section_modal/<str:student_class>', login_required(StudentSectionModal.as_view(), login_url=login_url), name='student_section_modal'),
    path('portal/admin/student/other/student_subject/<str:student_class>', login_required(StudentSubject.as_view(), login_url=login_url), name='student_subject'),
]

urlpatterns = [
    path('portal/admin/student/marksheet/<str:id>', semiadmin_required(Marksheet.as_view(), login_url=login_url), name='student_marksheet'),
    path('portal/admin/student/return/<str:student_class>/<str:student_class_room>', semiadmin_required(ReturnStudent.as_view(), login_url=login_url), name='student_return'),
    path('portal/admin/student/student_update/<str:student_class>/<str:student_class_room>/<str:id>', semiadmin_required(StudentEdit.as_view(), login_url=login_url), name='student_update'),
    path('portal/admin/student/create_excel', semiadmin_required(AdmissionExcel.as_view(), login_url=login_url), name='create_excel'),
    path('portal/admin/student/create_bulk', semiadmin_required(AdmissionBulk.as_view(), login_url=login_url), name='create_bulk'),
    path('portal/admin/student/create', semiadmin_required(Admission.as_view(), login_url=login_url), name='create'),
    path('portal/admin/student', semiadmin_required(Student.as_view(), login_url=login_url), name='student'),
    path('portal/admin/subject_permission', semiadmin_required(SubjectPermission.as_view(), login_url=login_url), name='subject_permission'),
    path('portal/admin/teacher', semiadmin_required(Teacher.as_view(), login_url=login_url), name='teacher'),
    path('portal/admin/management_team', semiadmin_required(ManagementTeam.as_view(), login_url=login_url), name='management_team'),
    path('portal/admin/permission', semiadmin_required(TeacherPermission.as_view(), login_url=login_url), name='permission'),
    path('portal/admin/parent', semiadmin_required(Parent.as_view(), login_url=login_url), name='parent'),
    path('portal/admin/accountant', semiadmin_required(Accountant.as_view(), login_url=login_url), name='accountant'),
    path('portal/admin/librarian', semiadmin_required(Librarian.as_view(), login_url=login_url), name='librarian'),
]


urlpatterns += filter_
urlpatterns += other
