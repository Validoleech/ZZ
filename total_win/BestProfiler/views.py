from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from BestProfiler.forms import RegisterForm, LoginForm
from .models import Grades


# Create your views here.

def index(request):
    if request.user.is_authenticated:
        return redirect('/main_page')
    else:
        return redirect('/login')


def register_view(request):  # Регистрация в системе
    context = {}
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
    return render(request, 'register_auth.html', context)


def login_view(request):  # Вход в систему
    context = {}
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
        return render(request, 'login.html', {"form": LoginForm()})


def mainpage_view(request):
    context = {"users": User.objects.all()}
    return render(request, 'main.html', context)


@login_required
def logout_view(request):
    logout(request)
    print("here")
    return redirect('/')


def AvgGrade(id, subject):
    grade = Grades.object.filter(user_id=id).filter(subject=subject)
    sum = 0
    for i in range(len(grade)):
        sum += grade[i].grade
    return sum / len(grade)



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


@login_required
def user_page_view(request, user_id):
    context = {}

    user = User.objects.get(pk=user_id)

    perf = Grades.objects.filter(user_id=user_id)

    context['user'] = user

    context["perfomance"] = perf



    return render(request, 'user.html', context)
