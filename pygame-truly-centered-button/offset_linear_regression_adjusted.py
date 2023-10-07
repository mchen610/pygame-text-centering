import numpy as np
from sklearn.linear_model import LinearRegression
import json

try:
    with open("offset_data_adjusted.json", "r") as file:
        dict = json.load(file)
        x_data = dict['font_size_list']
        y_data = dict['offset_list']

    x_data = np.array(x_data)
    y_data = np.array(y_data)

    x_data = x_data.reshape(-1, 1)
    y_data = y_data.reshape(-1, 1)

    model = LinearRegression()
    model.fit(x_data, y_data)


    ape = np.abs(y_data/x_data) * 100

    mape = np.mean(ape)

    params = {'coef': float(model.coef_[0][0]), 'intercept': float(model.intercept_[0]), 'MAPE': mape}
    print(params)
    try:
        with open('data_analysis.json', 'r') as file:
            data = json.load(file)
    except:
        data = {}

    data['adjusted_data'] = params

    with open('data_analysis.json', 'w') as file:
        json.dump(data, file, indent=4)
except:
    print("Data does not exist!")