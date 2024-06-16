import requests

class AirQualityServiceClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.api_base_url = "http://api.airvisual.com/v2"

    def get_air_quality_data(self, city: str, state: str, country: str) -> dict:
        url = f"{self.api_base_url}/city?city={city}&state={state}&country={country}&key={self.api_key}"
        response = requests.get(url)
        if response.ok:
            return response.json()
        else:
            response.raise_for_status()

    def validation_and_transformation_of_data(self,data):
        if "info " not in data:
            raise ValueError    #sprawdzanie czy mamy wyst danych
        
        #pobieranie danych o pogodzie i zaniecz pow
        weather_status = ""
        pollution_status = ""
        temp = ""
        pressure =""
            #validacja wartosci
        if not (-50 <= temp <= 50):
           raise ValueError("Temperature value out of range")
        if not (800 <= pressure <= 1200):
           raise ValueError("Pressure value out of range")

        transformed_data = {
        'city': "Warsaw",
        'state': "Mazovia",
        'country': "Poland",
        'temp': temp,
        'pressure': pressure,
        'aq_index': pollution_status['aqius'],
        'timestamp': weather_status['ts']}
        return transformed_data
    