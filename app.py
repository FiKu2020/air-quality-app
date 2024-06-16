from flask import Flask, request, jsonify
from flask.views import MethodView
from datetime import datetime, timezone
from models import DataStore, WeatherAirQualityInfo

app = Flask(__name__)

def convert_to_utc(dt):
    if dt.tzinfo:
        dt = dt.astimezone(timezone.utc).replace(tzinfo=None)
    return dt

class AirQualityView(MethodView):
    def get(self):
        timestamp_param = request.args.get('timestamp')
        if timestamp_param:
            try:
                request_timestamp = convert_to_utc(datetime.fromisoformat(timestamp_param))
                closest_entry = storage.get_closest_entry(request_timestamp)
                if closest_entry:
                    return jsonify(closest_entry.dict())
                else:
                    return jsonify({"message": "Data not found"}), 404
            except ValueError:
                return jsonify({"error": "Invalid timestamp format"}), 400
        else:
            all_entries = [entry.dict() for entry in storage.entries]
            return jsonify(all_entries)

    def post(self):
        try:
            data = request.json
            if data['timestamp'].endswith('Z'):
                data['timestamp'] = data['timestamp'][:-1]
            data['timestamp'] = convert_to_utc(datetime.fromisoformat(data['timestamp']).replace(tzinfo=timezone.utc))
            entry = WeatherAirQualityInfo(**data)
            storage.add_entry(entry)
            return jsonify(entry.dict()), 201
        except pydantic.ValidationError as e:
            return jsonify({"error": str(e)}), 400
        except ValueError:
            return jsonify({"error": "Invalid datetime format"}), 400

storage = DataStore()

app.add_url_rule('/api/entries', view_func=AirQualityView.as_view('entries_api'))

if __name__ == '__main__':
    app.run(debug=True)