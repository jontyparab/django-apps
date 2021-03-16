from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone

from django.views import View
from todo.models import Task


class Todo(LoginRequiredMixin, View):
    def get(self, request):
        tasks = Task.objects.filter(user=request.user).order_by('-datecompleted')
        return render(request, 'todo/todo.html', {'tasks': tasks})

    def post(self, request):
        checkboxes = request.POST.getlist('checklist')
        print(checkboxes)
        if 'completed' in checkboxes:
            datecompleted = timezone.now()
        else:
            datecompleted = None

        if request.POST['action'] == 'Create':
            # instance way of creating a record
            newTask = Task(title=request.POST['title'], description=request.POST['description'],
                           important=bool('important' in checkboxes), datecompleted=datecompleted, user=request.user)
            newTask.save()

        if request.POST['action'] == 'Update':
            # Direct way of updating or deleting a record ('cleanup' code is not executed, not an issue most of the time)
            Task.objects.filter(id=request.POST['pk']).update(title=request.POST['title'], description=request.POST['description'], important=bool('important' in checkboxes), datecompleted=datecompleted, user=request.user)

        if request.POST['action'] == 'Delete':
            Task.objects.filter(id=request.POST['pk']).delete()

        if request.POST['action'] == 'Done':
            print("WORKING")
            Task.objects.filter(id=request.POST['pk']).update(datecompleted=timezone.now())
        return HttpResponseRedirect(self.request.path_info)
