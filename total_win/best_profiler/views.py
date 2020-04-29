from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request):
    return HttpResponse("Hello world!")

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
    #TODO И так далее
    MaxMark = max(MathAvg+PhysicsAvg, MathAvg+InformaticsAvg) 
    if (MathAvg+PhysicsAvg) >
         score = MathAvg+PhysicsAvg / 2
