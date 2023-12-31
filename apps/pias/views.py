from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import PiasConsultForm


@login_required(login_url='/users/login/')
def pias_home(request):
    """provisório... chama a homepage dos PIAS"""

    template_name = 'pias/pias_homepage.html'
    return render(request, template_name)


def pias_consult_form_view(request):
    context = {}

    # create object of form
    form = PiasConsultForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            messages.success(request, f" consulta realizada com sucesso ")
            return redirect('user_homepage')

    template_name = 'pias/pias_consult.html'

    context = {'form': form}
    return render(request, template_name, context)
