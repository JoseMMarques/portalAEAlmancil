from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required(login_url='/users/login/')
def pias_home(request):
    """provisório... chama a homepage dos PIAS"""

    template_name = 'pias/pias_homepage.html'
    return render(request, template_name)
