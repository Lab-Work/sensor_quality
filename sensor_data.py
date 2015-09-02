import numpy as np
from datetime import datetime

class SensorData:

    def __init__(self, address, network, sensors_allNetwork):
        
        #Load the csv files as to a dictionary
        #The key is the name of the sensor
        #The value is the contensts of the csv file
        
        self.sensors_array = np.genfromtxt(address + sensors_allNetwork, dtype='str', delimiter=',')
        self.sensor_dict = dict()
        for each_sensor in self.sensors_array:
            sensor_file = address + '\\' + network + '\\' + each_sensor + '.csv'
            self.sensor_dict[each_sensor] = np.genfromtxt(sensor_file, dtype='str', delimiter=',')

# Derived class of SensorData
class SensorDataStatistics(SensorData):

    def __init__(self, address, network, sensors_allNetwork):
        
        # Call the constructor for the parent class
        SensorData.__init__(self, address, network, sensors_allNetwork)

    def percent_missing_speed(self, sensors_missingData, start, end):

        # Set the column number and mode, corresponding to the way the speed
        # data is organized in the csv file
        column = 1
        mode = 'speed'

        # Call the helper function
        self.percent_missing(column, mode, sensors_missingData, start, end)
        
    def percent_missing_count(self, sensors_missingData, start, end):

        # Set the column number and mode, corresponding to the way the count
        # data is organized in the csv file
        column = 2
        mode = 'count'

        # Call the helper function
        self.percent_missing(column, mode, sensors_missingData, start, end)

    def percent_missing(self, column, mode, sensors_missingData, start, end):

        # Set the start and end times in datetime format
        start = datetime.strptime(start, "%m/%d/%y %H:%M")
        end = datetime.strptime(end, "%m/%d/%y %H:%M")

        # Load the sensors that will be analyzed
        # NOTE: The csv file must include at least 2 sensors (bug caused by numpy array)
        #       Else, for loop will not work
        sensors_missingData_array = np.genfromtxt(sensors_missingData, dtype='str', delimiter=',')

        # Iterate for each sensor in the csv file
        for each_sensor in sensors_missingData_array:

            # Initialize the numbers that will be used to find the percent missing
            missing = 0
            total = 0

            # Find the number of rows of the array to avoid going out of bounds
            rows = np.shape(self.sensor_dict[each_sensor])[0] - 1

            # Iterate for each row in each sensor's array
            for row in range(1, rows):

                # Set the time at the current row in datetime format
                time = datetime.strptime(self.sensor_dict[each_sensor][row, 0], "%m/%d/%y %H:%M")

                # If the time falls between the start and end time
                if time >= start and time <= end:

                    # Count for total
                    total += 1

                    # If the row is missing the variable of the correspondent mode
                    if not self.sensor_dict[each_sensor][row, column]:
                        # Count as missing
                        missing += 1

            # Compute the percent of data missing for the correspondent mode
            percent = missing/total*100

            # Print results on command prompt
            print("Interval: %s - %s" %(start, end))
            print ("%s is missing %.2f%% of the %s data." %(each_sensor, percent, mode))
            print("\n")  

    def percent_difference_speed(self, sensors_compareData, start, end):

        # Set the column number and mode, corresponding to the way the speed
        # data is organized in the csv file
        column = 1
        mode = 'speed'

        # Call the helper function
        self.percent_difference(column, mode, sensors_compareData, start, end)

    def percent_difference_count(self, sensors_compareData, start, end):

        # Set the column number and mode, corresponding to the way the count
        # data is organized in the csv file
        column = 2
        mode = 'count'

        # Call the helper function
        self.percent_difference(column, mode, sensors_compareData, start, end)

    def percent_difference(self, column, mode, sensors_compareData, start, end):

        # Set the start and end times in datetime format
        start = datetime.strptime(start, "%m/%d/%y %H:%M")
        end = datetime.strptime(end, "%m/%d/%y %H:%M")

        # Load the PAIR of sensors that will be analyzed
        # NOTE: The csv file must include a PAIR of sensors, where the first one is the 'initial' data
        #       and the second one is the 'final' data (for percent difference computation)
        sensors_compareData_array = np.genfromtxt(sensors_compareData, dtype='str', delimiter=',')

        # Set identifiers for each sensor
        first_sensor = sensors_compareData_array[0]
        second_sensor = sensors_compareData_array[1]

        # Initialize the numbers that will be used to find the percent difference
        suma = 0
        count = 0

        # Initialize variables that will hold the first row in the time interval
        first_orig = 1
        second_orig = 1

        # Find the last row of the array to avoid going out of bounds
        max_end = np.shape(self.sensor_dict[sensors_compareData_array[0]])[0] - 1

        # Update the first row of the time interval for the first sensor
        # NOTE: It is assumed that the time interval is within the given data set
        while datetime.strptime(self.sensor_dict[first_sensor][first_orig, 0], "%m/%d/%y %H:%M") != start:
            first_orig += 1

        # Update the first row of the time interval for the second sensor
        # NOTE: It is assumed that the time interval is within the given data set
        while datetime.strptime(self.sensor_dict[second_sensor][second_orig, 0], "%m/%d/%y %H:%M") != start:
            second_orig += 1

        # For each row in the time interval
        # NOTE: It is assumed that no time intervals are skipped in either of the sensors
        for row in range(first_orig, max_end):

            # Set the time at the current row in datetime format
            time = datetime.strptime(self.sensor_dict[first_sensor][row, 0], "%m/%d/%y %H:%M")

            # If the time falls between the start and end time
            if time >= start and time <= end:

                # If the data of the correspondent mode is existent in both sensors
                if self.sensor_dict[first_sensor][row, column] and self.sensor_dict[second_sensor][row, column]:

                    # Set a variable holding the data of the correspondent mode for the first sensor
                    initial = self.sensor_dict[first_sensor][row, column].astype(np.float)

                    # Set a variable holding the data of the correspondent mode for the second sensor 
                    final = self.sensor_dict[second_sensor][row, column].astype(np.float)

                    # Add the percent difference to the variable holding all the percent differences
                    suma += (final - initial)/initial

                    # Increase the count of rows considered for this statistic
                    count += 1

            # Update the first_orig and second_orig variables so that
            # the for loop continues with the next row
            first_orig += 1
            second_orig += 1

        # Compute the average percent difference
        percent = suma/count*100

        # Print results on command prompt
        print("Interval: %s - %s" %(start, end))
        print("The %s data of %s is %.2f%% different than the data of %s." %(mode, second_sensor, percent, first_sensor))
        print("\n")
        
