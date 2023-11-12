from apps.pias import views
from django.urls import path

app_name = 'pias'

urlpatterns = [
    path("home/", views.pias_home, name="pias_home"),
]
