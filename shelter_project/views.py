from django.shortcuts import render

def home(request):
    return render(request, 'shelter_project/home.html')
