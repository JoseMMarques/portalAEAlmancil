from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, FileResponse
import os
from django.db.models import Q

import core.settings
from .forms import PiasConsultForm
from .models import PIAS
from apps.accounts.models import Student, StudentMore
from apps.school_structure.models import StudentSchoolClass


@login_required(login_url='/users/login/')
def pias_home(request):
    """provisório... chama a homepage dos PIAS"""

    template_name = 'pias/pias_homepage.html'
    return render(request, template_name)


def pias_view(request):
    """ View aue controla a página de consulta dos PIAS """

    context = {}

    # create object of form
    form = PiasConsultForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():

            # student = form.cleaned_data.get('student')
            # student_pias = PIAS.objects.all().filter(
            #    student=student,
            # ).order_by('-doc_date')

            query = form.cleaned_data.get('turma')
            qs2 = StudentSchoolClass.objects.all()
            qs1 = Student.objects.all()
            print(qs1)
            if query is not None:
                lookups = Q(process_number__icontains=query) | Q(name__icontains=query) | Q(Alunos_turma__school_class__name__icontains=query)
                print(lookups)
                qs1 = Student.objects.filter(lookups)
            context = {
                "students": qs1,
            }
            print(qs1)
            template_name = 'pias/pias.html'
            return render(request, template_name, context)

            # ver -> https://stackoverflow.com/questions/73901044/django-python-reference-related-data-from-q-object

            # return redirect('pias:pias_consult_view', student_id=student.id)

    template_name = 'pias/pias.html'

    context = {'form': form}
    return render(request, template_name, context)


def pias_consult_view(request, student_id):
    """ View aue controla a página de resultados dos PIAS pesquisados """

    student = get_object_or_404(Student, id=student_id)
    student_pias = PIAS.objects.all().filter(
        student=student_id,
    ).order_by('-doc_date')

    context = {
        "pias": student_pias,
        "student": student,
    }

    template_name = 'pias/pias_consult.html'

    return render(request, template_name, context)


def pias_document_view(request, student_id, doc_slug):

    doc = get_object_or_404(PIAS, slug=doc_slug)

    doc_full_path = str(core.settings.MEDIA_ROOT) + '/' + str(doc.uploaded_to)

    print(doc_full_path)

    with open(doc_full_path, 'rb') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'filename=some_file.pdf'
        return response



