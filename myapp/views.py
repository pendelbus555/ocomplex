from django.shortcuts import render, HttpResponseRedirect
from .forms import CityForm


def index(request):
    if request.method == "POST":
        form = CityForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect("/thanks/")

    else:
        form = CityForm()

    return render(request, "myapp/index.html", {"form": form})
