from django.shortcuts import render


def portal_aealmancil(request):
    """Função que gera a página inicial da plataforma"""

    template_name = "portal_aealmancil.html"
    return render(request, template_name)
