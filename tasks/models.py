from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Task(models.Model):
    priority_choices = (
        ('1', 'Urgent & Important'),
        ('2', 'Not Urgent & Important'),
        ('3', 'Urgent & Not Important'),
        ('4', 'Not Urgent & Not Important'),
    )
    title = models.CharField(max_length=100)
    description = models.TextField(blank = True, max_length=255)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null= True, blank= True, default='Miscellaneous')
    priority = models.CharField(max_length=1, choices=priority_choices)
    due_date = models.DateField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title