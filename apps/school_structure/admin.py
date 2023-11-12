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
        'name', 'get_school_year', 'get_school', 'get_teachers', 'get_students', 'grade', 'slug', 'created', 'modified'
    ]
    search_fields = [
        'name', 'get_school_year', 'get_school', 'get_teachers', 'get_students', 'grade', 'slug', 'created', 'modified'
    ]
    list_filter = [
        'name', 'school_year__name', 'school__name', 'teachers', 'students', 'grade', 'slug', 'created', 'modified'
    ]

    def get_school_year(self, obj):
        return obj.school_year.name

    # Allows column order sorting
    get_school_year.admin_order_field = 'school_year'
    # Renames column
    get_school_year.short_description = 'Ano Letivo'

    def get_school(self, obj):
        return obj.school.name

    # Allows column order sorting
    get_school.admin_order_field = 'school'
    # Renames column
    get_school.short_description = 'Escola'

    def get_teachers(self, obj):
        return [teacher.get_short_name() for teacher in obj.teachers.all()]

    # Allows column order sorting
    get_teachers.admin_order_field = 'teacher'
    # Renames column
    get_teachers.short_description = 'Professores da turma'

    def get_students(self, obj):
        return [student.get_short_name() for student in obj.students.all()]

    # Allows column order sorting
    get_students.admin_order_field = 'student'
    # Renames column
    get_students.short_description = 'Alunos da turma'


admin.site.register(SchoolClass, SchoolClassAdmin)


class CargoDTAdmin(admin.ModelAdmin):
    """Definições do CargoDT no Admin"""

    list_display = [
        'get_teacher_dt', 'get_school_year', 'get_turma', 'slug', 'created', 'modified'
    ]
    search_fields = [
        'get_teacher_dt', 'get_school_year', 'get_turma', 'slug', 'created', 'modified'
    ]
    list_filter = [
        'teacher_dt__name', 'school_year__name', 'turma__name', 'slug', 'created', 'modified'
    ]

    def get_teacher_dt(self, obj):
        return obj.teacher_dt.get_short_name()

    # Allows column order sorting
    get_teacher_dt.admin_order_field = 'teacher'
    # Renames column
    get_teacher_dt.short_description = 'Diretor de Turma'

    def get_school_year(self, obj):
        return obj.school_year.name

    # Allows column order sorting
    get_school_year.admin_order_field = 'school_year'
    # Renames column
    get_school_year.short_description = 'Ano Letivo'

    def get_turma(self, obj):
        return obj.turma.name

    # Allows column order sorting
    get_turma.admin_order_field = 'turma'
    # Renames column
    get_turma.short_description = 'Turma'


admin.site.register(CargoDT, CargoDTAdmin)
