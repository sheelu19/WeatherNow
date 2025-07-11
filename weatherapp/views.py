import datetime
import re
import requests
from django.shortcuts import render
from django.contrib import messages
from django.views.decorators.cache import cache_page
from django.templatetags.static import static  # ✅ Import static helper

# Background image mapping
WEATHER_BACKGROUND_MAP = {
    '01d': 'images/clear_day.jpg',
    '01n': 'images/clear_night.jpg',
    '02d': 'images/few_day.jpg',
    '02n': 'images/few_night.jpg',
    '03d': 'images/scattered_day.jpg',
    '03n': 'images/scattered_night.jpg',
    '09d': 'images/shower_day.jpg',
    '09n': 'images/shower_night.webp',
    '10d': 'images/rain_day.webp',
    '10n': 'images/rain_night.jpg',
    '11d': 'images/thunder_day.jpg',
    '11n': 'images/thunder_night.jpg',
    '13d': 'images/snow_day.jpg',
    '13n': 'images/snow_night.jpg',
    '50d': 'images/fog_day.jpg',
    '50n': 'images/fog_night.webp',
    'default': 'images/default.jpg'
}

API_KEY = '0ac832535159d770507c7ca929207a16'
BASE_WEATHER_URL = 'https://api.openweathermap.org/data/2.5/weather'
PARAMS = {'units': 'metric', 'appid': API_KEY}


def get_background_image(description, icon):
    description = description.lower()
    if icon in ['04d', '04n']:
        if 'overcast' in description:
            return 'images/overcast_days.jpg' if icon == '04d' else 'images/overcast_nightt.jpg'
        elif 'broken' in description:
            return 'images/broken_day.jpg' if icon == '04d' else 'images/broken_night.jpg'
    return WEATHER_BACKGROUND_MAP.get(icon, WEATHER_BACKGROUND_MAP['default'])


def fetch_weather(city):
    url = f'{BASE_WEATHER_URL}?q={city}'
    response = requests.get(url, params=PARAMS)
    response.raise_for_status()
    return response.json()


@cache_page(60 * 5)
def home(request):
    if request.method == 'POST' and 'city' in request.POST:
        raw_input = request.POST['city']
        city = re.sub(r'\b(District|City|Town)\b', '', raw_input.split(',')[0], flags=re.IGNORECASE).strip()

        recent_cities = request.session.get('recent_cities', [])
        if city and city.lower() not in [c.lower() for c in recent_cities]:
            recent_cities.insert(0, city)
        request.session['recent_cities'] = recent_cities[:5]

    elif 'recent' in request.GET:
        city = request.GET['recent']
    elif 'clear' in request.GET:
        request.session['recent_cities'] = []
        city = 'yamunanagar'
    else:
        city = 'yamunanagar'

    try:
        weather_data = fetch_weather(city)
        description = weather_data['weather'][0]['description']
        icon = weather_data['weather'][0]['icon']
        temp = weather_data['main']['temp']
        bg_image_url = static(get_background_image(description, icon))

        return render(request, 'weatherapp/index.html', {
            'description': description,
            'icon': icon,
            'temp': temp,
            'day': datetime.date.today(),
            'city': city,
            'bg_image_url': bg_image_url,
            'exception_occurred': False,
            'recent_cities': request.session.get('recent_cities', [])
        })

    except (requests.RequestException, KeyError, IndexError):
        try:
            messages.warning(request, 'Invalid city. Showing Yamunanagar data.')
            fallback_city = 'yamunanagar'
            fallback_data = fetch_weather(fallback_city)
            description = fallback_data['weather'][0]['description']
            icon = fallback_data['weather'][0]['icon']
            temp = fallback_data['main']['temp']
            bg_image_url = static(get_background_image(description, icon))

            return render(request, 'weatherapp/index.html', {
                'description': description,
                'icon': icon,
                'temp': temp,
                'day': datetime.date.today(),
                'city': fallback_city,
                'bg_image_url': bg_image_url,
                'exception_occurred': True,
                'recent_cities': request.session.get('recent_cities', [])
            })

        except Exception:
            messages.error(request, 'Weather service is currently unavailable.')
            return render(request, 'weatherapp/index.html', {
                'description': 'clear sky',
                'icon': '01d',
                'temp': 25,
                'day': datetime.date.today(),
                'city': 'yamunanagar',
                'bg_image_url': static(WEATHER_BACKGROUND_MAP['default']),
                'exception_occurred': True,
                'recent_cities': []
            })
