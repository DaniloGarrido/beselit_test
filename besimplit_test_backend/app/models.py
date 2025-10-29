from django.db import models

# Create your models here.
#Modelo Task especificado en el enunciado
class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)