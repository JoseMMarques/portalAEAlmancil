from django.core.management.base import BaseCommand, CommandError

from apps.school_structure.models import School


class Command(BaseCommand):
    """ Execução do comando na consola: python manage.py loadescolas """
    help = 'Carrega a base de dados com objetos do tipo Escola. ' \
           'Execução do comando na consola: python manage.py loadescolas.'

    def handle(self, *args, **kwargs):

        # caminho para o ficheiro
        path = 'apps/school_structure/utils/escolas_data.csv'

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
        fields = [ name, code, address, phone1, phone2, NIF, email, diretor, coordenador ]
        """

        if School.objects.filter(name=fields[0]).exists():
            # Verifica se a escola já existe na base de dados
            self.stdout.write(
                self.style.WARNING('Escola "%s" Já existe!' % (fields[0])))
        else:
            # Cria Escola na base de dados
            try:
                School.objects.create(
                    name=fields[0],
                    code=fields[1],
                    address=fields[2],
                    phone1=fields[3],
                    phone2=fields[4],
                    nif=fields[5],
                    email=fields[6],
                    diretor=fields[7],
                    coordenador=fields[8],
                )
                self.stdout.write(
                    self.style.SUCCESS('Escola "%s" criada com sucesso!' % (fields[0])))
            except Exception as e:
                self.stdout.write(self.style.ERROR('%s (%s)' % (e, type(e))))
