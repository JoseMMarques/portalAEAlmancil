from django.http import HttpResponse
from apps.school_structure.models import CargoDT, StudentSchoolClass
import datetime


def get_school_year_by_today_date(data):
    """Determina o ano letivo de uma determinada data"""
    if data.month > 8:
        ano_letivo = "{}/{}".format(data.year, data.year+1)
    else:
        ano_letivo = "{}/{}".format(data.year-1, data.year)
    return ano_letivo


def is_dt_or_is_admin_required(function):
    def wrap(request, *args, **kwargs):
        now = datetime.datetime.now()
        ano_letivo = get_school_year_by_today_date(now)

        student = StudentSchoolClass.objects.get(
            student_id=kwargs['student_id'],
            school_year__name=ano_letivo
        )
        cargo_dt = CargoDT.objects.get(
            school_class=student.school_class,
            school_year__name=ano_letivo
        )

        if cargo_dt.teacher_dt == request.user or request.user.is_admin:
            return function(request, *args, **kwargs)
        else:
            return HttpResponse("Não permitido", status=403)

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

