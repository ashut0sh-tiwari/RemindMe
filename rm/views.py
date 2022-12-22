from dataclasses import fields
from turtle import title
from django.shortcuts import render, redirect
# from django.http import HttpResponse
from django.views.generic.list import ListView #use to display data
from django.views.generic.detail import DetailView #used to display detailed list data
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView #used to create,update data 

# from rm.models import Notes #used to display list data
from .models import Notes #use to import model data
from django.urls import reverse_lazy #used to redirect page to url using name
from django.contrib.auth.views import LoginView #login view is used to render a login page 
from django.contrib.auth.forms import UserCreationForm #use to render django form
from django.contrib.auth import login #use to save the user info from register page and directly logged them in

from django.contrib.auth.mixins import LoginRequiredMixin #this login mixin import is used to authorize user and we can pass this as arguement in parameters to authorise user access

# Create your views here.

# def home(request):
#     return HttpResponse('hello home')

class HomeLogin(LoginView): #login page which is used to login user to the website
    template_name = 'rm/login.html' # it takes default template name which can be changed by this method
    fields = '__all__' #takes default fields
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('homelist') #redirecting user to the home page

class HomeRegister(FormView):
    template_name = 'rm/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('homelist')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(HomeRegister, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('homelist')
        return super(HomeRegister, self).get(*args, **kwargs)


class HomeList(LoginRequiredMixin, ListView): #ListView takes default html template with models name_list.html
    model = Notes
    context_object_name = 'notes' #it takes data as object name which can be changed by this context function
    template_name = 'rm/home.html' # it takes default template name which can be changed by this method

    def get_context_data(self, **kwargs):# function is used to show their individual data to every user
        context = super().get_context_data(**kwargs)
        context['notes'] = context['notes'].filter(user=self.request.user)
        context['count'] = context['notes'].filter(complete=False).count()
        search_input = self.request.GET.get('search') or ''
        if search_input:
            context['notes'] = context['notes'].filter(title__icontains=search_input)
        context['search_input'] = search_input
        return context
        

class HomeDetail(LoginRequiredMixin, DetailView): #detailview takes default html template with models name_detail.html
    model = Notes
    context_object_name = 'notes' #it takes data as object name which can be changed by this context function
    template_name = 'rm/detail.html' # it takes default template name which can be changed by this method

class HomeCreate(LoginRequiredMixin, CreateView): #createview takes default html template with models name_form.html
    model = Notes
    # context_object_name = 'notes' #it takes data as object name which can be changed by this context function
    fields = ['title', 'desc', 'complete'] #createview automatically makes form using models value
    template_name = 'rm/create.html' # it takes default template name which can be changed by this method
    success_url = reverse_lazy('homelist') #takes url names as arguement to redirect to that page
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(HomeCreate, self).form_valid(form)

class HomeUpdate(LoginRequiredMixin, UpdateView): #createview takes default html template with models name_form.html
    model = Notes
    # context_object_name = 'notes' #it takes data as object name which can be changed by this context function
    fields = ['title', 'desc', 'complete'] #createview automatically makes form using models value
    template_name = 'rm/create.html' # it takes default template name which can be changed by this method
    success_url = reverse_lazy('homelist') #takes url names as arguement to redirect to that page


class HomeDelete(LoginRequiredMixin, DeleteView): #createview takes default html template with models name_form.html
    model = Notes
    context_object_name = 'notes' #it takes data as object name which can be changed by this context function
    # fields = '__all__' #createview automatically makes form using models value
    template_name = 'rm/delete.html' # it takes default template name which can be changed by this method
    success_url = reverse_lazy('homelist') #takes url names as arguement to redirect to that page