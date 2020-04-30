from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from BestProfiler.forms import RegisterForm, LoginForm
from .models import Grades
from BestProfiler.menu import get_context_menu, REGISTER_PAGE_NAME, LOGIN_PAGE_NAME, USER_PAGE_NAME, USER_VIEW_PAGE_NAME, HOME_PAGE_NAME

# Create your views here.
def AvgGrade(id, subject):
    grade = Grades.objects.filter(user_id=id).filter(subject=subject)
    sum = 0
    for i in range(len(grade)):
        sum += grade[i].grade
    if len(grade) != 0:
        return sum / len(grade)
    else:
        return sum



def direction(id):
    MathAvg = AvgGrade(id, "math")
    PhysicsAvg = AvgGrade(id, "physics")
    InformaticsAvg = AvgGrade(id, "informatics")

    RussianAvg = AvgGrade(id, "rus")
    EnglishAvg = AvgGrade(id, "en")
    FrenchAvg = AvgGrade(id, "fr")

    CompScore = max(MathAvg + PhysicsAvg, MathAvg + InformaticsAvg, RussianAvg + EnglishAvg, RussianAvg + FrenchAvg,
                    FrenchAvg + EnglishAvg)

    if (MathAvg + PhysicsAvg) == CompScore:
        score = MathAvg + PhysicsAvg / 2
        orientation = "Физика; инженерия"
    if (MathAvg + InformaticsAvg) == CompScore:
        score = MathAvg + InformaticsAvg / 2
        orientation = "Информатика; программирование"
    if (RussianAvg + EnglishAvg) == CompScore:
        score = RussianAvg + EnglishAvg / 2
        orientation = "Лингвистика; перевод (английский)"
    if (RussianAvg + FrenchAvg) == CompScore:
        score = RussianAvg + FrenchAvg / 2
        orientation = "Лингвистика; перевод (французский)"
    if (EnglishAvg+FrenchAvg) == CompScore:
        score = EnglishAvg + FrenchAvg / 2
        orientation = "Лингвистика; перевод (многоязычность)"

    return score, orientation


def index(request):
    if request.user.is_authenticated:
        return redirect('/main_page')
    else:
        return redirect('/login')


def register_view(request):  # Регистрация в системе
    context = {'menu': get_context_menu(request, REGISTER_PAGE_NAME)}
    if request.method == 'POST':
        errors = []
        register_form = RegisterForm(request.POST or None)
        if register_form.is_valid():
            login_data = register_form.cleaned_data['login']
            password_data = register_form.cleaned_data['password']
            password_repeat_data = register_form.cleaned_data['password_repeat']

            context['form'] = RegisterForm()

            print(login_data, password_data)

            # if len(login_data) < 5:
            #    errors.append('Логин должен иметь длину больше 5 символов')

            if User.objects.filter(username=login_data).exists():
                errors.append('Пользователь с таким логином уже существует')

            # if len(password_data) < 6:
            #    errors.append('Пароль должен иметь длину больше 6 символов')

            if password_data != password_repeat_data:
                errors.append('Пароли не совпадают')

            if len(errors) == 0:
                user = User.objects.create_user(username=login_data, password=password_data)
                user.save()

                if user is not None:
                    # login(request, user)
                    # return redirect('/login')
                    return redirect('/main_page')

                return redirect('/main_page')
        else:
            errors.append('Заполните все поля')
        context['error'] = errors[0]
    else:
        context['form'] = RegisterForm()
    return render(request, 'register.html', context)


def login_view(request):  # Вход в систему
    context = {'menu': get_context_menu(request, LOGIN_PAGE_NAME)}
    if request.method == 'POST':
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            login_data = login_form.cleaned_data['login']
            password_data = login_form.cleaned_data['password']

            print(login_data)
            print(password_data)

            user = authenticate(request, username=login_data, password=password_data)

            if user is not None:
                login(request, user)
                return redirect('/main_page')

        context['error'] = 'Неверный логин или пароль'

        return render(request, 'login.html', context)
    else:
        context['form'] = LoginForm()
        return render(request, 'login.html', context)


def mainpage_view(request):
    context = {'menu': get_context_menu(request, HOME_PAGE_NAME)}

    score, orientation = direction(user_id)
    context['score'] = score
    context['orientation'] = orientation

    context = {"users": User.objects.all()}
    return render(request, 'main.html', context)


@login_required
def logout_view(request):
    logout(request)
    print("here")
    return redirect('/')


@login_required
def user_page_view(request, user_id):
    context = {'menu': get_context_menu(request, USER_PAGE_NAME)}

    user = User.objects.get(pk=user_id)

    perf = Grades.objects.filter(user_id=user_id)
    s = set()
    for i in perf:
        s.add(i.subject)
    score, orientation = direction(user_id)

    context['user'] = user
    context['predmet'] = s
    context["perfomance"] = perf

    context['score'] = score
    context['orientation'] = orientation

    return render(request, 'user.html', context)
