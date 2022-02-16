
from operator import imod
from django.contrib import admin

from .models import TodoModel

# Register your models here.

class TodoAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)

admin.site.register(TodoModel, TodoAdmin)