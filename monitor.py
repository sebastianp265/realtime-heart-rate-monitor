import requests
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from datetime import datetime
import time
import matplotlib.dates as mdates

all_times = []
all_heart_rates = []

anomaly_times = []
anomaly_heart_rates = []

fig, ax = plt.subplots()
all_heart_rates_line, = ax.plot([], [], label="Normalne wyniki", color='blue')
anomaly_heart_rates_line, = ax.plot([], [], 'ro', label="Anomalie")

ax.set_xlabel('Data i godzina')
ax.set_ylabel('Tętno (uderzenia na minutę)')
ax.legend()
ax.grid(True)


def fetch_data():
    try:
        response = requests.get('http://127.0.0.1:5000/heart_rate')
        if response.status_code == 200:
            data = response.json()
            return data['heart_rate'], data['anomaly']
        else:
            print(f"Error fetching data: {response.status_code}")
            return None, None
    except Exception as e:
        print(f"Exception occurred: {e}")
        return None, None


def update(frame):
    print(f"Frame number {frame}")
    current_datetime = datetime.fromtimestamp(time.time())
    heart_rate, anomaly = fetch_data()
    if heart_rate is not None:
        all_times.append(current_datetime)
        all_heart_rates.append(heart_rate)

        if anomaly == "YES":
            anomaly_heart_rates.append(heart_rate)
            anomaly_times.append(current_datetime)

        if len(all_times) > 100:
            all_times.pop(0)
            all_heart_rates.pop(0)

        if len(anomaly_times) > 100:
            anomaly_times.pop(0)
            anomaly_heart_rates.pop(0)

        # Remove corresponding anomaly data if present
        while len(anomaly_times) > 0 and anomaly_times[0] < all_times[0]:
            anomaly_times.pop(0)
            anomaly_heart_rates.pop(0)

        all_heart_rates_line.set_data(all_times, all_heart_rates)
        anomaly_heart_rates_line.set_data(anomaly_times, anomaly_heart_rates)

        ax.relim()
        ax.autoscale_view()

        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
        fig.autofmt_xdate()

    else:
        print("No data fetched")

    return all_heart_rates_line, anomaly_heart_rates_line


ani = FuncAnimation(fig, update, interval=1000)

plt.show()
