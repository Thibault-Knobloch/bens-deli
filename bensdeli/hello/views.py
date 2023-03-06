from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Person
from .forms import PersonForm


def hello_world(request):
    return HttpResponse("Hello world, this is Ben's Deli !")


def person_list(request):
    people = Person.objects.all()
    return render(request, 'hello/person_list.html', {'people': people})


def person_create(request):
    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('person_list')
    else:
        form = PersonForm()
    return render(request, 'hello/person_create.html', {'form': form})