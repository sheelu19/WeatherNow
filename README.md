#  Django Weather App

This is a simple Django-based web application that shows the current weather for a given city using data from the OpenWeatherMap API.

## Project Structure

weatherproject/

│

├── manage.py

├── weatherproject/ # Django settings

│ ├── init.py

│ ├── settings.py

│ ├── urls.py

│ └── wsgi.py

│

├── weatherapp/ # Weather app

│ ├── migrations/

│ ├── static/

│ ├── templates/

│ ├── init.py

│ ├── admin.py

│ ├── apps.py

│ ├── models.py

│ ├── tests.

│ ├── views.py

│ └── urls.py

│

└── static/ # Static files (optional)

##  Features

-  Search weather by city name.
-  Real-time weather data via OpenWeatherMap API.
-  Displays temperature, humidity, wind speed, and conditions.
-  Styled using Bootstrap and custom CSS.

---

## ⚙ Setup Instructions

**1. Clone the Repository**
      git clone https://github.com/your-username/weatherproject.git
      cd weatherproject
      
**2. Create and Activate a Virtual Environment**
      python -m venv venv
      source venv/bin/activate   # On Windows: venv\Scripts\activate
      
**3. Install Dependencies**
      pip install -r requirements.txt
      If requirements.txt is missing, install manually:
      pip install django requests
      
**4. Get an API Key**
      Sign up at OpenWeatherMap and get your API key. 
      In your weatherapp/views.py, replace:
      api_key = "YOUR_API_KEY_HERE"
      with your actual API key.
      
**5. Run Database Migrations**
      python manage.py migrate
      
**6. Run the Development Server**
      python manage.py runserver
      Visit the app at http://127.0.0.1:8000/

**Example Usage**
  Enter the name of any city.
  
  Click Get Weather.
  
  See weather info including:
  
  Temperature (°C)
  
  Weather description
  
  Humidity (%)
  
  Wind speed (m/s)

