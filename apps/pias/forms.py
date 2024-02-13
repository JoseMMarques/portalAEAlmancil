from django import forms

from .models import PIAS, StudentSchoolRoute


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


class StudentSchoolRouteAddForm(forms.ModelForm):
    """ Formulário para inserir novo percurso escolar do aluno no Pias"""
    class Meta:
        model = StudentSchoolRoute
        fields = [
            'school_year', 'school',
        ]


class StudentSchoolRouteEditForm(forms.ModelForm):
    """ Formulário para editar o percurso escolar do aluno no Pias"""
    class Meta:
        model = StudentSchoolRoute
        fields = [
            'school_year', 'school',
        ]
