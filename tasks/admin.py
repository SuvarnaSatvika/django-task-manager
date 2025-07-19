from django.contrib import admin

from tasks.models import Category
from tasks.models import Task

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "user"]

@admin.register(Task)
class TasksAdmin(admin.ModelAdmin):
    list_display = ["title", "description", "category", "priority", "due_date", "completed", "created_at", "user" ]



