from django.contrib import admin

from .models import SchoolYear, School, SchoolClass, CargoDT

class SchoolYearAdmin(admin.ModelAdmin):
    """Definições do Ano Letivo no Admin"""

    list_display = [
        'name', 'slug', 'start_date', 'end_date', 'created', 'modified'
    ]
    search_fields = [
        'name', 'slug', 'start_date', 'end_date', 'created', 'modified'
    ]
    list_filter = [
        'name', 'slug', 'start_date', 'end_date', 'created', 'modified'
    ]


admin.site.register(SchoolYear, SchoolYearAdmin)


class SchoolAdmin(admin.ModelAdmin):
    """Definições da Escola no Admin"""

    list_display = [
        'name', 'code', 'slug', 'address', 'phone1', 'phone2', 'email', 'nif', 'created', 'modified'
    ]
    search_fields = [
        'name', 'code', 'slug', 'address', 'phone1', 'phone2', 'email', 'nif', 'created', 'modified'
    ]
    list_filter = [
        'name', 'code', 'slug', 'address', 'phone1', 'phone2', 'email', 'nif', 'created', 'modified'
    ]


admin.site.register(School, SchoolAdmin)


class SchoolClassAdmin(admin.ModelAdmin):
    """Definições da Turma no Admin"""

    list_display = [
        'name', 'get_school_year', 'get_school', 'teacher_dt', 'grade', 'slug', 'created', 'modified'
    ]
    search_fields = [
        'name', 'get_school_year', 'get_school', 'teacher_dt', 'grade', 'slug', 'created', 'modified'
    ]
    list_filter = [
        'name', 'school_year__name', 'school__name', 'teacher_dt', 'grade', 'slug', 'created', 'modified'
    ]

    def get_school_year(self, obj):
        return obj.school_year.name

    # Allows column order sorting
    get_school_year.admin_order_field = 'school_year'
    # Renames column
    get_school_year.short_description = 'Turma'

    def get_school(self, obj):
        return obj.school.name

    # Allows column order sorting
    get_school.admin_order_field = 'school'
    # Renames column
    get_school.short_description = 'Escola'


admin.site.register(SchoolClass, SchoolClassAdmin)