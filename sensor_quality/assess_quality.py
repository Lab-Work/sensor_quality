# Author: Juan Carlos Martinez

import numpy as np
import sensor_quality
import os
from datetime import datetime as dt
import time

# INPUT PARAMETERS
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


# DO NOT MODIFY
# Find the path to the current directory and folder

#os.path.dirname(os.path.realpath(__file__))
directory = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))
folder = directory + '\data\\' + network
# Load the configuration data files
all_sensors = np.atleast_1d(np.genfromtxt(directory + r'\configuration_files\all_sensors.csv', dtype='str', delimiter=',', skip_header=1))
missing_data_sensors = np.atleast_1d(np.genfromtxt(directory + r'\configuration_files\missing_data_sensors.csv', dtype='str', delimiter=',', skip_header=1))
different_data_sensors = np.atleast_2d(np.genfromtxt(directory + r'\configuration_files\different_data_sensors.csv', dtype='str', delimiter=',', skip_header=1))
# Convert parameters to datetime format
initial = dt.strptime(initial, "%m/%d/%Y %H:%M")
final = dt.strptime(final, "%m/%d/%Y %H:%M")
start = (dt.strptime(start, "%H:%M")).time()
end = (dt.strptime(end, "%H:%M")).time()


# UNCOMMENT FUNCTIONS NEEDED
sensor_quality = sensor_quality.sensor_statistics(all_sensors, folder)
sensor_quality.percent_missing_speed(missing_data_sensors, initial, final)
sensor_quality.percent_missing_count(missing_data_sensors, initial, final)
sensor_quality.percent_missing_speed_subinterval(missing_data_sensors, initial, final, start, end)
sensor_quality.percent_missing_count_subinterval(missing_data_sensors, initial, final, start, end)
#sensor_quality.percent_difference_speed(different_data_sensors, initial, final)
#sensor_quality.percent_difference_count(different_data_sensors, initial, final)
#sensor_quality.percent_difference_speed_subinterval(different_data_sensors, initial, final, start, end)
sensor_quality.percent_difference_count_subinterval(different_data_sensors, initial, final, start, end)
