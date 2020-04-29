from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from BestProfiler.forms import RegisterForm, LoginForm
# Create your views here.

def index(request):
    if request.user.is_authenticated:
        return redirect('/main_page')
    else:
        return redirect('/register')

def register_view(request):
    if request.method == 'POST':
        errors = []
        context = {}
        register_form = RegisterForm(request.POST or None)
        if register_form.is_valid():
            login_data = register_form.cleaned_data['login']
            password_data = register_form.cleaned_data['password']
            password_repeat_data = register_form.cleaned_data['password_repeat']

            print(login_data, password_data)

            #if len(login_data) < 5:
            #    errors.append('Логин должен иметь длину больше 5 символов')

            if User.objects.filter(username=login_data).exists():
                errors.append('Пользователь с таким логином уже существует')

            #if len(password_data) < 6:
            #    errors.append('Пароль должен иметь длину больше 6 символов')

            if password_data != password_repeat_data:
                errors.append('Пароли не совпадают')


            if len(errors) == 0:
                user = User.objects.create_user(username=login_data, password=password_data)
                user.save()

                if user is not None:
                    login(request, user)
                    return redirect('/')

                return redirect('/')
        else:
            errors.append('Заполните все поля')
        context['error'] = errors[0]
    else:
        register_form = RegisterForm()
    return render(request, 'register_auth.html', {'form': register_form})

def login_view(request):



    if not request.user.is_authenticated:
        if request.method == "POST":
            login_form = LoginForm(request.POST or None)


def AvgGrade(id, subject):
    Grades = Grades.object.filter(user_id=request.user)
    sum = 0
    for i in range(len(Grades)):
        sum += Grades[i].grade
    return sum / len(Grades)

def direction(id):
    MathAvg = AvgGrade(id, "math")
    PhysicsAvg = AvgGrade(id, "physics")
    InformaticsAvg = AvgGrade(id, "informatics")
    RussianAvg = AvgGrade(id, "rus")
    EnglishAvg = AvgGrage(id, "en")
    FrenchAvg = AvgGrade(id, "fr")
    # TODO И так далее
    MaxMark = max(MathAvg+PhysicsAvg, MathAvg+InformaticsAvg)
    # if (MathAvg+PhysicsAvg) >
    #      score = MathAvg+PhysicsAvg / 2

