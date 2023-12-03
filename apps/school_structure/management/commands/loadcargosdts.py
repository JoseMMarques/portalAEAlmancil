from django.core.management.base import BaseCommand, CommandError

from apps.school_structure.models import SchoolYear, SchoolClass, CargoDT
from apps.accounts.models import User, Teacher


class Command(BaseCommand):
    """ Execução do comando na consola: python manage.py loadescolas """
    help = 'Carrega a base de dados com objetos do tipo CargoDt. ' \
           'Execução do comando na consola: python manage.py loadcargosdts.'

    def handle(self, *args, **kwargs):

        # caminho para o ficheiro
        path = 'apps/school_structure/utils/cargoDT_data.csv'

        # tenta abrir o ficheiro txt na localização indicada
        try:
            file_data = open(path, encoding='utf8')
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('\nERRO: Ficheiro não encontrado em -> %s' % path))
            return

        # grava todos os objetos do ficheiro de dados na Base de Dados
        for line in file_data.readlines():
            model_fields = line.strip().split(',')

            self.save_object_in_db(model_fields)

    def save_object_in_db(self, fields):
        """
        modelo CargoDT
        fields = [ school_year, school_class, teacger_dt, secretary ]
        """

        if CargoDT.objects.filter(school_class__name=fields[1], school_year__name=fields[0]).exists():
            # Verifica se o CargoDT já existe na base de dados
            self.stdout.write(
                self.style.WARNING('CargoDT do "%s" de "%s" Já existe!' % (fields[1], fields[0])))
        else:
            # Cria Disciplina na base de dados
            try:
                school_year = SchoolYear.objects.get(name=fields[0])
                school_class = SchoolClass.objects.get(name=fields[1], school_year=school_year)
                teacher_dt = Teacher.objects.get(name=fields[2])
                secretary = Teacher.objects.get(name=fields[3])
                CargoDT.objects.create(
                    school_year=school_year,
                    school_class=school_class,
                    teacher_dt=teacher_dt,
                    secretary=secretary,
                )
                self.stdout.write(
                    self.style.SUCCESS('CargoDT "%s" de "%s" criado com sucesso!' % (fields[1], fields[0])))
            except Exception as e:
                self.stdout.write(self.style.ERROR('%s (%s)' % (e, type(e))))
