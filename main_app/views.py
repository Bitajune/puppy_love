from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Puppy, Toy
from .forms import FeedingForm


class PuppyCreate(LoginRequiredMixin, CreateView):
    model = Puppy
    fields = ['name', 'breed', 'description', 'age']
    success_url = '/puppies/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class PuppyUpdate(LoginRequiredMixin, CreateView):
    model = Puppy
    fields = ['breed', 'description', 'age']


class PuppyDelete(LoginRequiredMixin, CreateView):
    model = Puppy
    success_url = '/puppies/'


def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


@login_required
def puppies_index(request):
    puppies = Puppy.objects.filter(user=request.user)
    return render(request, 'puppies/index.html', {'puppies': puppies})


@login_required
def puppies_detail(request, puppy_id):
    puppy = Puppy.objects.get(id=puppy_id)
    toys_puppy_doesnt_have = Toy.objects.exclude(
        id__in=puppy.toys.all().values_list('id'))
    feeding_form = FeedingForm()
    return render(request, 'puppies/detail.html', {
        'puppy': puppy, 'feeding_form': feeding_form,
        'toys': toys_puppy_doesnt_have
    })


@login_required
def add_feeding(request, puppy_id):
    form = FeedingForm(request.POST)
    if form.is_valid():
        new_feeding = form.save(commit=False)
        new_feeding.puppy_id = puppy_id
        new_feeding.save()
    return redirect('detail', puppy_id=puppy_id)


def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)


@login_required
def assoc_toy(request, puppy_id, toy_id):
    Puppy.objects.get(id=puppy_id).toys.add(toy_id)
    return redirect('detail', puppy_id=puppy_id)


@login_required
def unassoc_toy(request, puppy_id, toy_id):
    Puppy.objects.get(id=puppy_id).toys.remove(toy_id)
    return redirect('detail', puppy_id=puppy_id)


class ToyList(LoginRequiredMixin, ListView):
    model = Toy


class ToyDetail(LoginRequiredMixin, DetailView):
    model = Toy


class ToyCreate(LoginRequiredMixin, CreateView):
    model = Toy
    fields = '__all__'


class ToyUpdate(LoginRequiredMixin, UpdateView):
    model = Toy
    fields = ['name', 'color']


class ToyDelete(LoginRequiredMixin, DeleteView):
    model = Toy
    success_url = '/toys/'
