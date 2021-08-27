from flask import Flask, request, abort
import ie_bike_model
import sklearn
from platform import python_version
import argparse
import time
from datetime import datetime
import sklearn

app = Flask(__name__)


@app.route("/")
def home():
    packages = {
        "python version": python_version(),
        "sklearn version": sklearn.__version__,
        "ie_bike_model version": ie_bike_model.__version__,
    }
    return packages


@app.route("/train_and_persist", methods=["GET"])
def train_and_persist():
    from ie_bike_model.model import train_and_persist

    train_and_persist()

    # Include the score of the model in the API
    scored = train_and_persist()
    message = {"status": "ok", "Score of trained model - RMSE": scored}
    return message


@app.route("/predict", methods=["GET"])
def predict():

    try:

        from ie_bike_model.model import predict

        weatherdict = {
            "clear": "Clear, Few clouds, Partly cloudy, Partly cloudy",
            "cloudy": "Mist + Cloudy, Mist + Broken clouds, Mist + Few clouds, Mist",
            "light_rain": "Light Snow, Light Rain + Thunderstorm + Scattered clouds, Light Rain + Scattered clouds",
            "heavy_rain": "Heavy Rain + Ice Pallets + Thunderstorm + Mist, Snow + Fog",
        }

        date = str(request.args.get("date"))
        hour = int(request.args.get("hour", ""))
        weather_sit = str(request.args.get("weather_situation", ""))
        temperature = float(request.args.get("temperature", ""))
        feeling_temperature = float(request.args.get("feeling_temperature", ""))
        humidity = float(request.args.get("humidity", ""))
        windspeed_ = float(request.args.get("windspeed", ""))

        if weather_sit in weatherdict:
            weathersit2 = str(weatherdict.get(weather_sit))

        executiontime = time.time()
        prediction = predict(
            dteday=date,
            hr=hour,
            weathersit=weathersit2,
            temp=temperature,
            atemp=feeling_temperature,
            hum=humidity,
            windspeed=windspeed_,
        )
        result = {
            "result": round(prediction),
            "elapsed_time": round((time.time() - executiontime), 3),
        }

        return result

    except:
        valid_arg = [
            "date",
            "hour",
            "weather_situation",
            "temperature",
            "feeling_temperature",
            "humidity",
            "windspeed",
        ]
        for el in valid_arg:
            if str(el) not in request.args:
                message = {"Not a correct parameters: ": el}
                return message
            else:
                abort(400)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="IE Bikes Model.")
    parser.add_argument("port", type=int, help="Port to create the HTTPS")
    args = parser.parse_args()
    app.run(host="0.0.0.0", port=args.port, debug=True)
