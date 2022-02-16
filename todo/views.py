
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .models import TodoModel
from django.utils import timezone
from django.contrib.auth.decorators import login_required # декоратор, помечаем функции которые не должны работтеь если ты не зарег
# Create your views here.

def home(request):
    return render(request, 'todo/home.html')

def loginuser(request):
    if request.method == 'GET': # * 
        return render(request, 'todo/loginuser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password']) # *создаем объект пользователя и берем имя и пароль из request
        if user is None: # * если пароль или логин не совпадает
            return render(request, 'todo/loginuser.html', {'form': AuthenticationForm(), 'error': 'Username and password did not match'}) # * возвращаем окно логинюзер с ошибкой
        else: # * если удалось аутентифицироваться
            login(request, user) # ! что бы после логина пользователь был на странице аккаунта
            return redirect('currenttodos') # ! перенаправляем на страницу пользователя



def signupuser(request):
    if request.method == 'GET': # * 
        return render(request, 'todo/signupuser.html', {'form': UserCreationForm()})
    else:
        # create new user 
        if request.POST['password1'] == request.POST['password2']: # ! проверяем пароль1 и пароль2 из POST 
            try: # ! если имя уникальное создадим пользователя
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1']) # user object
                user.save() # save user
                login(request, user) # ! что бы после логина пользователь был на странице аккаунта
                return redirect('currenttodos') # ! перенаправляем на страницу пользователя
            except IntegrityError: # ! если имя занято 
                return render(request, 'todo/signupuser.html', {'form': UserCreationForm(), 'error': 'this name has alredy taken. Choose another'})
        else: #  ! если пароли заняты
            return render(request, 'todo/signupuser.html', {'form': UserCreationForm(), 'error': 'Password did not match'})        


@login_required
def logoutuser(request):
    if request.method == 'POST': # потому что некотрые браузеры автоматом обрабатываеют get запросы
        logout(request)
        return redirect('home')


@login_required
def currenttodos(request):
    todos = TodoModel.objects.filter(user = request.user, datecomplited__isnull=True) # записываем в переменную все незаершенные тудушки юзера
    return render(request, 'todo/currenttodos.html', {'todos': todos}) # 


@login_required
def complitedtodos(request):  # завершенный 
    #   записываем в переменную все завершенные тудушки юзера                        остортировано по дате
    todos = TodoModel.objects.filter(user = request.user, datecomplited__isnull=False).order_by('-datecomplited')
    return render(request, 'todo/complitedtodos.html', {'todos': todos}) # 


@login_required
def completetodo(request, todo_pk): # принимаем ключ записи
    todo = get_object_or_404(TodoModel, pk=todo_pk, user=request.user)   #  задачи именно этого юзера
    if request.method == 'POST': #
        todo.datecomplited = timezone.now() # * в случае выполнения задачи будет заполнять текущим датой и временем
        todo.save() # сохраняем
        return redirect('currenttodos') # 


@login_required
def deletetodo(request, todo_pk): # принимаем ключ записи
    todo = get_object_or_404(TodoModel, pk=todo_pk, user=request.user)   #  задачи именно этого юзера
    if request.method == 'POST': #
        todo.delete() # удалеяем
        return redirect('currenttodos') # 

# * открытие определенной тудушки с описанием
@login_required
def viewtodo(request, todo_pk): # в параметры добавили ключ записи
    todo = get_object_or_404(TodoModel, pk=todo_pk, user=request.user)  # может открыать только юзер, чья тудушка 
    if request.method == 'GET': # если получаем запрос то отправлет на страницу редактирования тудушки
        form = TodoForm(instance=todo)  # описанеи будет в форме в отдельном окне
        return render(request, 'todo/viewtodo.html', {'todo': todo, 'form':form}) # 
    else: # если уже там
        try:
            form = TodoForm(request.POST, instance=todo)   #  попробуем отправить и сохранить изменения
            form.save()    #
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/viewtodo.html', {'todo': todo, 'form':form, 'error': 'bad info'}) #  если ошибка скажем об этом 


@login_required  
def createtodo(request): #
    if request.method == 'GET': #
        return render(request, 'todo/createtodo.html', {'form': TodoForm()}) # передаем созданную форму для создания туду
    else: #
        try:
            form = TodoForm(request.POST) # передаем из форму то что ввели
            newtodo = form.save(commit=False) # сохраняем данные в БД и записываем в переменную
            newtodo.user = request.user # привязваем к пользователю указывая его
            newtodo.save() #  сохраням в БД
            return redirect('currenttodos') # перенапраляем на список записей
        except ValueError:
            return render(request, 'todo/createtodo.html', {'form': TodoForm(), 'error': 'bad data past in'}) # если введени слишком много символов в title
