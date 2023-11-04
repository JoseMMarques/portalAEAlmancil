from django.contrib import admin
from django.urls import path, include

from core import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.portal_aealmancil, name='portal_aealmancil'),
    path('users/', include('apps.accounts.urls')),
]
