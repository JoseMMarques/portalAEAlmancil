import os

from django.db import models
from django.urls import reverse
from django.utils.text import slugify
import datetime
from django.conf import settings
import unicodedata


def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])


def path_and_rename(instance, filename):
    """ Funtion to rename de uploaded file in the PIAS model"""

    # converte a data e tempo atual em string
    # vai servir como 'id', para tornar o nome do ficheiro único
    now = datetime.datetime.now()
    date_string = now.strftime("%Y%m%d%H%M%S")

    upload_to = str(settings.MEDIA_PIAS)
    extension = filename.split('.')[-1]
    student_process_number = instance.student.process_number
    doc_date = str(instance.doc_date)
    doc_date_formated = doc_date.replace('-', '')
    doc_type = instance.type
    doc_type_formated = str(doc_type).replace(' ', '')
    doc_type_formated = remove_accents(doc_type_formated)

    new_filename = upload_to + "/" + student_process_number + "_" + \
                   doc_date_formated + "_" + doc_type_formated + "_" + date_string + "." + extension

    new_filename = str(new_filename).replace("\\", "/")
    return new_filename


class PiasType(models.Model):
    """Um modelo para os tipos de documentos do PIAS"""

    name = models.CharField(
        'Tipo',
        max_length=300,
        blank=False,
        null=False,
    )
    description = models.TextField(
        'Descrição',
        blank=True,
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        blank=True,
        help_text='Deixar em branco para criar um slug automático e único'
    )
    created = models.DateTimeField(
        'Criado em',
        auto_now_add=True,
    )
    modified = models.DateTimeField(
        'Modificado em',
        auto_now=True,
    )

    class Meta:
        verbose_name = 'Tipo de Documento'
        verbose_name_plural = 'Tipos de Documentos'
        ordering = ['name']

    def __str__(self):
        """returns the name of the object"""
        return self.name

    def get_absolute_url(self):
        pass

    def save(self, *args, **kwargs):
        """ Set an automatic and unique slug for the name of the class"""

        super(PiasType, self).save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(self.name)
            self.save()


class PIAS(models.Model):
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
    description = models.TextField(
        'Descrição',
        blank=True,
    )
    slug = models.SlugField(
        max_length=250,
        unique=True,
        blank=True,
        help_text='Deixar em branco para criar um slug automático e único'
    )
    uploaded_to = models.FileField(
        upload_to=path_and_rename,
        max_length=500,
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
        auto_now=True,
    )

    class Meta:
        verbose_name = 'PIA'
        verbose_name_plural = 'PIA\'s'
        ordering = ['name']

    def __str__(self):
        """returns the name of the object"""
        return self.name

    def get_absolute_url(self):
        return reverse(
            'pias:pias_document_pdf_view',
            kwargs={
                'student_id': self.student_id,
                'doc_slug': self.slug
            }
        )

    def save(self, *args, **kwargs):
        """ Set an automatic and unique slug for the name of the class"""

        super(PIAS, self).save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(self.name) + '_' + str(self.id)
            self.save()

    def rename_file_edited_document(self, old_file_path):
        """ Funtion to rename un edited file in the PIAS model"""
        upload_to = str(settings.MEDIA_PIAS)
        # vai ao nome antigo do ficheiro buscar os dados corretos
        student_process_number = old_file_path.split('_')[-4].split("\\")[-1]
        doc_date = str(self.doc_date)
        doc_date_formated = doc_date.replace('-', '')
        date_string_and_extension = old_file_path.split('_')[-1]
        doc_type = self.type
        doc_type_formated = str(doc_type).replace(' ', '')
        doc_type_formated = remove_accents(doc_type_formated)

        # localização do ficheiro com o nome do ficheiro incorporado
        new_file_path = upload_to + "/" + student_process_number + "_" + \
                       doc_date_formated + "_" + doc_type_formated + "_" + date_string_and_extension

        # formata o path
        new_file_path = str(new_file_path).replace("\\", "/")
        # renomeia o ficheiro no diretório PIAS
        os.rename(old_file_path, new_file_path)
        # atualiza o campo "uploaded_to"
        self.uploaded_to = new_file_path.split('/')[-2] + "/" + new_file_path.split('/')[-1]

        return new_file_path


# Upload files
# https://simpleisbetterthancomplex.com/tutorial/2016/08/01/how-to-upload-files-with-django.html

# relacionar outros docs do mesmo modelo
# https://docs.djangoproject.com/en/4.2/ref/models/fields/#django.db.models.ManyToManyField.symmetrical
# https://afeez1131.hashnode.dev/introduction-to-symmetrical-and-asymmetrical-relationships-in-djangos-manytomanyfield

# rename a file and upload
# https://stackoverflow.com/questions/64633436/how-do-i-rename-image-that-i-uploaded-through-django-rest-framework
# https://stackoverflow.com/questions/15140942/django-imagefield-change-file-name-on-upload

# apagar ficheiros de diretorios
# https://stackoverflow.com/questions/33080360/how-to-delete-files-from-filesystem-using-post-delete-django-1-8

# VER ESTE PARA ALTERAR FICHEIRO NO DIRETORIO
# https://stackoverflow.com/questions/73019488/overwrite-file-if-the-name-is-same-in-django