from apps.pias import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

app_name = 'pias'

urlpatterns = [
    path('', views.pias_view, name="pias_view"),
    path('<student_id>/', views.pias_consult_view, name="pias_consult_view"),
    path('<student_id>/pdf/<doc_slug>/', views.pias_document_pdf_view, name="pias_document_pdf_view"),
    path('<student_id>/inserir/', views.pias_insert_view, name="pias_insert_view"),
    path('<student_id>/<doc_id>/consultar/', views.pias_document_detail_view, name="pias_document_detail_view"),
    path('<student_id>/<doc_id>/editar/', views.pias_edit_view, name="pias_edit_view"),
    path('<student_id>/<doc_id>/remover/', views.pias_delete_view, name="pias_delete_view"),

    #path("consulta/", views.pias_home, name="pias_home"),
    #path("upload/", views.pias_home, name="pias_home"),
]
# Serving the media files in development mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += staticfiles_urlpatterns()
