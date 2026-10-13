# Create your views here.
from django.shortcuts import render
from .models import Animal

def animal_list(request):
    # Fetch only animals that are available
    available_animals = Animal.objects.filter(available=True)
    
    # Send the data to the HTML template
    return render(request, 'shelter_project/animal_listing.html', {'animals': available_animals})
