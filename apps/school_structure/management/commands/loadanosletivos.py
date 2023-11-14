from django.core.management.base import BaseCommand, CommandError

from apps.school_structure.models import SchoolYear


class Command(BaseCommand):
    """ Execução do comando na consola: python manage.py loadanosletivos """
    help = 'Carrega a base de dados com objetos do tipo Ano_letivo. ' \
           'Execução do comando na consola: python manage.py loadanosletivos.'

    def handle(self, *args, **kwargs):

        # caminho para o ficheiro
        path = 'apps/school_structure/utils/anos_letivos_data.csv'

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
        modelo ano_letivo
        fields = [ name, start_date, end_date ]
        """
        if SchoolYear.objects.filter(name=fields[0]).exists():
            # Verifica se a escola já existe na base de dados
            self.stdout.write(
                self.style.WARNING('Ano Letivo "%s" Já existe!' % (fields[0])))
        else:
            # Cria Ano Letivo na base de dados
            try:
                SchoolYear.objects.create(
                    name=fields[0],
                    start_date=fields[1],
                    end_date=fields[2],
                )
                self.stdout.write(
                    self.style.SUCCESS('Ano Letivo "%s " criado com sucesso!' % (fields[0])))
            except Exception as e:
                self.stdout.write(self.style.ERROR('%s (%s)' % (e, type(e))))
