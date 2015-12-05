import numpy as np
from datetime import datetime as dt
from collections import OrderedDict

class sensor_statistics:

    def __init__(self, all_sensors, folder):
        self.sensors = OrderedDict()
        for sensorID in all_sensors:
            file = folder + '\\' + str(sensorID) + '.csv'
            self.sensors[sensorID] = np.atleast_2d(np.genfromtxt(file, dtype='str', delimiter=',', skip_header=1))

    def percent_missing_speed(self, missing_data_sensors, initial, final):
        print('\n')
        print('Percent Missing: Speed')
        print('Interval: %s - %s' %(initial, final))
        start, end = initial.time(), final.time()
        self.__percent_missing(missing_data_sensors, initial, final, start, end, 'speed')

    def percent_missing_count(self, missing_data_sensors, initial, final):
        print('\n')
        print('Percent Missing: Count')
        print('Interval: %s - %s' %(initial, final))
        start, end = initial.time(), final.time()
        self.__percent_missing(missing_data_sensors, initial, final, start, end, 'count')

    def percent_missing_speed_subinterval(self, missing_data_sensors, initial, final, start, end):
        print('\n')
        print('Percent Missing: Speed')
        print('Interval: %s - %s' %(initial, final))
        print('Subinterval: %s - %s' %(start, end))
        self.__percent_missing(missing_data_sensors, initial, final, start, end, 'speed')

    def percent_missing_count_subinterval(self, missing_data_sensors, initial, final, start, end):
        print('\n')
        print('Percent Missing: Count')
        print('Interval: %s - %s' %(initial, final))
        print('Subinterval: %s - %s' %(start, end))
        self.__percent_missing(missing_data_sensors, initial, final, start, end, 'count')

    def percent_difference_speed(self, different_data_sensors, initial, final):
        print('\n')
        print('Percent Difference: Speed')
        print('Interval: %s - %s' %(initial, final))
        start, end = initial.time(), final.time()
        self.__percent_difference(different_data_sensors, initial, final, start, end, 'speed')

    def percent_difference_count(self, different_data_sensors, initial, final):
        print('\n')
        print('Percent Difference: Count')
        print('Interval: %s - %s' %(initial, final))
        start, end = initial.time(), final.time()
        self.__percent_difference(different_data_sensors, initial, final, start, end, 'count')

    def percent_difference_speed_subinterval(self, different_data_sensors, initial, final, start, end):
        print('\n')
        print('Percent Difference: Speed')
        print('Interval: %s - %s' %(initial, final))
        print('Subinterval: %s - %s' %(start, end))
        start, end = initial.time(), final.time()
        self.__percent_difference(different_data_sensors, initial, final, start, end, 'speed')

    def percent_difference_count_subinterval(self, different_data_sensors, initial, final, start, end):
        print('\n')
        print('Percent Difference: Count')
        print('Interval: %s - %s' %(initial, final))
        print('Subinterval: %s - %s' %(start, end))
        start, end = initial.time(), final.time()
        self.__percent_difference(different_data_sensors, initial, final, start, end, 'count')

    def __percent_missing(self, missing_data_sensors, initial, final, start, end, mode):

        # Idenitify the column for the given mode.
        # Check only data within intervals of interest.
        # If datum is missing, add it to the missing count.
        # Compute the percentage of missing data.
        
        column = 1 if mode == 'speed' else 2 if mode == 'count' else 0
        for sensorID in missing_data_sensors:
            try:
                total, missing = 0, 0
                for datum in self.sensors[sensorID]:
                    timestamp = dt.strptime(datum[0], "%m/%d/%Y %H:%M")
                    if initial <= timestamp <= final and start <= timestamp.time() <= end:
                        total += 1
                        if not(datum[column]):
                            missing += 1
                percent = 100*missing/total
                print('Sensor %s is missing %.2f%% of the %s data.' %(sensorID, percent, mode))
            except ZeroDivisionError:
                print('Sensor %s has no readings for the given interval.' %(sensorID))
            except IndexError:
                print('Sensor %s is missing 100%% of the %s data.' %(sensorID, mode))

    def __percent_difference(self, different_data_sensors, initial, final, start, end, mode):

        column = 1 if mode == 'speed' else 2 if mode == 'count' else 0         
        for sensorIDs in different_data_sensors:
            try:
                initial_sensor, final_sensor = sensorIDs[0], sensorIDs[1]
                initial_sensor_data, final_sensor_data = np.atleast_1d(np.empty((1,1))), np.atleast_1d(np.empty((1,1)))
                for datum in self.sensors[initial_sensor]:
                    timestamp = dt.strptime(datum[0], "%m/%d/%Y %H:%M")
                    if initial <= timestamp <= final and start <= timestamp.time() <= end:
                        initial_sensor_data = np.append(initial_sensor_data, datum[column])
                for datum in self.sensors[final_sensor]:
                    timestamp = dt.strptime(datum[0], "%m/%d/%Y %H:%M")
                    if initial <= timestamp <= final and start <= timestamp.time() <= end:
                        final_sensor_data = np.append(final_sensor_data, datum[column])
                difference, count = 0, 0
                for initial_datum, final_datum in zip(initial_sensor_data, final_sensor_data):
                    if initial_datum != '' and final_datum != '':
                        initial_datum, final_datum = float(initial_datum), float(final_datum)
                        if initial_datum != 0:
                            count += 1
                            difference += abs(initial_datum - final_datum)/initial_datum
                percent = 100*difference/count
                print("The %s data of %s is %.2f%% different compared to the %s data of %s." %(mode, final_sensor, percent, mode, initial_sensor))

            except IndexError:

                
