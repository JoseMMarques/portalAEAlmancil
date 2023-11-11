from django.contrib.auth.forms import UserCreationForm, ReadOnlyPasswordHashField
from django import forms
from .models import User


class UserAdminCreationForm(UserCreationForm):
    """Formulário para a criação de um utilizador no Admin"""

    class Meta:
        Model = User
        fields = ['email']


class UserAdminForm(forms.ModelForm):
    """ Formulário para a configuração de mais dados do utilizador no Admin"""

    password = ReadOnlyPasswordHashField(
        label="Password",
        help_text="Raw passwords are not stored, so there is no way to see this "
                  "user’s password, but you can change the password using "
                  '<a href="{}">this form</a>.',
    )

    class Meta:
        model = User
        fields = [
            'type', 'name', 'birth_date', 'sex', 'process_number', 'email', 'phone', 'address',
            'is_admin', 'is_staff', 'is_active', 'is_superadmin', 'is_game', 'is_pias',
        ]


class UserChangeForm(forms.ModelForm):
    """ Formulário para a configuração de dados do utilizador """

    class Meta:
        model = User
        fields = [
            'name', 'birth_date', 'phone', 'address', "password",
        ]
