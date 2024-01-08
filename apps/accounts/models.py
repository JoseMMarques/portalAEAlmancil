from datetime import date

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.core.validators import RegexValidator
from django_resized import ResizedImageField


class UserManager(BaseUserManager):
    def create_user(self, name, email, password=None):
        if not email:
            raise ValueError('Utilizador tem que ter email!')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, email, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            name=name,
            password=password,

        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):

    class Types(models.TextChoices):
        TEACHER = "TEACHER", "Professor"
        STUDENT = "STUDENT", "Estudante"
        EMPLOYEE = "EMPLOYEE", "Funcionário"

    type = models.CharField(
        'Tipo',
        max_length=50,
        choices=Types.choices,
        default=Types.TEACHER
    )

    name = models.CharField(
        'Nome',
        max_length=254,
    )
    birth_date = models.DateField(
        'Data de nascimento',
        blank=True,
        null=True,
    )
    SEX_CHOICES = (
        ('M', 'Masculino'),
        ('F', 'Feminino'),
    )
    sex = models.CharField(
        'Sexo',
        choices=SEX_CHOICES,
        max_length=100,
        blank=True,
        null=True,
    )
    process_number = models.CharField(
        'Número do processo',
        max_length=15,
    )
    email = models.EmailField(
        'e-mail',
        max_length=254,
        unique=True,
    )
    phone = models.CharField(
        'Telemóvel',
        max_length=12,
        blank=True,
    )
    avatar = ResizedImageField(
        size=[185, 185],
        upload_to='users_fotos/',
        default='users_fotos/no_image.png',
        crop=['middle', 'center'],
        quality=75
    )
    address = models.TextField(
        'Morada',
        blank=True,
    )
    postal_code_message = 'Formato "nnnn-nnn". Exemplo: 8100-128'
    postal_code_regex = RegexValidator(
        regex=r'^\d{4}\-\d{3}$',
        message=postal_code_message,
    )
    postal_code = models.CharField(
        'Código Postal',
        validators=[postal_code_regex],
        max_length=12,
        unique=False,
        blank=True,
        help_text='Insira um código postal com o formato "nnnn-nnn. Exemplo: 8100-128'
    )
    locality = models.TextField(
        'Localidade',
        blank=True,
    )
    nif_message = ' O NIF deve conter 9 dígitos.'
    nif_regex = RegexValidator(
        regex=r'\d{9}$',
        message=nif_message
    )
    nif = models.CharField(
        'NIF',
        validators=[nif_regex],
        max_length=10,
        blank=True,
        help_text='Introduza um NIF com 9 dígitos',
        # unique=True, ainda não tenho os NIF dos alunos na Base de Dados
        # TODO: ter nifs dos alunos na base de dados e desconebtar este campo
    )
    nationality = models.CharField(
        'Nacionalidade',
        max_length=30,
        blank=True,
    )
    # required fields
    last_login = models.DateTimeField(
        'Último acesso',
        auto_now_add=True
    )
    created = models.DateTimeField(
        'Criado em',
        auto_now_add=True
    )
    modified = models.DateTimeField(
        'modificado em',
        auto_now=True
    )
    is_admin = models.BooleanField(
        'Administrador',
        default=False
    )
    is_staff = models.BooleanField(
        'Staff',
        default=False
    )
    is_active = models.BooleanField(
        'Conta ativa',
        default=False
    )
    is_superadmin = models.BooleanField(
        'Super Administrador',
        default=False
    )
    is_game = models.BooleanField(
        'Membro GAME',
        default=False
    )
    is_pias = models.BooleanField(
        'administrador dos PIAS',
        default=False
    )

    class Meta:
        """options (metadata) to the field"""
        verbose_name = "Utilizador"
        verbose_name_plural = "Todos os Utilizadores"
        ordering = ['type']

    def __str__(self):
        """Return the str.name fom the object"""
        return self.name

    def get_age(self):
        """return the age of the user from the birth_date"""
        today = date.today()
        if self.birth_date:
            return today.year - self.birth_date.year - (
                    (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
            )

    def get_first_name(self):
        """Get the user first name"""
        return str(self).split(" ")[0]

    def get_last_name(self):
        """get the user last name"""
        return str(self).split(" ")[-1]

    def get_short_name(self):
        """Get the user first name"""
        return str(self).split(" ")[0] + " " + str(self).split(" ")[-1]

    def get_type(self):
        """ Retorna o verbose name do tipo do utilizador.
        Útil para o formulário de participação disciplinar """

        if self.type == 'TEACHER':
            return "Professor"
        if self.type == 'STUDENT':
            return "Aluno"
        if self.type == 'EMPLOYEE':
            return "Funcionário"
        else:
            return "Outro"

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']


class TeacherManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.TEACHER)


class Teacher(User):
    base_type = User.Types.TEACHER
    objects = TeacherManager()

    @property
    def more(self):
        return self.teachermore

    class Meta:
        proxy = True
        verbose_name = "Professor"
        verbose_name_plural = "Professores"
        ordering = ('name',)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = User.Types.TEACHER
            # para encriptar a password
            self.set_password(self.password)
        return super().save(*args, **kwargs)


class TeacherMore(models.Model):
    """Um modelo para os professores da escola"""

    user = models.OneToOneField(
        Teacher,
        on_delete=models.CASCADE
    )
    # atualizar de OnetoOneField para ManyToManyField
    # school_class_dt = models.OneToOneField(    <--´
    #     'school_structure.SchoolClass',
    #     verbose_name='Direção de Turma',
    #     on_delete=models.CASCADE,
    #     blank=True,
    #     null=True,
    # )
    hobbies = models.CharField(
        'Interesses',
        max_length=200,
    )
    # is_dt = models.BooleanField(
    #     'DT',
    #     default=False
    # )

    # inserir atributo
    # cargo_dt = models.ManyToManyField(...)

    def __str__(self):
        """Return the str.name fom the object"""
        return self.user.name

    class Meta:
        verbose_name = "Prof ++"
        verbose_name_plural = "Profes ++"
        ordering = ('user',)


class StudentManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.STUDENT)


class Student(User):
    base_type = User.Types.STUDENT
    objects = StudentManager()

    class Meta:
        proxy = True
        verbose_name = "Aluno"
        verbose_name_plural = "Alunos"
        ordering = ('name',)

    @property
    def more(self):
        return self.studentmore

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = User.Types.STUDENT
            # para encriptar a password
            self.set_password(self.password)
        return super().save(*args, **kwargs)


class StudentMore(models.Model):
    """Um modelo para os alunos da escola"""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True
    )
    father_name = models.CharField(
        'Nome do Pai',
        max_length=150,
        blank=True,
    )
    father_phone = models.CharField(
        'Telemóvel do pai',
        max_length=12,
        blank=True,
    )
    father_work = models.CharField(
        'Profissão do pai',
        max_length=60,
        blank=True,
    )
    father_email = models.EmailField(
        'Email do pai',
        max_length=254,
        blank=True,
    )
    mother_name = models.CharField(
        'Nome da mãe',
        max_length=150,
        blank=True,
    )
    mother_phone = models.CharField(
        'Telemóvel da mãe',
        max_length=12,
        blank=True,
    )
    mother_work = models.CharField(
        'Profissão da mãe',
        max_length=60,
        blank=True,
    )
    mother_email = models.EmailField(
        'Email da mãe',
        max_length=254,
        blank=True,
    )
    ee_kinship = models.CharField(
        'Parentesco',
        max_length=50,
        blank=True,
    )
    ee_name = models.CharField(
        'Encarregado de Educação',
        max_length=150,
        blank=True,
    )
    ee_phone = models.CharField(
        'Telemóvel do EE',
        max_length=12,
        blank=True,
    )
    ee_work = models.CharField(
        'Profissão do EE',
        max_length=60,
        blank=True,
    )
    ee_email = models.EmailField(
        'Email do EE',
        max_length=254,
        blank=True,
    )

    class Meta:
        verbose_name = "Aluno ++"
        verbose_name_plural = "Alunos ++"
        ordering = ('user',)

    def __str__(self):
        """Return the str.name fom the object"""
        return self.user.name


class EmployeeManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.EMPLOYEE)


class Employee(User):
    base_type = User.Types.EMPLOYEE
    objects = EmployeeManager()

    class Meta:
        proxy = True
        verbose_name = "Funcionário"
        verbose_name_plural = "Funcionários"
        ordering = ('name',)

    @property
    def more(self):
        return self.employeemore

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = User.Types.EMPLOYEE
            # para encriptar a password
            self.set_password(self.password)
        return super().save(*args, **kwargs)


class EmployeeMore(models.Model):
    """Um modelo para os funcionários da escola"""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True
    )
    role = models.CharField(
        'Função',
        max_length=150,
        blank=True,
    )
    workplace = models.CharField(
        'Local de Trabalho',
        max_length=150,
        blank=True,
    )

    class Meta:
        verbose_name = "Funcionário ++"
        verbose_name_plural = "Funcionários ++"
        ordering = ('user',)

    def __str__(self):
        """Return the str.name fom the object"""
        return self.user.name
