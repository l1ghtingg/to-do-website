from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.base import kwarg_re

from .models import Task
from django.views.generic.list import ListView
from django.contrib.auth.views import LoginView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

class CustomLoginView(LoginView):
    template_name = 'myfirstapp/login.html'
    fields = ['title', 'description', 'complete']
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')

class RegisterView(FormView):
    template_name = 'myfirstapp/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterView, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterView, self).get(*args, **kwargs)


class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'

    def get_queryset(self):
        tasks = Task.objects.filter(user=self.request.user)
        search_input = self.request.GET.get('search-area', '')

        if search_input:
            tasks = tasks.filter(title__startswith=search_input)

        self.extra_context = {'search_input': search_input}

        return tasks


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = "myfirstapp/task.html"


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')


    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)

class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = '__all__'
    success_url = reverse_lazy('tasks')

class DeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')