from django import forms
from .models import PIAS


class PiasConsultForm(forms.Form):
    """Formulario para consulta dos PIAS"""
    search = forms.CharField()


class PiasInsertForm(forms.ModelForm):
    """ Formulário para inserir novo documento no Pias"""

    class Meta:
        model = PIAS
        fields = [
            'school_year', 'type', 'name', 'doc_date', 'description', 'related_docs', 'uploaded_to',
        ]

        widgets = {
            'uploaded_to': forms.FileInput,
        }


class PiasEditForm(forms.ModelForm):
    """ Formulário para inserir novo documento no Pias"""

    class Meta:
        model = PIAS
        fields = [
            'school_year', 'type', 'name', 'doc_date', 'description', 'related_docs', 'uploaded_to',
        ]

