from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import PiasConsultForm
from .models import PIAS


@login_required(login_url='/users/login/')
def pias_home(request):
    """provisório... chama a homepage dos PIAS"""

    template_name = 'pias/pias_homepage.html'
    return render(request, template_name)


def pias_consult_view(request):
    """ View aue controla a página de consulta dos PIAS """

    context = {}

    # create object of form
    form = PiasConsultForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():

            student = form.cleaned_data.get('student')
            student_pias = PIAS.objects.all().filter(
                student=student,
            ).order_by('-doc_date')

            messages.success(request, f" consulta realizada com sucesso ")

            context = {"pias": student_pias}
            template_name = 'pias/pias_result.html'

            return render(request, template_name, context)

    template_name = 'pias/pias_consult.html'

    context = {'form': form}
    return render(request, template_name, context)


def pias_result_view(request):
    """ View aue controla a página de resultados dos PIAS pesquisados """

    text = 'Estou nos resultados'
    context = {"text": text}
    template_name = 'pias/pias_result.html'

    return render(request, template_name, context)
