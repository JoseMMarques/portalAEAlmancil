from apps.pias import views
from django.urls import path

app_name = 'pias'

urlpatterns = [
    path('', views.pias_view, name="pias_view"),
    path('<student_id>/consulta/', views.pias_consult_view, name="pias_consult_view"),
    path('<student_id>/consulta/<doc_slug>/', views.pias_document_view, name="pias_document_view"),

    #path("consulta/", views.pias_home, name="pias_home"),
    #path("upload/", views.pias_home, name="pias_home"),
]
