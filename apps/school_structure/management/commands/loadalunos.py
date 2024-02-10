from django.core.management.base import BaseCommand

from apps.accounts.models import User, Student, StudentMore


class Command(BaseCommand):
    """ Execução do comando na consola: python manage.py loadalunos """
    help = 'Carrega a base de dados com objetos do tipo alunos. ' \
           'Execução do comando na consola: python manage.py loadalunos.'

    def handle(self, *args, **kwargs):

        # caminho para o ficheiro
        path = 'apps/school_structure/utils/alunos_data.csv'

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
        Modelo Aluno
        fields = [ process_number, name, birth_date, phone, email, address, email_ee, name_ee, phone_ee_1, phone_ee_2]
        """

        if Student.objects.filter(process_number=fields[0]).exists():
            # Verifica se o aluno já existe na base de dados
            self.stdout.write(
                self.style.WARNING('O aluno(a) "%s" já está registado na BD!' % (fields[1])))
        else:
            # Cria aluno na base de dados
            try:
                User.objects.create(
                    process_number=fields[0],
                    name=fields[1],
                    birth_date=fields[2],
                    email=fields[3],
                    phone=fields[4],
                    type="STUDENT",
                )
                user = User.objects.get(process_number=fields[0])
                user.set_password(fields[10])
                user.save()
                StudentMore.objects.create(
                    user=user,
                    ee_email=fields[6],
                    ee_name=fields[7],
                    ee_phone=fields[8],
                )

                self.stdout.write(
                    self.style.SUCCESS('Aluno(a) "%s" - "%s" criado(a) com sucesso!' % (fields[0], fields[1])))
            except Exception as e:
                self.stdout.write(self.style.ERROR('%s (%s)' % (e, type(e))))
