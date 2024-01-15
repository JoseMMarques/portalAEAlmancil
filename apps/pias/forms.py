from django import forms
from .models import PIAS


class PiasConsultForm(forms.Form):
    """Formulario para consulta dos PIAS"""
    search = forms.CharField()
