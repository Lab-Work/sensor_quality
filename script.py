import numpy as np
import sensor_data_2
import os
from datetime import datetime as dt
import time

# Datetime boundaries for the period of interest.
# Format: "%m/%d/%Y %H:%M"
initial = '11/1/2014 00:00'
final = '11/30/2014 23:55'

# Time boundaries for subperiod of interest within larger period.
# Format: "%H:%M"
start = '16:30'
end = '17:30'

# Network: 'I80' or 'I57I64'
network = 'I57I64'



# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Find the path to the current directory and folder
directory = os.path.dirname(os.path.realpath(__file__))
folder = directory + '\\' + network

# Load the configuration data files
all_sensors = np.atleast_1d(np.genfromtxt(directory + r'\all_sensors.csv', dtype='str', delimiter=',', skip_header=1))
missing_data_sensors = np.atleast_1d(np.genfromtxt(directory + r'\missing_data_sensors.csv', dtype='str', delimiter=',', skip_header=1))
different_data_sensors = np.atleast_2d(np.genfromtxt(directory + r'\different_data_sensors.csv', dtype='str', delimiter=',', skip_header=1))

initial = dt.strptime(initial, "%m/%d/%Y %H:%M")
final = dt.strptime(final, "%m/%d/%Y %H:%M")
start = (dt.strptime(start, "%H:%M")).time()
end = (dt.strptime(end, "%H:%M")).time()

sensor_data = sensor_data_2.sensor_statistics(all_sensors, folder)
sensor_data.percent_missing_speed(missing_data_sensors, initial, final)
sensor_data.percent_missing_count(missing_data_sensors, initial, final)
sensor_data.percent_missing_speed_subinterval(missing_data_sensors, initial, final, start, end)
sensor_data.percent_missing_count_subinterval(missing_data_sensors, initial, final, start, end)
#sensor_data.percent_difference_speed(different_data_sensors, initial, final)
#sensor_data.percent_difference_count(different_data_sensors, initial, final)
#sensor_data.percent_difference_speed(different_data_sensors, initial, final)
