from flask import Flask, request, jsonify, render_template
import joblib
import requests

app = Flask(__name__)

# Load your trained model
model = joblib.load('airquality.joblib')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/heatmap')
def heatmap():
    return render_template('heatmap.html')

@app.route('/predict_manually', methods=['POST','GET'])
def predict_manually():
    if request.method == 'POST':
        # Extract data from form
        pm25 = float(request.form['PM2.5'])
        pm10 = float(request.form['PM10'])
        o3 = float(request.form['O3'])
        no2 = float(request.form['NO2'])
        co = float(request.form['CO'])
        so2 = float(request.form['SO2'])

        # Prepare data for prediction
        sample = [[pm25, pm10, o3, no2, co, so2]]
        prediction = model.predict(sample)[0]

        # Determine Air Quality Index based on prediction
        result, conclusion = determine_air_quality(prediction)

        # Return the result to the user
        return render_template('results.html', prediction=prediction, result=result, conclusion=conclusion)
    else:
        return render_template('index.html')

def determine_air_quality(prediction):
    if prediction < 50:
        return 'Air Quality Index is Good', 'The Air Quality Index is excellent. It poses little or no risk to human health.'
    elif 51 <= prediction < 100:
        return 'Air Quality Index is Satisfactory', 'The Air Quality Index is satisfactory, but there may be a risk for sensitive individuals.'
    elif 101 <= prediction < 200:
        return 'Air Quality Index is Moderately Polluted', 'Moderate health risk for sensitive individuals.'
    elif 201 <= prediction < 300:
        return 'Air Quality Index is Poor', 'Health warnings of emergency conditions.'
    elif 301 <= prediction < 400:
        return 'Air Quality Index is Very Poor', 'Health alert: everyone may experience more serious health effects.'
    else:
        return 'Air Quality Index is Severe', 'Health warnings of emergency conditions. The entire population is more likely to be affected.'

# Function to fetch pollutant data from WAQI API
# import requests

def get_pollutants(city, token="2c04ce9d22c0e023c45841b0a61c24fd3a22d1b6"):
    url = f"https://api.waqi.info/feed/{city}/?token={token}"
    response = requests.get(url)
    data = response.json()
    if data['status'] == 'ok':
        iaqi = data['data']['iaqi']
        pm25 = iaqi.get('pm25', {}).get('v')
        pm10 = iaqi.get('pm10', {}).get('v')
        o3 = iaqi.get('o3', {}).get('v')
        no2 = iaqi.get('no2', {}).get('v')
        co = iaqi.get('co', {}).get('v')
        so2 = iaqi.get('so2', {}).get('v')
        return {
            'PM2.5': pm25,
            'PM10': pm10,
            'O3': o3,
            'NO2': no2,
            'CO': co,
            'SO2': so2
        }
    else:
        return None

@app.route('/city_pollutants', methods=['GET', 'POST'])
def city_pollutants():
    if request.method == 'POST':
        city = request.form['city']
        pollutants = get_pollutants(city)
        return render_template('city_pollutants.html', city=city, pollutants=pollutants)
    else:
        return render_template('city_pollutants.html', city=None, pollutants=None)

if __name__ == '__main__':
    app.run(debug=True)
