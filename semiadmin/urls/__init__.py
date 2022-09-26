from django.urls import path, include
from django.contrib.auth.decorators import login_required
from utils.auth import semiadmin_required

from ..views import (
	Dashboard, SemiAdminAccount, Logout, GetTemplate, SemiAdminChangePassword
)

app_name = 'semiadmin'
login_url = '/portal/login/'


urlpatterns = [
    path('portal/admin/change_password', semiadmin_required(SemiAdminChangePassword.as_view(), login_url=login_url), name='semiadmin_change_password'),
    path('get_template/<str:name>', semiadmin_required(GetTemplate.as_view(), login_url=login_url), name='get_template'),
    path('portal/admin/dashboard', semiadmin_required(Dashboard.as_view(), login_url=login_url), name='dashboard'),
    path('portal/admin/profile', semiadmin_required(SemiAdminAccount.as_view(), login_url=login_url), name='profile'),
    path('portal/login/logout', login_required(Logout.as_view(), login_url=login_url), name='logout'),
    path('', include('semiadmin.urls.academic')),
    path('', include('semiadmin.urls.accounting')),
    path('', include('semiadmin.urls.back_office')),
    path('', include('semiadmin.urls.exam')),
    path('', include('semiadmin.urls.settings')),
    path('', include('semiadmin.urls.users')),
]
