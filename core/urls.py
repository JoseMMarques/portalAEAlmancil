from django.contrib import admin
from django.urls import path, include

from core import views

app_name = 'core'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.landing_page, name='landing_page'),
    path('my_homepage/', views.user_homepage, name='user_homepage'),
    path('users/', include('apps.accounts.urls')),
]
