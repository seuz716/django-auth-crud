from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.http import HttpResponse
from django.db.utils import IntegrityError
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import TaskForm
from .models import Task
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
def home(request):
    """
    Vista para mostrar la página de inicio.
    """
    return render(request, 'home.html')


def signup(request):
    """
    Vista para el registro de usuarios.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            password1 = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')
            if password1 != password2:
                messages.error(request, 'Las contraseñas no coinciden')
            else:
                username = form.cleaned_data.get('username')
                try:
                    user = User.objects.create_user(username=username, password=password1)
                    login(request, user)
                    messages.success(request, '¡Registro exitoso!')
                    return redirect('tasks')
                except IntegrityError as e:
                    messages.error(request, f'Error al crear el usuario: {str(e)}')
        else:
            errors = form.errors
            for field, error in errors.items():
                messages.error(request, f'{field}: {error}')
    else:
        form = UserCreationForm()
        
    return render(request, 'signup.html', {'form': form})






@login_required
def tasks(request):
    """
    Vista para mostrar las tareas del usuario.
    """
    try:
        tasks = Task.objects.filter(author=request.user, completed=False).order_by('-created_date')
    except ObjectDoesNotExist:
        tasks = []
    
    return render(request, 'tasks.html', {'tasks': tasks})

@login_required
def tasks_completed(request):
    """
    Vista para mostrar las tareas del usuario.
    """
    try:
        tasks = Task.objects.filter(author=request.user, completed=True)
    except ObjectDoesNotExist:
        tasks = []
    
    return render(request, 'tasks.html', {'tasks': tasks})




@login_required
def create_tasks(request):
    """
    Vista para crear las tareas del usuario.
    """
    try:
        if request.method == 'GET':
            form = TaskForm()
            return render(request, 'create_tasks.html', {'form': form})
        
        if request.method == 'POST':
            form = TaskForm(request.POST)
            if form.is_valid():
                task = form.save(commit=False)
                task.author = request.user
                task.save()
                messages.success(request, 'Task created successfully!')
                return redirect('tasks')  # Redirige al usuario a la página de tareas
        
        # Si ocurre un error de ValueError al procesar la solicitud POST
        raise ValueError('Please provide valid data')
    
    except ValueError as e:
        messages.error(request, str(e))
        return redirect('tasks')  # Redirige al usuario a la página de tareas

    form = TaskForm()
    return render(request, 'create_tasks.html', {'form': form})


@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, pk=task_id, author=request.user)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('tasks')
    else:
        form = TaskForm(instance=task)

    return render(request, 'task_detail.html', {'task': task, 'form': form})

from django.shortcuts import get_object_or_404, redirect

@login_required
def delete_task(request, task_id):
    """
    Vista para eliminar una tarea.
    """
    try:
        task = get_object_or_404(Task, pk=task_id, author=request.user)

        if request.method == 'POST':
            task.delete()
            return redirect('tasks')

        return render(request, 'task_detail.html', {'task': task})

    except Task.DoesNotExist:
        return redirect('tasks')
  

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, author=request.user)

    if request.method == 'POST':
        task.completed = True
        task.published_date = timezone.now()
        task.save()
        return redirect('tasks')

    return render(request, 'task_detail.html', {'task': task})

@login_required
def signout(request):
    """
    Vista para cerrar sesión del usuario.
    """
    logout(request)
    return redirect('home')

def signin(request):
    """
    Vista para iniciar sesión del usuario.
    """
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, '¡Inicio de sesión exitoso!')
            return redirect('tasks')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
            return redirect('signin')
    else:
        form = AuthenticationForm()
        return render(request, 'signin.html', {'form': form})
