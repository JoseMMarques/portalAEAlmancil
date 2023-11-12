from django.db import models
from django.utils.text import slugify
from django.core.validators import RegexValidator


class SchoolYear(models.Model):
    """ Um modelo para o ano letivo """

    name_message = 'Formato "aaaa/aaaa. Exemplo: 2022/2023'
    name_regex = RegexValidator(
        regex=r'^\d{4}\/\d{4}$',
        message=name_message,
    )
    name = models.CharField(
        'Designação',
        validators=[name_regex],
        max_length=12,
        unique=False,
        blank=False,
        help_text='Insira um ano letivo como o formato "aaaa/aaaa. Exemplo: 2022/2023'
    )
    slug = models.SlugField(
        max_length=20,
        unique=True,
        blank=True,
        help_text='Deixar em branco para criar um slug automático e único'
    )
    start_date = models.DateField(
        'Início',
        blank=True,
        null=True,
    )
    end_date = models.DateField(
        'Fim',
        blank=True,
        null=True,
    )
    created = models.DateTimeField(
        'Criado em',
        auto_now_add=True,
    )
    modified = models.DateTimeField(
        'Modificado em',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Ano Letivo'
        verbose_name_plural = 'Anos Letivos'
        ordering = ['name']

    def __str__(self):
        """returns the name of the object"""
        return self.name

    def get_absolute_url(self):
        pass

    def save(self, *args, **kwargs):
        """ Set an automatic and unique slug for the name of the class"""

        super(SchoolYear, self).save(*args, **kwargs)
        if not self.slug:
            self.slug = self.name.replace("/", "-") + '_' + str(self.id)
            self.save()


class School(models.Model):
    """ Um modelo para as Escolas do Agrupamento"""

    name = models.CharField(
        'Designação',
        max_length=254,
    )
    code_message = 'O código da Escola deve ter 6 dígitos.'
    code_regex = RegexValidator(
        regex=r'\d{6}$',
        message=code_message
    )
    code = models.CharField(
        'Código de Agrupamento',
        validators=[code_regex],
        max_length=10,
        blank=True,
        help_text='Introduza um código com 6 dígitos.'
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        blank=True,
        help_text='Deixar em branco para criar um slug automático e único'
    )
    address = models.TextField(
        'Morada',
        blank=True,
    )
    phone1 = models.CharField(
        'Telefone 1',
        max_length=12,
        blank=True,
    )
    phone2 = models.CharField(
        'Telefone 2',
        max_length=12,
        blank=True,
    )
    nif_message = 'o NIF deve ter 9 dígitos.'
    nif_regex = RegexValidator(
        regex=r'\d{9}$',
        message=nif_message
    )
    nif = models.CharField(
        'NIF',
        validators=[nif_regex],
        max_length=10,
        blank=True,

        help_text='Introduza um NIF com 9 dígitos.'
    )
    email = models.EmailField(
        'email',
        max_length=254,
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

    class Meta:
        verbose_name = 'Escola'
        verbose_name_plural = 'Escolas'
        ordering = ['name']

    def __str__(self):
        """returns the name of the object"""
        return self.name

    def get_absolute_url(self):
        pass

    def save(self, *args, **kwargs):
        """ Set an automatic and unique slug for the name of the class"""

        super(School, self).save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(self.name) + '_' + str(self.id)
            self.save()


class SchoolClass(models.Model):
    """Um modelo para as turmas"""

    school_year = models.ForeignKey(
        'SchoolYear',
        verbose_name='Ano Letivo',
        on_delete=models.CASCADE
    )
    school = models.ForeignKey(
        'School',
        verbose_name='Escola',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    teachers = models.ManyToManyField(
        'accounts.Teacher',
    )
    students = models.ManyToManyField(
        'accounts.Student',
    )
    name = models.CharField(
        'Designação da turma',
        max_length=20,
    )
    GRADE_OPTIONS = (
        ("1ºANO", "1ºAno"), ("2ºANO", "2ºAno"),
        ("3ºANO", "3ºAno"), ("4ºANO", "4ºAno"),
        ("5ºANO", "5ºAno"), ("6ºANO", "6ºAno"),
        ("7ºANO", "7ºAno"), ("8ºANO", "8ºAno"),
        ("9ºANO", "9ºAno"), ("PRE", "Pre-escola"),
    )
    grade = models.CharField(
        'Ano de Escolaridade',
        choices=GRADE_OPTIONS,
        max_length=12,
        default='9ºAno'
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        blank=True,
        help_text='Deixar em branco para criar um slug automático e único.'
    )
    created = models.DateTimeField(
        'Criado em',
        auto_now_add=True
    )
    modified = models.DateTimeField(
        'modificado em',
        auto_now=True
    )

    class Meta:
        verbose_name = "Turma"
        verbose_name_plural = "Turmas"
        ordering = ('name',)

    def __str__(self):
        """Return the str.name fom the object"""
        return self.name

    def get_absolute_url(self):
        pass

    def save(self, *args, **kwargs):
        """Set an automátic and unique slug from name and id fields"""
        super(SchoolClass, self).save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(self.name) + "-" + str(self.id)
            self.save()


class CargoDT(models.Model):
    """Um modelo para registar a função de Diretor de Turma """

    teacher_dt = models.ForeignKey(
        'accounts.Teacher',
        verbose_name='Turma',
        on_delete=models.CASCADE,
    )
    turma = models.OneToOneField(
        'SchoolClass',
        verbose_name='Turma',
        on_delete=models.CASCADE
    )
    school_year = models.ForeignKey(
        'SchoolYear',
        verbose_name='Ano Letivo',
        on_delete=models.CASCADE
    )
    created = models.DateTimeField(
        'Criado em',
        auto_now_add=True
    )
    modified = models.DateTimeField(
        'modificado em',
        auto_now=True
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        blank=True,
        help_text='Deixar em branco para criar um slug automático e único.'
    )

    class Meta:
        verbose_name = "Cargo de DT"
        verbose_name_plural = "Cargos de DT"
        ordering = ('teacher',)

    def __str__(self):
        """Return the str.name fom the object"""
        return self.teacher_dt.name

    def get_absolute_url(self):
        pass

    def save(self, *args, **kwargs):
        """Set an automátic and unique slug from name and id fields"""
        super(CargoDT, self).save(*args, **kwargs)
        if not self.slug:
            self.slug = "DT-" + slugify(self.teacher_dt.name) + "-" + str(self.id)
            self.save()
