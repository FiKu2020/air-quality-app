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