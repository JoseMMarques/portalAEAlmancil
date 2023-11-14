# Generated by Django 4.2.6 on 2023-11-14 17:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('type', models.CharField(choices=[('TEACHER', 'Professor'), ('STUDENT', 'Estudante'), ('EMPLOYEE', 'Funcionário')], default='TEACHER', max_length=50, verbose_name='Tipo')),
                ('name', models.CharField(max_length=254, verbose_name='Nome')),
                ('birth_date', models.DateField(blank=True, null=True, verbose_name='Data de nascimento')),
                ('sex', models.CharField(blank=True, choices=[('M', 'Masculino'), ('F', 'Feminino')], max_length=100, null=True, verbose_name='Sexo')),
                ('process_number', models.CharField(blank=True, max_length=15, verbose_name='Número do processo')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='e-mail')),
                ('phone', models.CharField(blank=True, max_length=12, verbose_name='Telemóvel')),
                ('address', models.TextField(blank=True, verbose_name='Morada')),
                ('last_login', models.DateTimeField(auto_now_add=True, verbose_name='Último acesso')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modificado em')),
                ('is_admin', models.BooleanField(default=False, verbose_name='Administrador')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Staff')),
                ('is_active', models.BooleanField(default=False, verbose_name='Conta ativa')),
                ('is_superadmin', models.BooleanField(default=False, verbose_name='Super Administrador')),
                ('is_game', models.BooleanField(default=False, verbose_name='Membro GAME')),
                ('is_pias', models.BooleanField(default=False, verbose_name='administrador dos PIAS')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Utilizador',
                'verbose_name_plural': 'Todos os Utilizadores',
                'ordering': ['type'],
            },
        ),
        migrations.CreateModel(
            name='EmployeeMore',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('role', models.CharField(blank=True, max_length=150, verbose_name='Função')),
                ('workplace', models.CharField(blank=True, max_length=150, verbose_name='Local de Trabalho')),
            ],
            options={
                'verbose_name': 'Funcionário ++',
                'verbose_name_plural': 'Funcionários ++',
                'ordering': ('user',),
            },
        ),
        migrations.CreateModel(
            name='StudentMore',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('name_ee', models.CharField(blank=True, max_length=150, verbose_name='Encarregado de Educação')),
                ('email_ee', models.EmailField(blank=True, max_length=254, verbose_name='Email do EE')),
                ('phone_ee_1', models.CharField(blank=True, max_length=12, verbose_name='Telemóvel 1 do EE')),
                ('phone_ee_2', models.CharField(blank=True, max_length=12, verbose_name='Telemóvel 2 do EE')),
            ],
            options={
                'verbose_name': 'Aluno ++',
                'verbose_name_plural': 'Alunos ++',
                'ordering': ('user',),
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
            ],
            options={
                'verbose_name': 'Funcionário',
                'verbose_name_plural': 'Funcionários',
                'ordering': ('name',),
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('accounts.user',),
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
            ],
            options={
                'verbose_name': 'Aluno',
                'verbose_name_plural': 'Alunos',
                'ordering': ('name',),
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('accounts.user',),
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
            ],
            options={
                'verbose_name': 'Professor',
                'verbose_name_plural': 'Professores',
                'ordering': ('name',),
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('accounts.user',),
        ),
        migrations.CreateModel(
            name='TeacherMore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subjects', models.CharField(max_length=200, verbose_name='Disciplinas')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='accounts.teacher')),
            ],
            options={
                'verbose_name': 'Prof ++',
                'verbose_name_plural': 'Profes ++',
                'ordering': ('user',),
            },
        ),
    ]
