import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.impute import SimpleImputer
import joblib

# Load the data
df = pd.read_csv("city_day.csv")

# Select relevant features
features = ['PM2.5', 'PM10', 'O3', 'NO2', 'CO', 'SO2']
target = 'AQI'

# Drop rows where target is NaN

df = df.dropna(subset=[target])

# Handle missing values
imputer = SimpleImputer(strategy='mean')
df[features] = imputer.fit_transform(df[features])

# Split the data
X = df[features]
y = df[target]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Squared Error: {mse}")
print(f"R2 Score: {r2}")

# Save the model using joblib
joblib.dump(model, 'airquality.joblib')
print("Model saved successfully!")