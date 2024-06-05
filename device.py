from flask import Flask, jsonify
import numpy as np
import random
import time

app = Flask(__name__)


# Generate heart rate data for simulation
def generate_base_heart_rate_data():
    timestamps = np.arange(0, 24 * 60 * 60, 1)  # Simulate data for one day at 1-second intervals
    base_heart_rates = 70 + 5 * np.sin(2 * np.pi * timestamps / (24 * 60 * 60))  # Sine wave for base heart rate
    return base_heart_rates


base_heart_rates = generate_base_heart_rate_data()

# Calculate mean and standard deviation for anomaly detection
mean_hr = np.mean(base_heart_rates)
std_hr = np.std(base_heart_rates)


def generate_heart_rate():
    current_time = time.time()
    day_seconds = 24 * 60 * 60
    second_of_day = int(current_time % day_seconds)

    # Base heart rate from sine wave
    base_heart_rate = base_heart_rates[second_of_day]

    # Add random noise
    noise = np.random.normal(0, 1)
    heart_rate = base_heart_rate + noise

    # Simulate periods of exercise or rest
    if random.random() < 0.05:
        # Exercise
        heart_rate += random.randint(20, 40)
    elif random.random() < 0.05:
        # Rest
        heart_rate -= random.randint(10, 20)

    return heart_rate


def is_anomaly(heart_rate):
    # Calculate Z-score
    z_score = (heart_rate - mean_hr) / std_hr
    # Detect anomalies with Z-score > 2 or < -2 and clinically abnormal heart rates
    return abs(z_score) > 2 or heart_rate < 50 or heart_rate > 110


@app.route('/heart_rate', methods=['GET'])
def get_heart_rate():
    heart_rate = generate_heart_rate()
    anomaly = "YES" if is_anomaly(heart_rate) else "NO"
    return jsonify({'heart_rate': int(heart_rate), 'anomaly': anomaly})


if __name__ == '__main__':
    app.run(debug=True)
