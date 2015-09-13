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

        # Set up an array of times.
        # NOTE: This assumes that all the sensors have the same time array
        self.times_array = self.sensor_dict[self.sensors_array[0]][:,0]

# Derived class of SensorData
class SensorDataStatistics(SensorData):

    def __init__(self, address, network, sensors_allNetwork):
        
        # Call the constructor for the parent class
        SensorData.__init__(self, address, network, sensors_allNetwork)

    def percent_missing_speed(self, sensors_missingData, start, end):

        # Set the column number and mode, corresponding to the way the speed
        # data is organized in the csv file. This is not daily over time
        column = 1
        mode = 'speed'
        daily = False

        # Call the helper function
        return self.percent_missing(column, mode, sensors_missingData, start, end, daily)
        
    def percent_missing_count(self, sensors_missingData, start, end):

        # Set the column number and mode, corresponding to the way the count
        # data is organized in the csv file. This is not daily over time
        column = 2
        mode = 'count'
        daily = False

        # Call the helper function
        return self.percent_missing(column, mode, sensors_missingData, start, end, daily)
    
    def percent_missing_speed_daily(self, sensors_missingData, start, end, daily_start, daily_end):

        # Set the column number and mode, corresponding to the way the speed
        # data is organized in the csv file. This is daily over time
        column = 1
        mode = 'speed'

        # Call helper function
        self.percent_missing_daily(sensors_missingData, start, end, daily_start, daily_end, column, mode)

    def percent_missing_count_daily(self, sensors_missingData, start, end, daily_start, daily_end):

        # Set the column number and mode, corresponding to the way the speed
        # data is organized in the csv file. This is daily over time
        column = 2
        mode = 'count'

        # Call helper function
        self.percent_missing_daily(sensors_missingData, start, end, daily_start, daily_end, column, mode)

    def percent_missing_daily(self, sensors_missingData, start, end, daily_start, daily_end, column, mode):

        # The helper function will be called on daily basis
        daily = True

        # Set the start and end times in datetime format
        start = datetime.strptime(start, "%m/%d/%y %H:%M")
        end = datetime.strptime(end, "%m/%d/%y %H:%M")

        # Set a row not to go over to in the for loop
        max_row = np.shape(self.times_array)[0] - 1

        # Set the rows that delimit the time interval considered
        # If the interval is not found, the function will print a message
        # and return
        first_row = 1
        while datetime.strptime(self.times_array[first_row], "%m/%d/%Y %H:%M") != start:
            first_row += 1
            if first_row == max_row:
                print('Interval could not be found')
                return
        last_row = first_row
        while datetime.strptime(self.times_array[last_row], "%m/%d/%Y %H:%M") != end:
            if last_row == max_row:
                print('Interval could not be found')
                return
            last_row += 1

        # Save the daily start and end strings as datetime
        daily_start = datetime.strptime(daily_start, "%H:%M")
        daily_end = datetime.strptime(daily_end, "%H:%M")

        # Extract the numerical time of the daily start and end times
        daily_start_value = daily_start.hour*60 + daily_start.minute
        daily_end_value = daily_end.hour*60 + daily_end.minute

        # Start a sum that will hold the sum of averages
        suma = 0

        # Start a sum that will hold the number of time intervals
        count = 0

        # Set rows that will be updated as iteration proceeds
        # This will delimit the daily intervals
        start_row = first_row
        end_row = first_row

        # Initialize a checker that will control when the while
        # loop has to end
        check = True

        # Set a time value (in minute granularity) to identify
        # what falls in the daily interval
        time = datetime.strptime(self.times_array[start_row], "%m/%d/%Y %H:%M")
        time_value = time.hour*60 + time.minute

        # Set a granularity to update the time value with
        granularity = 5

        # While the rows are within the time interval
        while check:

            # Find the row numbers for the start (and update end for running time)
            # until they fall in the daily interval and they are within
            # the larger time interval
            while time_value < daily_start_value and start_row < last_row:
                start_row +=  1
                end_row += 1
                
                # Update the time value using the granularity
                time_value = (time_value + granularity)%1440
                
                # Set a marker indicating that a start was found
                mark_start = True

            # Find the row numbers for the end
            while time_value < daily_end_value and end_row < last_row:
                end_row += 1
                time_value = (time_value + granularity)%1440

                # Set a marker indicating that an end was found
                mark_end = True

            # If the end of the larger interval has been reached,
            # don't run the while loop after this iteration
            if end_row == last_row:
                check = False

            # If an interval has been found, call the helper function
            # and update the value holders
            if mark_start and mark_end:
                start_str = self.times_array[start_row]
                end_str = self.times_array[end_row]
                print(start_str)
                start_str = datetime.strptime(start_str, "%m/%d/%Y %H:%M").strftime("%m/%d/%y %H:%M")
                end_str = datetime.strptime(end_str, "%m/%d/%Y %H:%M").strftime("%m/%d/%y %H:%M")
                suma = suma + self.percent_missing(column, mode, sensors_missingData, start_str, end_str, daily)
                count += 1

            # Update values for next loop iteration
            end_row += 1
            start_row = end_row
            time_value = (time_value + granularity)%1440
            mark_start = False
            mark_end = False

        percent = suma/count
        print('The sensors:')
        sensors_missingData_array = np.genfromtxt(sensors_missingData, dtype='str', delimiter=',')
        for sensor in sensors_missingData_array:
            print(sensor)
        print("Missed %.2f%% of the %s data during the daily interval %s - %s between %s - %s." %(percent, mode, daily_start, daily_end, start, end)) 
    
    def percent_missing(self, column, mode, sensors_missingData, start, end, daily):

        # Set the start and end times in datetime format
        start = datetime.strptime(start, "%m/%d/%y %H:%M")
        end = datetime.strptime(end, "%m/%d/%y %H:%M")

        # Load the sensors that will be analyzed
        # NOTE: The csv file must include at least 2 sensors (bug caused by numpy array)
        #       Else, for loop will not work
        sensors_missingData_array = np.genfromtxt(sensors_missingData, dtype='str', delimiter=',')

        # Set variables that will hold the stats for the return value if
        # the function is called as daily
        if daily:
            daily_total = 0
            daily_count = 0

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
                time = datetime.strptime(self.sensor_dict[each_sensor][row, 0], "%m/%d/%Y %H:%M")

                # If the time falls between the start and end time
                if time >= start and time <= end:

                    # Count for total
                    total += 1

                    # If mode is speed, check only for missing cells
                    if mode == 'speed':
                        # If the row is missing the variable of the correspondent mode
                        if not self.sensor_dict[each_sensor][row, column]:
                            missing += 1

                    # Else, mode is count. Check for missing cells and count 0
                    else:
                        if not self.sensor_dict[each_sensor][row, column]:
                            missing += 1
                        elif np.float(self.sensor_dict[each_sensor][row, column]) == 0:
                            missing += 1

            # Check if at least one time inteval was found
            if total == 0:
                print('Time interval not in data base')
                return

            # Compute the percent of data missing for the correspondent mode
            percent = missing/total*100

            # If this is being used to calculate daily info in another function,
            # return the percent
            if daily:
                daily_total += percent
                daily_count += 1
                
            else:
                # Print results on command prompt
                print("Interval: %s - %s" %(start, end))
                print ("%s is missing %.2f%% of the %s data." %(each_sensor, percent, mode))
                print("\n")

        # If the call is daily, return the average for the data set in the csv file
        if daily:
            daily_average = daily_total/daily_count
            return daily_average

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

        # Print an empty line on the command prompt
        print("\n")

        # Set the start and end times in datetime format
        start = datetime.strptime(start, "%m/%d/%y %H:%M")
        end = datetime.strptime(end, "%m/%d/%y %H:%M")

        # Load the PAIR of sensors that will be analyzed
        # NOTE: The csv file must include PAIRS of sensors, where the first one is the 'initial' data
        #       and the second one is the 'final' data (for percent difference computation)
        #       The first sensor is at the top, the second sensor is below it
        #       At least TWO pairs must be in the csv file, else the for loop will not work.
        #       This is due to a array/tuple issue with numpy
        sensors_compareData_array = np.genfromtxt(sensors_compareData, dtype='str', delimiter=',')

        # Set the maximum number of sensor pairs
        columns = np.shape(sensors_compareData_array)[1]

        # Iterate for each pair
        for pair in range (0, columns):

            # Set identifiers for each sensor
            first_sensor = sensors_compareData_array[0, pair]
            second_sensor = sensors_compareData_array[1, pair]

            # Initialize the numbers that will be used to find the percent difference
            suma = 0
            count = 0

            # Initialize variables that will hold the first row in the time interval
            first_orig = 1
            second_orig = 1

            # Find the last row of the array to avoid going out of bounds
            max_end = np.shape(self.sensor_dict[sensors_compareData_array[0, pair]])[0] - 1

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
