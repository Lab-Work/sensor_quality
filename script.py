import numpy as np
import sensor_data

network = 'I80'
address = r'C:\Users\Carlos\Desktop\ResearchStatistics'
sensors_allNetwork = r'\sensors_allNetwork.csv'
sensors_missingData = address + r'\sensors_missingData.csv'
sensors_compareData = address + r'\sensors_compareData.csv' 
start = '5/9/15 19:50'
end = '5/9/15 20:10'

sensors = sensor_data.SensorDataStatistics(address, network, sensors_allNetwork)
sensors.percent_missing_speed(sensors_missingData, start, end)
sensors.percent_missing_count(sensors_missingData, start, end)
sensors.percent_difference_speed(sensors_compareData, start, end)  
sensors.percent_difference_count(sensors_compareData, start, end)
