from django.shortcuts import render
from animal.models import Animal

def home(request):
    animals = Animal.objects.all()
    
    return render(request, 'shelter_project/home.html', {"animals": animals},)
