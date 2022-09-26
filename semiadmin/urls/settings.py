from django.urls import path
from utils.auth import semiadmin_required as login_required


from ..views import (
    SchoolSettings
    )

login_url = '/portal/login/'



urlpatterns = [
    path('portal/admin/school_settings', login_required(SchoolSettings.as_view(), login_url=login_url), name='school_settings')
]