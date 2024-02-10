from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def landing_page(request):
    """Função que gera a página inicial da plataforma"""
    template_name = "core/landing_page.html"
    return render(request, template_name)


@login_required(login_url='/users/login/')
def user_homepage(request):
    """Homepage do utilizador na plataforma"""
    template_name = 'core/user_homepage.html'
    return render(request, template_name)
