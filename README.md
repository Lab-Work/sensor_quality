# ICT R27-155 Data Quality

## 1) Overview
This repository contains code that computes simple data quality measures for the data set used in *ICT R27-155*. Namely, it can determine the percentages of data missing in a set of sensors for a given time period, and the percentage differences between sensor pairs for a given time period. The sets of sensors and the intervals studied are user-specified, based on the files provided.

## 2) License

This software is available under the permissive University of Illinois/NCSA Open Source License.

Copyright (c) 2015 The Board of Trustees of the University of Illinois. All rights reserved

Developed by: Department of Civil and Environmental Engineering University of Illinois at Urbana-Champaign

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal with the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions: Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimers. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimers in the documentation and/or other materials provided with the distribution. Neither the names of the Department of Civil and Environmental Engineering, the University of Illinois at Urbana-Champaign, nor the names of its contributors may be used to endorse or promote products derived from this Software without specific prior written permission.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE CONTRIBUTORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS WITH THE SOFTWARE.

## 3) Folders

### /sensor_quality
This folder contains the Python code used to assess data quality. There are two files:
#### assess_quality.py
This script runs the code that computes the data quality measures. There are two sections that need to be user-specified:

##### Input Parameters
This section must be filled-in by the user with parameters regarding the time intervals (e.g., an entire month) and subintervals (e.g., 9:00 AM - 10:00 AM for an entire month), as well as the the work zone under study ('I57I64' or 'I80'). The datetime formats are "%m/%d/%Y %H:%M" and "%H:%M".
##### Functions
Lines in this section must be commented/uncommented based on the user's needs. These functions belong to the sensor_quality class. They use the Input Parameters defined by the user. The functions are described next:
######percent_missing_speed(missing_data_sensors, initial, final)
This function computes the percentages of missing speed data for each of the senosrs in the missing_data_sensors.csv configuration file, starting on datetime *initial* and ending on datetime *final*.
######percent_missing_count(missing_data_sensors, initial, final)
This function computes the percentages of missing count data for each of the senosrs in the missing_data_sensors.csv configuration file, starting on datetime *initial* and ending on datetime *final*.
######percent_missing_speed_subinterval(missing_data_sensors, initial, final, start, end)
This function computes the percentages of missing speed data for each of the senosrs in the missing_data_sensors.csv configuration file, starting on datetime *initial* and ending on datetime *final* for the subintervals starting at *start* and ending at *end*.
######percent_missing_count_subinterval(missing_data_sensors, initial, final, start, end)
This function computes the percentages of missing count data for each of the sensors in the missing_data_sensors.csv configuration file, starting on datetime *initial* and ending on datetime *final* for the subintervals starting at *start* and ending at *end*.
######percent_difference_speed(different_data_sensors, initial, final)
This function computes the speed data percentage differences between each of the sensor pairs in the different_data_sensors.csv configuration file, starting on datetime *initial* and ending on datetime *final*.
######percent_difference_count(different_data_sensors, initial, final)
This function computes the count data percentage differences between each of the sensor pairs in the different_data_sensors.csv configuration file, starting on datetime *initial* and ending on datetime *final*.
######percent_difference_speed_subinterval(different_data_sensors, initial, final, start, end)
This function computes the speed data percentage differences between each of the sensor pairs in the different_data_sensors.csv configuration file, starting on datetime *initial* and ending on datetime *final* for the subintervals starting at *start* and ending at *end*.
######percent_difference_count_subinterval(different_data_sensors, initial, final, start, end)
This function computes the count data percentage differences between each of the sensor pairs in the different_data_sensors.csv configuration file, starting on datetime *initial* and ending on datetime *final* for the subintervals starting at *start* and ending at *end*.

#### sensor_quality.py
This code contains the sensor_quality class. This class is instantiated on the assess_quality.py script. 


### /configuration_files
This folder contains the configuration files needed to run the code.

#### all_sensors.csv
This file must contain the sensorIDs of **all the files** needed to be studied when the code runs. It consists of a single column with header *sensorID*. Include the sensorIDs (using the format explained in /data) of the relevant sensors, one per row.

#### missing_data_sensors.csv
This file must contain the sensorIDs of the **files to be assessed for missing data** when the code runs. It consists of a single column with header *sensorID*. Include the sensorIDs (using the format explained in /data) of the relevant sensors, one per row.

#### different_data_sensors.csv
This file must contain the sensorIDs of the **files to be assessed for sensor consistency** when the code runs. It consists of
two columns with headers *initial_sensorID* and *final_sensorID*. Include the sensorIDs (using the format explained in /data) of the relevant sensors, two per row and separated by a comma. Using this file, the data of the *final sensor* is compared against the data of the *initial sensor*.

### /data
This folder contains .csv files exported from JamLogic for each of the sensor systems used in *R27-155*. These files are organized by the road under study: I57I64 and I80. The files are named using the following convention:
- The first letter of each file indicates the direction of the road on which the sensor is located (Eastbound: E, Westbound: W, Southbound: S, Northbound: N).
- The numbers following the first letter are ordered based on the sensor deployment configuration, starting with 1.

#### /I57I64
This folder contains the files corresponding to the sensors deployed on the I57-I64 work zone.

#### /I80
This folder contains the files corresponding to the sensors deployed on the I80 work zone.

## 4) Running the Code
Python is needed to run this code. To run the code, follow the next instructions:
 1. Fill in the Input Parameters specified in assess_quality.py
 2. Comment/Uncomment with a '#' the functions of interest.
 3. Run assess_quality.py using Python. The results will be displayed on the command line.
