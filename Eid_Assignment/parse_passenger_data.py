from google.transit import gtfs_realtime_pb2
import requests

def fetch_gtfs_features():
    feed = gtfs_realtime_pb2.FeedMessage()
    response = requests.get('https://gtfs.example.com/vehicle_positions.pb')
    feed.ParseFromString(response.content)

    # Simulate aggregated features (you’ll refine this later)
    passenger_count = 420  # mock from position/trip data
    active_vehicles = len(feed.entity)

    return {
        "route": "R1",
        "time": datetime.datetime.now().strftime("%H:%M"),
        "passenger_count": passenger_count,
        "vehicle_count": active_vehicles,
        "weather": "clear",  # You can integrate a weather API
        "day_type": "weekday" if datetime.datetime.today().weekday() < 5 else "weekend"
    }
