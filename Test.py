# -*- coding: utf-8 -*-
"""
@author: Rafael Brandao Ferreira
VERSION: -
DATE: Monday Mar 18 22:54:08 2019
DESCRIPTION: Speed and Distance Calculation with Andro Sensor Data
First Static Code Analysis: -0.18
Last Static Code Analysis: 8.35

TEST CASES:
    Nike Running App for Android was used do verify all the data:
    For data with less than 5 minutes the pythoncode distorces the distance reality for 20%
    However for data more than 5 and more than 8 it becames very real 4%
    4 Types of Data was used, long term (12 minutes, 8 minutes, 6 minutes and 5 minutes)
    test1.csv = walked less and run more in the street
    test2.csv = walked more and run less in the street
    test3.csv = cellphonestopped
    test4.csv = combining stopping, walking and runnin
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy

def select_met(average_speed):
    '''
    Select MET according with the table at:
    https://www.hss.edu/conditions_burning-calories-with-exercise-calculating-estimated-energy-expenditure.asp
    '''
    if average_speed <= 3:
        met_value = 0
    if average_speed > 3 and average_speed <= 5:
        met_value = 5
    if average_speed > 5 and average_speed <= 6.50:
        met_value = 6
    if average_speed > 6.50 and average_speed <= 7.50:
        met_value = 7
    if average_speed > 7.50 and average_speed <= 8.20:
        met_value = 8
    if average_speed > 8.20 and average_speed <= 9.10:
        met_value = 9
    if average_speed > 9.10 and average_speed <= 10.20:
        met_value = 10
    if average_speed > 10.20 and average_speed <= 10.80:
        met_value = 11
    if average_speed > 10.80 and average_speed <= 12.00:
        met_value = 11.5
    if average_speed > 12.00 and average_speed <= 13.80:
        met_value = 12.5
    if average_speed > 13.80 and average_speed <= 14.20:
        met_value = 13.5
    if average_speed > 14.20:
        met_value = 14.5
    return met_value
def calculate_calories(user_kg, user_met, user_time):
    '''
    Calculate calories according with the table at:
    https://www.hss.edu/conditions_burning-calories-with-exercise-calculating-estimated-energy-expenditure.asp
    '''
    total_calories = 0.0175 * user_met*user_time * user_kg
    return total_calories
def calcul_distance(dataset):
    '''
    The function calculates the distance traveled
    '''
    dis_traveled = dataset[len(dataset)-1]
    return  dis_traveled

def calcul_time(dataset):
    '''
    The function calculates the time traveled
    '''
    time_traveled = dataset[len(dataset)-1]
    return  time_traveled
def max_speed(dataset):
    '''
    The function calculates the max speed
    '''
    max_value = 0
    size_data = len(dataset) - 1
    for values_data in range(size_data):
        if dataset[values_data] > max_value:
            max_value = dataset[values_data]
    return max_value
def calcul_rms(total_distance, user_time):
    '''
    The function calculates the rms value of a data
    '''
    average_value = total_distance*60/(1000*user_time)
    return average_value
def double_integration(vect_x, vect_y, vect_z, velocity_init, position_init, delta_t):
    '''
    The function calculates double integration in the acceleration to have speed and distance
    '''
    taille_vect = len(vect_x)
    velocity_x = [0]
    velocity_y = [0]
    velocity_z = [0]
    position_x = [0]
    position_y = [0]
    position_z = [0]
    time_stopped = 0
    for i in range(taille_vect):
        if i == 1:
            velocity_x.append(velocity_init[0])
            velocity_y.append(velocity_init[1])
            velocity_z.append(velocity_init[2])

            position_x.append(position_init[0])
            position_y.append(position_init[1])
            position_z.append(position_init[2])
        if i == 2:
            if vect_x[i] < 2 and vect_x[i] > -2:
                velocity_x.append(0)
            else:
                velocity_x.append(velocity_init[0]+integration_trapeze_init(velocity_init[0], i, vect_x, delta_t[i]))
            if vect_y[i] < 2 and vect_y[i] > -2:
                velocity_y.append(0)
            else:
                velocity_y.append(velocity_init[1]+integration_trapeze_init(velocity_init[1], i, vect_y, delta_t[i]))
            if vect_z[i] < 2 and vect_z[i] > -2:
                velocity_z.append(0)
            else:
                velocity_z.append(velocity_init[2]+integration_trapeze_init(velocity_init[2], i, vect_z, delta_t[i]))
            position_x.append(position_init[0]+integration_trapeze_init(position_init[0], i, velocity_x, delta_t[i]))
            position_y.append(position_init[1]+integration_trapeze_init(position_init[1], i, velocity_y, delta_t[i]))
            position_z.append(position_init[2]+integration_trapeze_init(position_init[2], i, velocity_z, delta_t[i]))
        if i > 2:
            #ipdb.set_trace()
            if vect_x[i] < 2.5 and vect_x[i] > -2.5:
                velocity_x.append(0)
            else:
                velocity_x.append(velocity_x[i-1]+integration_trapeze(i-1, i, vect_x, delta_t[i]))
            if vect_y[i] < 2.5 and vect_y[i] > -2.5:
                velocity_y.append(0)
            else:
                velocity_y.append(velocity_y[i-1]+integration_trapeze(i-1, i, vect_y, delta_t[i]))
            if vect_y[i] < 2.5 and vect_y[i] > -2.5:
                velocity_z.append(0)
            else:
                velocity_z.append(velocity_z[i-1]+integration_trapeze(i-1, i, vect_z, delta_t[i]))
            if velocity_x[i] < 5:
                position_x.append(position_x[i-1])
            else:
                position_x.append(position_x[i-1]+integration_trapeze(i-1, i, velocity_x, delta_t[i]))
#            position_x.append(position_x[i-1]+integration_trapeze(i-1, i, velocity_x, delta_t[i]))
            if velocity_y[i] < 5:
                position_y.append(position_y[i-1])
            else:
                position_y.append(position_y[i-1]+integration_trapeze(i-1, i, velocity_y, delta_t[i]))
            if velocity_z[i] < 5:
                position_z.append(position_z[i-1])
            else:
                position_z.append(position_z[i-1]+integration_trapeze(i-1, i, velocity_z, delta_t[i]))
            teste_time = velocity_x[i] + velocity_y[i] + velocity_z[i]
            if teste_time == 0:
                time_stopped = time_stopped + delta_t[i]
    velocity = np.array([velocity_x, velocity_y, velocity_z])
    position = np.array([position_x, position_y, position_z])
    return velocity, position, time_stopped

def integration_trapeze(new_data, past_data, data_vector, delta_t):
    '''
    The function integrates with trapeze mode
    '''
    f_a = data_vector[new_data]
    f_b = data_vector[past_data]
    val_int = (f_a+f_b)/2.
    val_int *= delta_t

    return val_int

def integration_trapeze_init(val_init, past_data, data_vector, delta_t):
    '''
    The function integrates with trapeze mode just for the fist integration
    '''
    f_a = val_init
    f_b = data_vector[past_data]
    val_int = (f_a+f_b)/2.
    val_int *= delta_t

    return val_int


USER_FILE = pd.read_csv('test1.csv')
USER_FILE.columns = USER_FILE.columns.str.replace('/', '')
USER_FILE.columns = USER_FILE.columns.str.replace('²', '2')
USER_FILE.columns = USER_FILE.columns.str.replace('°', '0')
USER_FILE.columns = USER_FILE.columns.str.replace('-', '')
USER_FILE.columns = USER_FILE.columns.str.replace('_', '')
USER_FILE.columns = USER_FILE.columns.str.replace('(', '')
USER_FILE.columns = USER_FILE.columns.str.replace(')', '')
USER_FILE.columns = USER_FILE.columns.str.replace(':', '')
USER_FILE.columns = USER_FILE.columns.str.replace(' ', '')

VEL_INITIAL = [0, 0, 0]
POS_INITIAL = [0, 0, 0]
DELTA_TIME = []
WEIGHT = 100
USER_FILE['Timesincestartinms'] = USER_FILE['Timesincestartinms']/60000

TIMETRAVELED = calcul_time(USER_FILE['Timesincestartinms'])
if TIMETRAVELED < 5:
    print('---------------')
    print('Your data is short, please select a data with more than 5 minutes')
    print('This is a limitation of the program')
else:
    for x in range(len(USER_FILE['Timesincestartinms'])):
        DELTA_TIME.append(0.5)    
    VEL_POS = double_integration(USER_FILE['LINEARACCELERATIONXms2'], USER_FILE['LINEARACCELERATIONYms2'], USER_FILE['LINEARACCELERATIONZms2'], VEL_INITIAL, POS_INITIAL, DELTA_TIME)
    SPEED = VEL_POS[0]
    DISTANCE = VEL_POS[1]
    TIMESTOPPED = VEL_POS[2]/60
    SPEEDREAL = SPEED[0, :]**2 + SPEED[1, :]**2 + SPEED[2, :]**2
    SPEEDREAL = SPEEDREAL**0.5
    DISTANCEREAL = DISTANCE[0, :]**2 + DISTANCE[1, :]**2 + DISTANCE[2, :]**2
    DISTANCEREAL = DISTANCEREAL**0.5
    FFT = scipy.fft(SPEEDREAL) # (G) and (H)
    BP = FFT[:]
    for j in range(len(BP)): # (H-red)
        if j >= 50:
            BP[j] = 0
    IBP = scipy.ifft(BP)
    X = USER_FILE['Timesincestartinms'].as_matrix()
    Y = SPEEDREAL
    FIG = plt.figure()
    AXES = FIG.add_axes([0, 0, 1, 1])
    AXES.plot(X, Y, 'r')
    AXES.set_title('Speed x Time')
    plt.xlabel("Minutes")
    plt.ylabel("m/s")
    
    X = USER_FILE['Timesincestartinms'].as_matrix()
    Y = IBP
    FIG = plt.figure()
    AXES = FIG.add_axes([0, 0, 1, 1])
    AXES.plot(X, Y, 'r')
    AXES.set_title('Speed x Time')
    plt.xlabel("Minutes")
    plt.ylabel("m/s")
    
    #raiz da media * offset de cada eixo * 1,2
    X = USER_FILE['Timesincestartinms'].as_matrix()
    Y = DISTANCEREAL
    FIG = plt.figure()
    AXES = FIG.add_axes([0, 0, 1, 1])
    AXES.plot(X, Y, 'b')
    AXES.set_title('Distance x Time')
    plt.xlabel("Minutes")
    plt.ylabel("Meters")
    
    DISTANCETRAVELED = calcul_distance(DISTANCEREAL)
    TIMETRAVELED = calcul_time(USER_FILE['Timesincestartinms'])
    #SPEEDMAX = max_speed(IBP)
    MEDIA = calcul_rms(DISTANCETRAVELED, TIMETRAVELED)
    METVALUE = select_met(MEDIA)
    CALORIES = calculate_calories(WEIGHT, METVALUE, TIMETRAVELED)
    
    print('-----------------------------')
    print('DISTANCE TRAVELED %.2f m' % DISTANCETRAVELED)
    print('TIME TRAVELED %.2f min' % TIMETRAVELED)
    print('AVERAGE SPEED %.2f km/h' % MEDIA)
    print('YOU STOPPED FOR %.2f min1' % TIMESTOPPED)
    print('TOTAL CALORIES %.2f kcal' % CALORIES)
    print('-----------------------------')
