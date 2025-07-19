from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.contrib import messages

from tasks.models import Category, Task
from tasks.templates.tasks.forms import TaskForm, CategoryForm


# Create your views here.

def home(request):
    return render(request, 'tasks/home.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account Created Successfully')
            return redirect('tasks:login')
    else:
        form = UserCreationForm()

    return render(request, 'tasks/signup.html', {'form' : form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data = request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('tasks:dashboard')
    else:
        form = AuthenticationForm()

    return render(request, 'tasks/login.html', {'form' : form})

def user_logout(request):
    logout(request)
    return redirect('tasks:login')

@login_required
def dashboard(request):
    status = request.GET.get('status', '')
    priority = request.GET.get('priority', '')
    tasks = Task.objects.filter(user=request.user)
    if status:
        tasks = tasks.filter(completed=(status == 'completed'))
    if priority:
        tasks = tasks.filter(priority=priority)
    categories = Category.objects.filter(user=request.user)
    return render(request, 'tasks/dashboard.html', {'tasks': tasks, 'categories': categories})

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST, user=request.user)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, 'Task created!')
            return redirect('tasks:dashboard')
    else:
        form = TaskForm(user=request.user)
    return render(request, 'tasks/task_form.html', {'form': form})

@login_required
def task_edit(request, pk):
    task = Task.objects.get(pk=pk, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated!')
            return redirect('tasks:dashboard')
    else:
        form = TaskForm(instance=task, user=request.user)
    return render(request, 'tasks/task_form.html', {'form': form})

@login_required
def task_delete(request, pk):
    task = Task.objects.get(pk=pk, user=request.user)
    task.delete()
    messages.success(request, 'Task deleted!')
    return redirect('tasks:dashboard')

@login_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            messages.success(request, 'Category created!')
            return redirect('tasks:dashboard')
    else:
        form = CategoryForm()
    return render(request, 'tasks/category_form.html', {'form': form})

@login_required
def task_toggle_complete(request, pk):
    task = Task.objects.get(pk=pk, user=request.user)
    task.completed = not task.completed  # Toggle the completed status
    task.save()
    messages.success(request, f"Task marked as {'Completed' if task.completed else 'Pending'}")
    return redirect('tasks:dashboard')