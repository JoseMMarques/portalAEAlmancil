from django.contrib import admin

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin, AdminPasswordChangeForm
from .models import User, Teacher, Student, Employee, TeacherMore, StudentMore, EmployeeMore
from .forms import UserAdminCreationForm, UserAdminForm


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_form = UserAdminCreationForm
    add_fieldsets = (
        (None, {
            'fields': ('type', 'name', 'process_number', 'email', 'sex', 'phone', 'address',
                       'is_admin', 'is_staff', 'is_active', 'is_superadmin', 'is_game', 'is_pias',
                       'password1', 'password2',)
        }),
    )
    form = UserAdminForm
    change_password_form = AdminPasswordChangeForm
    fieldsets = (
        (None, {
            'fields': ('email', 'password', 'type', )
        }),
        ('Informações Básicas', {
            'fields': ('name', 'birth_date', 'sex', 'phone', 'address', )
        }),
        (
            'Permissões', {
                'fields': (
                    'is_active', 'is_staff', 'is_admin', 'is_superadmin', 'is_game', 'is_pias',
                    'user_permissions'
                )
            }
        )
    )

    list_display = [
        'type', 'name', 'process_number', 'email', 'get_age', 'birth_date', 'sex', 'phone',
        'address', 'is_game', 'is_pias'
    ]

    list_filter = [
        'type', 'birth_date', 'sex', 'is_game',
        'created', 'modified', 'is_game', 'is_pias'
    ]

    search_fields = [
        'type', 'name', 'birth_date', 'sex', 'phone', 'address', 'is_game',
        'created', 'modified', 'is_game', 'is_pias'
    ]

    ordering = ('name', 'email',)


class TeacherMoreInline(admin.TabularInline):
    model = TeacherMore


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('email', 'password',)
        }),
        ('Informações Básicas', {
            'fields': ('name', 'birth_date', 'sex', 'phone', 'address', 'process_number')
        }),
        (
            'Permissões', {
                'fields': (
                    'is_active', 'is_staff', 'is_admin', 'is_superadmin', 'is_game', 'is_pias',
                    'user_permissions'
                )
            }
        )
    )
    list_display = [
        'name', 'get_first_name', 'get_last_name', 'get_age', 'birth_date', 'sex', 'phone',
        'address', 'is_game', 'is_pias'
    ]

    list_filter = [
        'name', 'birth_date', 'sex', 'phone', 'address', 'is_game',
        'created', 'modified', 'is_game', 'is_pias'
    ]

    search_fields = [
        'name', 'birth_date', 'sex', 'phone', 'address', 'is_game',
        'created', 'modified', 'is_game', 'is_pias'
    ]

    ordering = ('name', 'email',)
    inlines = [
        TeacherMoreInline,
    ]


class StudentMoreInline(admin.StackedInline):
    model = StudentMore


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('email', 'password',)
        }),
        ('Informações Básicas', {
            'fields': ('name', 'birth_date', 'sex', 'phone', 'address', 'process_number')
        }),
        (
            'Permissões', {
                'fields': (
                    'is_active', 'is_staff', 'is_admin', 'is_superadmin', 'is_game', 'is_pias',
                    'user_permissions'
                )
            }
        )
    )
    list_display = [
        'process_number', 'name', 'email', 'get_age', 'birth_date', 'sex', 'phone',
        'address', 'is_game', 'is_pias'
    ]

    list_filter = [
        'birth_date', 'sex', 'address', 'is_game',
        'created', 'modified', 'is_game', 'is_pias'
    ]

    search_fields = [
        'process_number', 'name', 'birth_date', 'sex', 'phone', 'address', 'is_game',
        'created', 'modified', 'is_game', 'is_pias'
    ]

    ordering = ('name', 'email',)
    inlines = [
        StudentMoreInline,
    ]


class EmployeeMoreInline(admin.TabularInline):
    model = EmployeeMore


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('email', 'password',)
        }),
        ('Informações Básicas', {
            'fields': ('name', 'birth_date', 'sex', 'phone', 'address', 'process_number')
        }),
        (
            'Permissões', {
                'fields': (
                    'is_active', 'is_staff', 'is_admin', 'is_superadmin', 'is_game', 'is_pias',
                    'user_permissions'
                )
            }
        )
    )
    list_display = [
        'name', 'get_first_name', 'get_last_name', 'get_age', 'birth_date', 'sex', 'phone',
        'address', 'is_game', 'is_pias',
    ]

    list_filter = [
        'name', 'birth_date', 'sex', 'phone', 'address', 'is_game',
        'created', 'modified', 'is_game', 'is_pias',
    ]

    search_fields = [
        'name', 'birth_date', 'sex', 'phone', 'address', 'is_game',
        'created', 'modified', 'is_game', 'is_pias',
    ]

    ordering = ('name', 'email',)
    inlines = [
        EmployeeMoreInline,
    ]

