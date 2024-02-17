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


def forbidden_403(request):
    """ Status error 403 -> acesso não permitido"""
    template_name = 'core/403_forbidden.html'
    return render(request, template_name)


def not_found_404(request):
    """ Status error 403 -> acesso não permitido"""
    template_name = 'core/404_not_found.html'
    return render(request, template_name)

