from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.accounts.models import User, Student, Teacher


def landing_page(request):
    """Função que gera a página inicial da plataforma"""

    template_name = "core/landing_page.html"
    return render(request, template_name)


@login_required(login_url='/users/login/')
def user_homepage(request):
    template_name = 'core/user_homepage.html'

    return render(request, template_name)
