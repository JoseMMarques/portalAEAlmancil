from django.forms import ModelForm
from .models import PIAS


class PiasConsultForm(ModelForm):
    """Formulario para consulta dos PIAS"""
    class Meta:
        model = PIAS
        fields = [
            'student',
        ]
