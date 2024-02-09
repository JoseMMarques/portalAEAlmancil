from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, FileResponse
import os
from django.db.models import Q

import core.settings
from .forms import PiasConsultForm, PiasInsertForm, PiasEditForm
from .models import PIAS
from apps.accounts.models import Student, StudentMore
from apps.school_structure.models import StudentSchoolClass
from django.conf import settings


@login_required(login_url='/users/login/')
def pias_home(request):
    """provisório... chama a homepage dos PIAS"""

    template_name = 'pias/pias_homepage.html'
    return render(request, template_name)


def pias_view(request):
    """ View aue controla a página de consulta dos PIAS """

    # create object of form
    form = PiasConsultForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():

            query = form.cleaned_data.get('search')
            qs = Student.objects.all()

            if query is not None:
                lookups = Q(process_number__icontains=query) | Q(name__icontains=query) \
                          | Q(Alunos_turma__school_class__name__icontains=query)
                qs = Student.objects.filter(lookups)

            form = PiasConsultForm(request.GET)

            template_name = 'pias/pias.html'
            context = {
                'students': qs,
                'form': form
            }
            return render(request, template_name, context)

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
    """ Mostra o documento numa janela à parte"""
    doc = get_object_or_404(PIAS, slug=doc_slug)
    # Construct the name for downloaded file
    download_file_name = str(doc.uploaded_to).split('/')[-1]
    # Abre o documento através do path completo
    with open(str(doc.uploaded_to.path), 'rb') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'filename= "PIA_{}"'.format(download_file_name)
        return response


def pias_insert_view(request, student_id):
    """ View aue insere novos documentos nos PIAS """
    student = get_object_or_404(Student, id=student_id)
    form = PiasInsertForm(request.POST, request.FILES or None)
    if form.is_valid():
        document = form.save(commit=False)
        document.student = student
        document.save()
        messages.success(request, f"'{document.name}' inserido no processo ")
        return redirect('pias:pias_consult_view', student_id=student_id)

    template_name = 'pias/pias_document_add.html'
    context = {
        'form': form,
        'student': student,
    }
    return render(request, template_name, context)


def pias_delete_view(request, student_id, doc_id):
    """Apaga um documento do PIA do aluno indicado"""
    doc = get_object_or_404(PIAS, id=doc_id)
    student = get_object_or_404(Student, id=student_id)
    # create object of form
    if request.method == 'POST':
        messages.success(request, f"'Documento '{doc.name}' removido com sucesso ")
        # remove o registo da base de dados e o ficheiro do diretório
        doc.delete()
        os.remove(doc.uploaded_to.path)
        return redirect('pias:pias_consult_view', student_id=student_id)

    template_name = 'pias/pias_document_delete.html'
    context = {
        'student': student,
        'doc': doc,
    }
    return render(request, template_name, context)


def pias_edit_view(request, student_id, doc_id):
    """ View aue insere novos documentos nos PIAS """
    student = get_object_or_404(Student, id=student_id)
    doc = get_object_or_404(PIAS, id=doc_id)
    old_file_path = doc.uploaded_to.path
    old_file_name = str(doc.uploaded_to).split('/')[-1]

    form = PiasEditForm(request.POST or None, request.FILES or None, instance=doc)
    if request.method == 'POST':
        if form.is_valid():
            document = form.save(commit=False)
            # form sem ficheiro -> atualiza os campos do nome
            if not request.FILES:
                document.rename_file_edited_document(old_file_path)
            # guarda o documento alterado na DB
            document.save()
            # se foi inserido um novo ficheiro, remove o antigo da DB
            if request.FILES:
                new_file_name = str(request.FILES['uploaded_to'])
                if new_file_name != old_file_name:
                    os.remove(old_file_path)
                    pass
            return redirect('pias:pias_consult_view', student_id=student_id)

    template_name = 'pias/pias_document_edit.html'
    context = {
        'form': form,
        'student': student,
        'doc': doc,
    }
    return render(request, template_name, context)
