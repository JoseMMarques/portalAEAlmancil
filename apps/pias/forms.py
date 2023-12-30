from django.forms import ModelForm
from .models import PIAS


class PiasConsultForm(ModelForm):

    #process_number = forms.IntegerField()

    class Meta:
        model = PIAS
        fields = [
            'student', 'school_year', 'name'
        ]
