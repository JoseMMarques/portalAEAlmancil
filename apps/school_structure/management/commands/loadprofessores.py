from django.core.management.base import BaseCommand

from apps.accounts.models import User, Teacher, TeacherMore


class Command(BaseCommand):
    """ Execução do comando na consola: python manage.py loadprofessores """
    help = 'Carrega a base de dados com objetos do tipo alunos. ' \
           'Execução do comando na consola: python manage.py loadprofessores.'

    def handle(self, *args, **kwargs):

        # caminho para o ficheiro
        path = 'apps/school_structure/utils/professores_data.csv'

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
        Modelo professor
        fields = [ process_number, name, birth_date, phone, email, phone, address, password]
        """

        if Teacher.objects.filter(process_number=fields[0]).exists():
            # Verifica se o professor já existe na base de dados
            self.stdout.write(
                self.style.WARNING('Professor(a) "%s" já está registado(a) na BD!' % (fields[1])))
        else:
            # Cria aluno na base de dados
            try:
                User.objects.create(
                    process_number=fields[0],
                    name=fields[1],
                    email=fields[4],
                    phone=fields[5],
                    type="TEACHER",
                )
                user = User.objects.get(process_number=fields[0])
                user.set_password(fields[7])
                user.save()
                TeacherMore.objects.create(
                    user=user,
                    hobbies="xadrez",
                )

                self.stdout.write(
                    self.style.SUCCESS('Professor(a) "%s" - "%s" criado(a) com sucesso!' % (fields[0], fields[1])))
            except Exception as e:
                self.stdout.write(self.style.ERROR('%s (%s)' % (e, type(e))))
