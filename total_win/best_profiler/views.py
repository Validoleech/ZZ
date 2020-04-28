from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request):
    return HttpResponse("Hello world!")

def avg_grade(id, subject):
    Grades = Grades.object.filter(user_id=request.user)
    sum = 0
    for i in range(len(Grades)):
        sum += Grades[i].grade
    return sum / len(Grades)

def direction():
    