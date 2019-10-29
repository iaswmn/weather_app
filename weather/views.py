from django.shortcuts import render
import requests
from django.contrib import messages
from .models import City
from .forms import CityForm


def index(request):
    key = '581d37f30e70964ed4e6aafcde5f5d39'
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + key

    if request.method == 'POST':
        cities = City.objects.all()
        city_names = []
        for city in cities:
            city_names.append(city.name)
        if request.POST['name'] not in city_names:
            form = CityForm(request.POST)
            form.save()
        else:
            messages.error(request, 'city exist!')

    form = CityForm()

    all_cities = []
    cities = City.objects.all()
    for city in cities:
        res = requests.get(url.format(city.name)).json()
        if res['cod'] == '404':
            city_info = {
                'city': city.name,
                'temp': 'error',
                'icon': 'error'
            }
            all_cities.append(city_info)
        else:
            city_info = {
                'city': city.name,
                'temp': res['main']['temp'],
                'icon': res['weather'][0]['icon']
            }
            all_cities.append(city_info)
    context = {'all_info': all_cities, 'form': form}
    return render(request, 'weather/index.html', context)
