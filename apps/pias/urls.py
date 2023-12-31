from apps.pias import views
from django.urls import path

app_name = 'pias'

urlpatterns = [
    path("consulta/", views.pias_consult_form_view, name="pias_consult_form_view"),
    #path("consulta/", views.pias_home, name="pias_home"),
    #path("upload/", views.pias_home, name="pias_home"),
]
