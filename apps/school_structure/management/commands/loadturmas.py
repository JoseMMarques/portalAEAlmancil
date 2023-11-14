from django.core.management.base import BaseCommand, CommandError

from apps.school_structure.models import SchoolYear, School, SchoolClass
from apps.accounts.models import User, Teacher, Student


class Command(BaseCommand):
    """ Execução do comando na consola: python manage.py loadturmas """
    help = 'Carrega a base de dados com objetos do tipo Turmas. ' \
           'Execução do comando na consola: python manage.py loadturmas.'

    def handle(self, *args, **kwargs):

        # caminho para o ficheiro
        path = 'apps/school_structure/utils/turmas_data.csv'

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
        Modelo Turma
        fields = [ school_year, school, teachers, students, name, grade ]
        """

        if SchoolClass.objects.filter(name=fields[4], school_year__name=fields[0]).exists():
            # Verifica se a escola já existe na base de dados
            self.stdout.write(
                self.style.WARNING('Turma "%s" de "%s" já existe!' % (fields[4], fields[0])))
        else:
            # Cria Escola na base de dados
            try:
                school_year = SchoolYear.objects.get(name=fields[0])
                school = School.objects.get(name=fields[1])

                SchoolClass.objects.create(
                    school_year=school_year,
                    school=school,
                    name=fields[4],
                    grade=fields[5],
                )
                school_class = SchoolClass.objects.get(name=fields[4], school_year__name=fields[0])
                students = fields[3].split()

                for student in students:
                    try:
                        school_class.students.add(Student.objects.get(process_number=student))
                    except Exception as e:
                        self.stdout.write(self.style.ERROR('%s (%s) -> Student process number: %s' % (e, type(e), student)))

                self.stdout.write(
                    self.style.SUCCESS('Turma "%s" do ano letivo "%s" criada com sucesso!' % (fields[4], fields[0])))
            except Exception as e:
                self.stdout.write(self.style.ERROR('%s (%s)' % (e, type(e))))
