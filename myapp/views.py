from django.shortcuts import render
from .forms import CityForm
from .services import get_weather, get_city_coordinates


def index(request):
    if request.method == "POST":
        form = CityForm(request.POST)
        if form.is_valid():
            city_name = form.cleaned_data['city_name']
            lat, lng = get_city_coordinates(city_name)
            if lat and lng:
                weather_data = get_weather(lat, lng)
                print(weather_data)
                return render(request, "myapp/index.html", {"form": form, "weather_data": weather_data})
            else:
                form.add_error('city_name', 'Invalid city name. Please enter a valid city or try again later.')
    else:
        form = CityForm()

    return render(request, "myapp/index.html", {"form": form})
