"""
Create a weather graph for the last seven days in Valencia Spain using an open weather API.
"""

import requests
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np

style.use('fivethirtyeight')

api_key = 'b045804ab93431828b3e101e2be26dc1'

location = "Valencia,es"

complete_api_link = 'http://api.openweathermap.org/data/2.5/forecast?q=' + location + '&appid=' + api_key
api_link = requests.get(complete_api_link)
api_data = api_link.json()

# create lists to store temperature and date
temp_list = []
date_list = []



# store and convert data into variables
for i in range(0, 40):
    temp_list.append(api_data['list'][i]['main']['temp'] - 273.15)
    date = datetime.fromtimestamp(api_data['list'][i]['dt'])
    date_list.append(date)



# plot the data
plt.plot(temp_list, label = 'Temperature')

# beautify the x-labels
plt.gcf().autofmt_xdate()

plt.xlabel('Date')
plt.ylabel('Temperature in Kelvin')
plt.title('Weather Graph for the last seven days in Valencia Spain')
plt.legend()
plt.show()

