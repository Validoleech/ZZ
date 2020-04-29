from django.db import models
from django.contrib.auth.models import User

class Grades(models.Model):
    id = models.IntegerField(primary_key=True)
    grade = models.IntegerField()
    date = models.DateTimeField()
    subject = models.CharField(max_length=12)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

class Olympics(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=12)
    description = models.TextField() # Описание олимпиады/хакатона
    date = models.DateTimeField() # Дата проведения
    theme = models.CharField(max_length=12) # Предмет, по которому проводится олимпиада

class OlympicsUsers(models.Model):
    olympic_id = models.ForeignKey(to=Olympics, on_delete=models.CASCADE)
    user_id = models.IntegerField()
    score = models.IntegerField()

class OtherAchievements(models.Model):
    description = models.TextField()
    theme = models.CharField(max_length=12)

