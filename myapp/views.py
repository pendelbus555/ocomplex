from django.shortcuts import render
from .forms import CityForm
from .services import get_weather, get_city_coordinates


def index(request):
    last_city = request.COOKIES.get('last_city', None)
    print(last_city)
    weather_data = None

    if request.method == "POST":
        form = CityForm(request.POST)
        if form.is_valid():
            city_name = form.cleaned_data['city_name']
            lat, lng = get_city_coordinates(city_name)
            if lat and lng:
                weather_data = get_weather(lat, lng)
                response = render(request, "myapp/index.html", {"form": form, "weather_data": weather_data})
                response.set_cookie('last_city', city_name, max_age=30*24*60*60)  # 30 дней
                return response
            else:
                form.add_error('city_name', 'Invalid city name. Please enter a valid city or try again later.')
    else:
        form = CityForm()

    return render(request, "myapp/index.html", {"form": form, 'last_city': last_city})
