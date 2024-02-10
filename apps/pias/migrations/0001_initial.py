# Generated by Django 4.2.6 on 2024-02-10 20:47

import apps.pias.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('school_structure', '0001_initial'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PiasType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300, verbose_name='Tipo')),
                ('description', models.TextField(blank=True, verbose_name='Descrição')),
                ('slug', models.SlugField(blank=True, help_text='Deixar em branco para criar um slug automático e único', max_length=255, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('modified', models.DateTimeField(auto_now_add=True, verbose_name='Modificado em')),
            ],
            options={
                'verbose_name': 'Tipo de Documento',
                'verbose_name_plural': 'Tipos de Documentos',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='PIAS',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Nome')),
                ('doc_date', models.DateField(blank=True, null=True, verbose_name='Data do documento')),
                ('description', models.TextField(blank=True, verbose_name='Descrição')),
                ('slug', models.SlugField(blank=True, help_text='Deixar em branco para criar um slug automático e único', max_length=250, unique=True)),
                ('uploaded_to', models.FileField(max_length=500, upload_to=apps.pias.models.path_and_rename)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Modificado em')),
                ('related_docs', models.ManyToManyField(blank=True, related_name='documentos_relacionados', to='pias.pias', verbose_name='Documentos relacionados')),
                ('school_year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school_structure.schoolyear', verbose_name='Ano Letivo')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.student', verbose_name='Aluno')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pias.piastype', verbose_name='Tipo')),
            ],
            options={
                'verbose_name': 'PIA',
                'verbose_name_plural': "PIA's",
                'ordering': ['name'],
            },
        ),
    ]
