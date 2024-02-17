from django.contrib import admin
from django.urls import path, include

from core import views

app_name = 'core'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.landing_page, name='landing_page'),
    path('my_homepage/', views.user_homepage, name='user_homepage'),
    path('users/', include('apps.accounts.urls')),
    path('pia/', include('apps.pias.urls')),
    path('error_403/', views.forbidden_403, name='forbidden_403'),
    path('error_404/', views.not_found_404, name='not_found_404')
]
