from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def portal_aealmancil(request):
    template_name = "portal_aealmancil.html"
    return render(request, template_name)


def login_view(request):
    """ Login do utilizador na plataforma """

    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)

    form = AuthenticationForm()
    template_name = "accounts/login.html"
    context = {"form": form}
    return render(request, template_name, context)

#TODO: fazer a app accounts e passar esta viewpa ra lá
#TODO: fazer o model dos utilizadores, de acordo com o Game_App