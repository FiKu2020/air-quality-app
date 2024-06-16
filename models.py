from datetime import datetime
from typing import Optional, List
import pydantic

class WeatherAirQualityInfo(pydantic.BaseModel):
    timestamp: datetime
    temp: Optional[int] = pydantic.Field(None, ge=-50, le=50)
    press: Optional[int] = pydantic.Field(None, ge=800, le=1200)
    aq_index: Optional[int] = pydantic.Field(None, ge=0)
    city: str
    state: str
    country: str

class DataStore:
    def __init__(self):
        self.entries: List[WeatherAirQualityInfo] = []

    def add_entry(self, entry: WeatherAirQualityInfo):
        self.entries.append(entry)

    def get_closest_entry(self, timestamp: datetime) -> Optional[WeatherAirQualityInfo]:
        normalized_timestamp = self.convert_to_utc(timestamp)
        try:
            return min(
                self.entries,
                key=lambda x: abs(self.convert_to_utc(x.timestamp) - normalized_timestamp),
                default=None
            )
        except ValueError:
            return None

    @staticmethod
    def convert_to_utc(dt: datetime) -> datetime:
        if dt.tzinfo:
            dt = dt.astimezone(timezone.utc).replace(tzinfo=None)
        return dt