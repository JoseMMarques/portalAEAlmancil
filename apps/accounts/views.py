from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import User


def login_view(request):
    """ ‘Login’ do utilizador na plataforma """
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        username = form['username']
        password = form['password']
        print(username)
        print(password)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Efetuou login com sucesso, '{username}'")
                return redirect('user_homepage')
            else:
                messages.error(request, "Utilizador e/ou password inválidos!")
        else:
            messages.error(request, "BOOOOLASSS Utilizador e/ou password inválidos!")
    form = AuthenticationForm()
    template_name = "accounts/login.html"
    context = {"form": form}
    return render(request, template_name, context)


def logout_view(request):
    logout(request)
    messages.success(request, "Efetuou o logout com sucesso!")
    return redirect('landing_page')


@login_required
def change_password(request):
    """
        Apresenta o formulário para alteração da password do utilizador
        # link -> navbar -> icon configurações -> alterar_password
        # url -> path("change_password/", views.change_password, name="change_password"),
    """
    template_name = 'accounts/change_password.html'
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        context = {"form": form}
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)     # importante!
            messages.success(request, 'A sua password foi atualizada com sucesso!')
            return redirect('plataforma_aealmancil')
        else:
            messages.error(request, 'Corrija os erros abaixo indicados!')
    else:
        form = PasswordChangeForm(request.user)
        context = {"form": form}
    return render(request, template_name, context)
