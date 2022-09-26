from django.urls import path
from .views import Index, Management, Gallery, Admissions, Contact

app_name = 'main'

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('home/', Index.as_view(), name='home'),
    path('management/', Management.as_view(), name='management'),
    path('gallery/', Gallery.as_view(), name='gallery'),
    path('admissions/', Admissions.as_view(), name='admissions'),
    path('contact/', Contact.as_view(), name='contact'),
]