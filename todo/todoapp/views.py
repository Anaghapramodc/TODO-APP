from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import request
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, FormView, TemplateView
from .models import task


# Create your views here.


# def home(request):
#     return render(request,'home.html')

class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add any additional context variables here
        return context

class CustomLoginView(LoginView):
    template_name = 'login.html'
    fields = '--all--'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('task')

class RegisterView(FormView):
    template_name = 'register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('task')

    def form_valid(self,form):
        user = form.save()
        if user is not None:
            login(self.request,user)
            return super(RegisterView,self).form_valid(form)

    def get(self,*args,**kwargs):
        if self.request.user.is_authenticated:
            return redirect('task')
        return super(RegisterView,self).get(*args,**kwargs)




class CustomLogoutView(LogoutView):
    template_name = 'logout.html'
    next_page = reverse_lazy('home')

    def dispatch(self,request,*args,**kwargs):
        return super().dispatch(request,*args,**kwargs)






class TaskList(LoginRequiredMixin,ListView):
    model = task
    context_object_name = 'task'
    template_name = 'list.html'
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['task'] = context['task'].filter(user=self.request.user)
        context['count'] = context['task'].filter(completed=False).count()

        return context




class TaskCreate(LoginRequiredMixin,CreateView):
    model = task
    fields = ['title','description','completed']
    success_url = reverse_lazy('task-create')
    template_name = 'taskcreate.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate,self).form_valid(form)


class TaskUpdate(LoginRequiredMixin,UpdateView):
    model = task
    fields = ['title','description','completed']
    success_url = reverse_lazy('task')
    template_name = 'taskcreate.html'


class TaskDelete(LoginRequiredMixin,DeleteView):
    model = task
    fields = ['title', 'description', 'completed']
    success_url = reverse_lazy('task')
    template_name = 'taskdelete.html'

class TaskDetailView(LoginRequiredMixin,DetailView):
    model = task
    template_name = 'taskdetail.html'



