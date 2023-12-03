from django.contrib import admin

from .models import SchoolYear, School, SchoolClass, StudentSchoolClass, TeacherSchoolClass, CargoDT, Subject


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


class StudentSchoolClassInline(admin.TabularInline):
    model = StudentSchoolClass
    extra = 0


class TeacherSchoolClassInline(admin.TabularInline):
    model = TeacherSchoolClass
    extra = 0


class SchoolClassAdmin(admin.ModelAdmin):
    """Definições da Turma no Admin"""

    list_display = [
        'name', 'get_school_year', 'get_school', 'get_teachers_subjects', 'get_students', 'grade', 'slug', 'created', 'modified'
    ]
    search_fields = [
        'name', 'get_school_year', 'get_school', 'get_teachers_subjects', 'get_students', 'grade', 'slug', 'created', 'modified'
    ]
    list_filter = [
        'name', 'school_year__name', 'school__name', 'teachers', 'students', 'grade', 'slug', 'created', 'modified'
    ]
    inlines = [
        StudentSchoolClassInline,
        TeacherSchoolClassInline,
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

    # def get_teachers(self, obj):
    #     return [teacher.get_short_name() for teacher in obj.teachers.all()]
    #
    # # Allows column order sorting
    # get_teachers.admin_order_field = 'teacher'
    # # Renames column
    # get_teachers.short_description = 'Professores'

    def get_teachers_subjects(self, obj):
        teachers = obj.teachers.all()

        # teacher_subjects_list = ",".join(str(item) for )
        teacher_subjects_list = []
        for teacher in teachers:
            if teacher.get_short_name() not in teacher_subjects_list:
                teacher_subjects_list.append(teacher.get_short_name())
                query = TeacherSchoolClass.objects.filter(teacher=teacher).all()
                query_list = []
                for q in query:
                    query_list.append(q.get_subject_short_name())

                teacher_subjects_list.append(query_list)
        return teacher_subjects_list

    # Allows column order sorting
    get_teachers_subjects.admin_order_field = 'teacher'
    # Renames column
    get_teachers_subjects.short_description = 'Professores'

    def get_students(self, obj):
        return [student.get_short_name() for student in obj.students.all()]

    # Allows column order sorting
    get_students.admin_order_field = 'student'
    # Renames column
    get_students.short_description = 'Alunos'


admin.site.register(SchoolClass, SchoolClassAdmin)


class CargoDTAdmin(admin.ModelAdmin):
    """Definições do CargoDT no Admin"""

    list_display = [
        'get_turma', 'get_teacher_dt', 'get_secretary',  'get_school_year', 'slug', 'modified'
    ]
    search_fields = [
        'get_turma', 'get_teacher_dt', 'get_secretary',  'get_school_year', 'slug', 'modified'
    ]
    list_filter = [
        'teacher_dt__name', 'secretary__name', 'school_year__name', 'school_class__name',
    ]

    def get_teacher_dt(self, obj):
        return obj.teacher_dt.get_short_name()

    # Allows column order sorting
    get_teacher_dt.admin_order_field = 'teacher_dt'
    # Renames column
    get_teacher_dt.short_description = 'Diretor de Turma'

    def get_secretary(self, obj):
        return obj.secretary.get_short_name()

    # Allows column order sorting
    get_secretary.admin_order_field = 'secretary'
    # Renames column
    get_secretary.short_description = 'Secretário'

    def get_school_year(self, obj):
        return obj.school_year.name

    # Allows column order sorting
    get_school_year.admin_order_field = 'school_year'
    # Renames column
    get_school_year.short_description = 'Ano Letivo'

    def get_turma(self, obj):
        return obj.school_class.name

    # Allows column order sorting
    get_turma.admin_order_field = 'school_class'
    # Renames column
    get_turma.short_description = 'Turma'


admin.site.register(CargoDT, CargoDTAdmin)


class SubjectAdmin(admin.ModelAdmin):
    """Definições das disciplinas no Admin"""

    list_display = [
        'name', 'short_name', 'slug', 'created', 'modified'
    ]
    search_fields = [
        'name', 'short_name', 'slug', 'created', 'modified'
    ]
    list_filter = [
        'name', 'short_name', 'slug', 'created', 'modified'
    ]


admin.site.register(Subject, SubjectAdmin)