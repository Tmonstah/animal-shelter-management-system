from django.shortcuts import render
from .models import Animal

# animal_listing: The function that is used to show
#   the animals on the webpage in our animal shelter.
# TODO: eventually add ability to not show animals no 
#       longer at the shelter.
def animal_listing(request):
    #grab all animals within the database
    animals = Animal.objects.all()
    return render(request, "animals/animals_list.html",
    {"animals": animals})