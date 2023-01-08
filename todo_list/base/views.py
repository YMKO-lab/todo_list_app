from django.shortcuts import render, redirect
#from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView

from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import login

from .models import Task

# Create your views here.

class CustomLoginView(LoginView):
     template_name = 'base/login.html'
     fields = '__all__'
     redirect_authenticated_user = True

     def get_success_url(self):
          return reverse_lazy('tasks')

class RegisterPage(FormView):
     template_name = 'base/register.html'
     form_class = UserCreationForm
     redirect_authenticated_user = True
     success_url = reverse_lazy('task')

     def form_valid(self, form):
          user = form.save()
          if user is not None:
               login(self.request, user)
          return super(RegisterPage, self).form_valid(form)

     def get(self, *args, **kwargs):
          if self.request.user.is_authenticated:
               return redirect('tasks')
          return super(RegisterPage, self).get(*args, **kwargs)     





class TaskList(LoginRequiredMixin, ListView):
     # This will create a list that displays a list of all tasks in the database
     # The 'model' attribute specifies the model that the view will use to retrieve
     # the list of objects.
     model = Task
     
     # The list of tasks will be passed to the template as a variable named 'tasks'
     # You can then access the list of tasks in the template using the 'tasks' variable
     context_object_name = 'tasks'


     def get_context_data(self, **kwargs):
          context = super().get_context_data(**kwargs)
          context['tasks'] = context['tasks'].filter(user=self.request.user)
          context['count'] = context['tasks'].filter(complete=False).count()
          return context

class TaskDetail(LoginRequiredMixin, DetailView):
     model = Task
     context_object_name = 'task'
     template_name = 'base/task.html'


class TaskCreate(LoginRequiredMixin, CreateView):
     model = Task
     
     # 'fields' attribute to specify the fields that should be included in the form.
     # In this case, you are using the "__all__" value to include all fields in the form.
     
     # Changed to "title", "description", "complete"
     fields = ['title', 'description', 'complete']
     
     # 'success_url' attribute to specify the URL to redirect to after the form 
     # submission is successful.
     # Using the 'reverse_lazy' function to reverse the URL pattern named "tasks".
     # This will redirect the user to the "tasks" URl after the form submission is 
     # successful. 
     success_url = reverse_lazy('tasks')

     def form_invalid(self, form):
          form.instance.user = self.request.user
          return super(TaskCreate, self).form_valid(form)

          

# The 'UpdateView' class provides a convenient way to handle the form submission and
# update the object in the database.
class TaskUpdate(LoginRequiredMixin, UpdateView):
     model = Task
     fields = ['title', 'description', 'complete']
     success_url = reverse_lazy('tasks')


# The "DeleteView" class provides a convenient way to handle the deletion
# of an object from the database
class DeleteView(LoginRequiredMixin, DeleteView):
     model = Task
     context_object_name = 'task'
     success_url = reverse_lazy('tasks')
     




