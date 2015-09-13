import numpy as np
import sensor_data

#network = 'I80'
network = 'I57I64'

address = r'C:\Users\Carlos\Documents\GitHub\Sensor_Statistics'

# Note: At least two sensors must be in this csv file (glitch)
sensors_allNetwork = r'\sensors_allNetwork.csv'

# Note: At least two sensors must be in this csv file (glitch)
sensors_missingData = address + r'\sensors_missingData.csv'

# Note: At least two PAIRS of sensors must be in this csv file (glitch)
sensors_compareData = address + r'\sensors_compareData.csv'


start = '11/1/14 00:00'
end = '11/30/14 23:55'

daily_start = '16:30'
daily_end = '17:30'

sensors = sensor_data.SensorDataStatistics(address, network, sensors_allNetwork)
#sensors.percent_missing_speed(sensors_missingData, start, end)
#sensors.percent_missing_count(sensors_missingData, start, end)
#sensors.percent_difference_speed(sensors_compareData, start, end)  
#sensors.percent_difference_count(sensors_compareData, start, end)
#sensors.percent_missing_speed_daily(sensors_missingData, start, end, daily_start, daily_end)
sensors.percent_missing_count_daily(sensors_missingData, start, end, daily_start, daily_end)
