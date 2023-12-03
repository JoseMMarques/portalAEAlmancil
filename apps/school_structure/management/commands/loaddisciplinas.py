from django.core.management.base import BaseCommand, CommandError

from apps.school_structure.models import Subject, SchoolYear


class Command(BaseCommand):
    """ Execução do comando na consola: python manage.py loadescolas """
    help = 'Carrega a base de dados com objetos do tipo Disciplina. ' \
           'Execução do comando na consola: python manage.py loaddisciplinas.'

    def handle(self, *args, **kwargs):

        # caminho para o ficheiro
        path = 'apps/school_structure/utils/disciplinas_data.csv'

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
        modelo disciplina
        fields = [ school_year, name, short_name ]
        """

        if Subject.objects.filter(name=fields[1], school_year__name=fields[0]).exists():
            # Verifica se a disciplina já existe na base de dados
            self.stdout.write(
                self.style.WARNING('Disciplina "%s" Já existe!' % (fields[1])))
        else:
            # Cria Disciplina na base de dados
            try:
                school_year = SchoolYear.objects.get(name=fields[0])
                Subject.objects.create(
                    school_year=school_year,
                    name=fields[1],
                    short_name=fields[2],
                )
                self.stdout.write(
                    self.style.SUCCESS('Disciplina "%s" criada com sucesso!' % (fields[1])))
            except Exception as e:
                self.stdout.write(self.style.ERROR('%s (%s)' % (e, type(e))))
