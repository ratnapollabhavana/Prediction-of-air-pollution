# Air Quality Index (AQI) Prediction

This project is a Machine Learning based web application that predicts Air Quality Index (AQI) using historical air pollution data.

## Technologies Used
- Python
- Flask
- Pandas
- Scikit-learn
- Joblib

## How to Run the Project

1. Install required packages:
   pip install -r requirements.txt

2. Run the application:
   python app.py

3. Open in browser:
   http://127.0.0.1:5000/

## Note
The trained model file (airquality.joblib) is not uploaded to GitHub because it exceeds GitHub's 100MB file size limit.

To generate the model file, run:
python retrain_model.py
