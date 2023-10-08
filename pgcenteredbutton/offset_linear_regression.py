import numpy as np
from sklearn.linear_model import LinearRegression
from pgcenteredbutton.generate_offset_data import generate_offset_data
from pgcenteredbutton.generate_adjusted_offset_data import generate_adjusted_offset_data
import json


try:
    with open("offset_data.json", "r") as file:
        dict = json.load(file)
except:
    generate_offset_data()
    with open("offset_data.json", "r") as file:
        dict = json.load(file)

x_data = dict['font_size_list']
y_data = dict['offset_list']

# Given data
x_data = np.array(x_data)  # Continue with all x values
y_data = np.array(y_data)  # Continue with all y values

# Reshape the data for scikit-learn
x_data = x_data.reshape(-1, 1)
y_data = y_data.reshape(-1, 1)

# Create and train the linear regression model
model = LinearRegression()
model.fit(x_data, y_data)


# Calculate the absolute percentage error for each data point
ape = np.abs(y_data / x_data) * 100

# Calculate MAPE
mape = np.mean(ape)

params = {'coef': float(model.coef_[0][0]), 'intercept': float(model.intercept_[0]), 'MAPE': mape}

try:
    with open('data_analysis.json', 'r') as file:
        data = json.load(file)
except:
    data = {}

data['unadjusted_data'] = params

with open('data_analysis.json', 'w') as file:
    json.dump(data, file, indent=4)

generate_adjusted_offset_data()