from django.db import models

# Create your models here.


class PiasType(models.Model):
    """Um modelo para os tipos de documentos do PIAS"""

    name = models.CharField(
        'Tipo',
        max_length=300,
        blank=False,
        null=False,
    )
    desciption = models.TextField(
        'Descrição',
        blank=True,
    )
    created = models.DateTimeField(
        'Criado em',
        auto_now_add=True,
    )
    modified = models.DateTimeField(
        'Modificado em',
        auto_now_add=True,
    )


class PIAS (models.Model):
    """ Um modelo para os pias dos alunos"""

    school_year = models.ForeignKey(
        'school_structure.SchoolYear',
        verbose_name='Ano Letivo',
        on_delete=models.CASCADE
    )
    type = models.ForeignKey(
        'PiasType',
        verbose_name="Tipo",
        on_delete=models.CASCADE
    )
    student = models.ForeignKey(
        'accounts.Student',
        verbose_name='Aluno',
        on_delete=models.CASCADE
    )
    name = models.CharField(
        'Nome',
        max_length=200,
        blank=False,
        null=False,
    )
    doc_date = models.DateField(
        'Data do documento',
        blank=True,
        null=True,
    )
    desciption = models.TextField(
        'Descrição',
        blank=True,
    )
    slug = models.SlugField(
        max_length=250,
        unique=True,
        blank=True,
        help_text='Deixar em branco para criar um slug automático e único'
    )
    file_name = models.CharField(
        'Nome do ficheiro',
        max_length=400,
        blank=False,
        null=False,
    )
    uploaded_to = models.FileField(
        upload_to='media/PIAS'
    )
    related_docs = models.ManyToManyField(
        "self",
        blank=True,
        verbose_name='Documentos relacionados',
    )
    created = models.DateTimeField(
        'Criado em',
        auto_now_add=True,
    )
    modified = models.DateTimeField(
        'Modificado em',
        auto_now_add=True,
    )

# Upload files
# https://simpleisbetterthancomplex.com/tutorial/2016/08/01/how-to-upload-files-with-django.html

# relacionar outros docs do mesmo modelo
# https://docs.djangoproject.com/en/4.2/ref/models/fields/#django.db.models.ManyToManyField.symmetrical
# https://afeez1131.hashnode.dev/introduction-to-symmetrical-and-asymmetrical-relationships-in-djangos-manytomanyfield

