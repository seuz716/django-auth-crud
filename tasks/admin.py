from django.contrib import admin
from .models import Task

class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ("created_date",)  # Agrega una coma después de "created_date" para convertirlo en una tupla

admin.site.register(Task, TaskAdmin)



		