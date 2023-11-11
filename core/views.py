from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.accounts.models import User, Student, Teacher


def landing_page(request):
    """Função que gera a página inicial da plataforma"""

    template_name = "core/landing_page.html"
    return render(request, template_name)


@login_required(login_url='/users/login/')
def user_homepage(request):
    template_name = 'core/user_homepage.html'
    context = {}
    user = User.objects.get(id=request.user.id)
    print('request user')
    print(user)

    # as minhas participações disciplinares
    # my_complaits = Complaint.objects.filter(user=user).order_by('-created')
    # context['my_complaints'] = my_complaits
    print('Base')
    print(context)

    # Se diretor turma
    # lista com participações da minha direcao de turma
    # if user.type == user.Types.TEACHER:
    #     teacher = Teacher.objects.get(id=user.id)
    #     print('teacher')
    #     print(teacher)
    #     try:
    #         # para o caso do professor não ter dados na classe TeacherMore
    #         if teacher.teachermore.is_dt:
    #             turma = teacher.teachermore.school_class_dt
    #             print(turma)
    #             my_dt_complaints = Complaint.objects.filter(turma=turma).order_by('-created')
    #             context['my_dt_complaints'] = my_dt_complaints
    #             print('ProfDT')
    #             print(context['my_dt_complaints'])
    #     except:
    #         print('o professor não é DT')

    # Se user for do GAME
    # listar participações de todos os alunos da escola  :)
    if user.is_game:
        # all_complaints = Complaint.objects.all().order_by('-created')
        # context['all_complaints'] = all_complaints
        print('MembroGame')
        # print(context['all_complaints'])

    return render(request, template_name, context)
