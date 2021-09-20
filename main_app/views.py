
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.views.generic import ListView, DetailView
from .models import Finch, Toy, Photo
from .forms import FeedingForm
import os
import uuid
import boto3


# Create your views here.

# class Finches:
#     def __init__(self, name, breed, description, age):
#         self.name = name
#         self.breed = breed
#         self.description = description
#         self.age = age

# finches = [
#     Finches('Taco','taco','tacotacos',3),
#     Finches('Burritto','burritto','burriburri',6),
#     Finches('Casa','casa','casacasaasa',2)
# ]

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def finches_index(request):
    finches = Finch.objects.all()
    return render(request, 'finches/index.html',{
        'finches': finches
    })

def finches_detail(request, finch_id):
    finch = Finch.objects.get(id=finch_id)
    toys_finch_doesnt_have = Toy.objects.exclude(id__in = finch.toys.all().values_list('id'))
    feeding_form = FeedingForm()
    return render(request,'finches/detail.html',{
        'finch': finch,
        'feeding_form': feeding_form,
        'toys': toys_finch_doesnt_have
    })

class FinchCreate(CreateView):
    model = Finch
    fields = ['name', 'breed','description','age']

class FinchUpdate(UpdateView):
    model = Finch
    fields = '__all__'

class FinchDelete(DeleteView):
    model = Finch
    success_url = '/finches'

def add_feeding(request, finch_id):
    form = FeedingForm(request.POST)
    if form.is_valid():
        new_feeding = form.save(commit=False)
        new_feeding.finch_id = finch_id
        new_feeding.save()
    return redirect('detail', finch_id=finch_id)

class ToyList(ListView):
    model = Toy

class ToyDetail(DetailView):
    model = Toy

class ToyCreate(CreateView):
    model = Toy
    fields = '__all__'

class ToyUpdate(UpdateView):
    model = Toy
    fields = ['name', 'color']

class ToyDelete(DeleteView):
    model = Toy
    success_url = '/toys'

def assoc_toy(request, finch_id, toy_id):
    Finch.objects.get(id=finch_id).toys.add(toy_id)
    return redirect('detail', finch_id=finch_id)

def some_function(request):
    secret_key = os.environ['SECRET_KEY']

def add_photo(request, finch_id):
    photo_file = request.FILES.get('photo-file',None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(photo_file, bucket, key)
            url = f"{os.environ['S3_BASE_URL']}/{key}"
            Photo.objects.create(url=url, finch_id=finch_id)
        except:
            print('Error')
    return redirect('detail', finch_id=finch_id)