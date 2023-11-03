from django.shortcuts import render


def portal_aealmancil(request):
    template_name = "portal_aealmancil.html"
    return render(request, template_name)
