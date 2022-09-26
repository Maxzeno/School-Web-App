from django.urls import path
from utils.auth import semiadmin_required as login_required

from ..views import (
    StudentFeeManager, ExpenseCategory, ExpenseManager,
	ExpenseCategoryAll, ExpenseCategoryDelete, ExpenseCategoryEdit, ExpenseCategoryCreate,
    ExpenseFilter, ExpenseDelete, ExpenseEdit, ExpenseCreate,
	InvoiceFilter, InvoiceDelete, InvoiceEdit, InvoiceCreate,
    ClassSectionStudent
    )

login_url = '/portal/login/'



modal = [
    path('portal/admin/invoice/filter', login_required(InvoiceFilter.as_view(), login_url=login_url), name='invoice_filter'),
    path('portal/admin/invoice/delete/<int:id>', login_required(InvoiceDelete.as_view(), login_url=login_url), name='invoice_delete'),
    path('portal/admin/invoice/edit/mass/<int:id>', login_required(InvoiceEdit.as_view(), login_url=login_url), name='invoice_edit_mass'),
    path('portal/admin/invoice/edit/single/<int:id>', login_required(InvoiceEdit.as_view(), login_url=login_url), name='invoice_edit_single'),
    path('portal/admin/invoice/create/mass', login_required(InvoiceCreate.as_view(), login_url=login_url), name='invoice_create_mass'),
    path('portal/admin/invoice/create/single', login_required(InvoiceCreate.as_view(), login_url=login_url), name='invoice_create_single'),

	path('portal/admin/expense/filter', login_required(ExpenseFilter.as_view(), login_url=login_url), name='expense_filter'),
    path('portal/admin/expense/delete/<int:id>', login_required(ExpenseDelete.as_view(), login_url=login_url), name='expense_delete'),
    path('portal/admin/expense/edit/<int:id>', login_required(ExpenseEdit.as_view(), login_url=login_url), name='expense_edit'),
    path('portal/admin/expense/create', login_required(ExpenseCreate.as_view(), login_url=login_url), name='expense_create'),

	path('portal/admin/expense_category/all', login_required(ExpenseCategoryAll.as_view(), login_url=login_url), name='expense_category_all'),
    path('portal/admin/expense_category/delete/<int:id>', login_required(ExpenseCategoryDelete.as_view(), login_url=login_url), name='expense_category_delete'),
    path('portal/admin/expense_category/edit/<int:id>', login_required(ExpenseCategoryEdit.as_view(), login_url=login_url), name='expense_category_edit'),
    path('portal/admin/expense_category/create', login_required(ExpenseCategoryCreate.as_view(), login_url=login_url), name='expense_category_create'),
]


filter_ = [
    path('portal/admin/class_section_student/<str:class_id>/<str:section_id>', login_required(ClassSectionStudent.as_view(), login_url=login_url), name='class_section_student'),
]



urlpatterns = [
    path('portal/admin/invoice', login_required(StudentFeeManager.as_view(), login_url=login_url), name='invoice'),
    path('portal/admin/expense_category', login_required(ExpenseCategory.as_view(), login_url=login_url), name='expense_category'),
    path('portal/admin/expense', login_required(ExpenseManager.as_view(), login_url=login_url), name='expense'),
]

urlpatterns += filter_
urlpatterns += modal
