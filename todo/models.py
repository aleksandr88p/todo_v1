
from django.db import models
# from django.test import modify_settings
from django.contrib.auth.models import User


# Create your models here.
class TodoModel(models.Model):
    title = models.CharField(max_length=150) # заголовок
    memo = models.TextField(blank=True) # описание (blank=True  делает поле не обязательным к заполнению) 
    created = models.DateTimeField(auto_now_add=True) # дата и время создания записи    auto_now_add=True -  будет создаваться автоматом
    datecomplited = models.DateTimeField(null=True, blank=True) # до какой даты нужно сделать (blank=True  делает поле не обязательным к заполнению) 
    #duration_time = models.DurationField() # продолжительность
    importanat = models.BooleanField(default=False) # важно или нет (по умолчанию не важно)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):  # *  что бы в админке было понятней видно тудушки
        return self.title  