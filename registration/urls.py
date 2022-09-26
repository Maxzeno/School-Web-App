from django.urls import path
from .views import PortalLogin, AdminLogin

app_name = 'registration'

urlpatterns = [
	path('portal/login/', PortalLogin.as_view(), name='portal_login'),
	path('admin/login/', AdminLogin.as_view(), name='admin_login'),
]