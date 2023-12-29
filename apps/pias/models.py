from django.db import models
from django.utils.text import slugify


def path_and_rename(instance, filename):
    """ Funtion to rename de uploaded file in the PIAS model"""

    upload_to = 'media/PIAS'
    extension = filename.split('.')[-1]
    student_process_number = instance.student.process_number
    doc_date = instance.doc_date
    doc_date_formated = doc_date.repalce('-', '')
    doc_type = instance.type
    doc_type_formated = doc_type.replace(' ', '')

    new_filename = upload_to + "/" + student_process_number + \
        doc_date_formated + doc_type_formated + instance.pk + extension

    return new_filename


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
        auto_now_add=True,
    )

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
    uploaded_to = models.FileField(
        upload_to=path_and_rename
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

    def __str__(self):
        """returns the name of the object"""
        return self.name

    def get_absolute_url(self):
        pass

    def save(self, *args, **kwargs):
        """ Set an automatic and unique slug for the name of the class"""

        super(PIAS, self).save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(self.name) + '_' + str(self.id)
            self.save()

# Upload files
# https://simpleisbetterthancomplex.com/tutorial/2016/08/01/how-to-upload-files-with-django.html

# relacionar outros docs do mesmo modelo
# https://docs.djangoproject.com/en/4.2/ref/models/fields/#django.db.models.ManyToManyField.symmetrical
# https://afeez1131.hashnode.dev/introduction-to-symmetrical-and-asymmetrical-relationships-in-djangos-manytomanyfield

# rename a file and upload
# https://stackoverflow.com/questions/64633436/how-do-i-rename-image-that-i-uploaded-through-django-rest-framework
# https://stackoverflow.com/questions/15140942/django-imagefield-change-file-name-on-upload
