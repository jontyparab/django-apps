from django.contrib import admin

from todo.models import Task


class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ['created']


admin.site.register(Task, TaskAdmin)
