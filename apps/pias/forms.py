from django.forms import ClearableFileInput
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

    def __init__(self, student_id, *args, **kwargs):
        super(PiasInsertForm, self).__init__(*args, **kwargs)
        # para aparecerem só documentos relacionados do próprio aluno
        if student_id:
            self.fields['related_docs'].queryset = PIAS.objects.filter(student_id=student_id)


class PiasEditForm(forms.ModelForm):
    """ Formulário para inserir novo documento no Pias"""

    class Meta:
        model = PIAS
        fields = [
            'school_year', 'type', 'name', 'doc_date', 'description', 'related_docs', 'uploaded_to',
        ]

        widgets = {
            'uploaded_to': forms.ClearableFileInput(),
        }

    def __init__(self, student_id, doc_id, *args, **kwargs):
        super(PiasEditForm, self).__init__(*args, **kwargs)
        # para aparecerem só documentos relacionados do próprio aluno
        if student_id:
            self.fields['related_docs'].queryset = PIAS.objects.filter(student_id=student_id).exclude(id=doc_id)

        # if doc_id:
        #     doc = PIAS.objects.get(id=doc_id)
        #     self.fields['uploaded_to'].widget.attrs.update(
        #         {'analytics_logger_id': doc.id, 'filename': doc.get_absolute_url(), }
        #     )


