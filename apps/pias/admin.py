from django.contrib import admin

from .models import PiasType, PIAS


class PiasAdmin(admin.ModelAdmin):
    """Definições dos Pias no Admin"""
    list_display = [
        'name', 'type', 'doc_date', 'uploaded_to', 'get_student', 'description', 'created', 'modified'
    ]

    search_fields = [
        'name', 'type', 'doc_date', 'uploaded_to', 'get_student', 'description', 'created', 'modified'
    ]
    list_filter = [
        'name', 'type', 'doc_date', 'uploaded_to', 'student', 'description', 'created', 'modified'
    ]

    def get_student(self, obj):
        return obj.student.name

    # Allows column order sorting
    get_student.admin_order_field = 'student'
    # Renames column
    get_student.short_description = 'Aluno'


admin.site.register(PIAS, PiasAdmin)


class PiasTypeAdmin(admin.ModelAdmin):
    """Definições dos Pias no Admin"""
    list_display = [
        'name', 'description', 'slug', 'created', 'modified'
    ]

    search_fields = [
        'name', 'description', 'slug', 'created', 'modified'
    ]
    list_filter = [
        'name', 'description', 'slug', 'created', 'modified'
    ]


admin.site.register(PiasType, PiasTypeAdmin)
