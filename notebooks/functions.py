import pandas as pd
from matplotlib import pyplot as plt

import numpy as np

def calculateMedian(i, variable, size):        
    start = max(i - size, 0) 
    end = min(i, len(variable)) 

    calculate_median = variable[start:end]
    calculate_median.sort()
    if(len(calculate_median) > 0): median = calculate_median[len(calculate_median)//2]
    else: median = variable[i]
        
    return median

def rolling_media(i, variable, size, variableMedian):
    median = calculateMedian(i, variable, size)
    variableMedian.append(median)
    
def cummulative_sum(i, variableMedian, gMax, gMin, drift):
        s_i = variableMedian[i] - variableMedian[i-1]
        
        gMax_i = max(gMax[i-1] + s_i - drift, 0)

        gMin_i = max(gMin[i-1] - s_i - drift, 0)
        gMax.append(gMax_i)
        gMin.append(gMax_i)
        return gMax_i, gMin_i


# All the iterative process into one function for easynes of study
# On the final model all variables have to be analysed in parallel (this function can't be used)

def generate_analysis(variable, size, drift, threshold, samples):

    ### MEDIAN values #####

    variableMedian = list()   # median stored


    #### CUSUM values #####

    alarms = list()           # Points where a movement change is detected
    opening = list()          # Points when an upward movement is detected
    closing = list()          # Points when an downward movement is detected

    s = list([0])             # internal variables for CUSUM
    gMax = list([0])
    gMin = list([0])


    ### STEP Detection ####

    alarmDetected = False
    alarmInterval = 10             # Alarms closer than this will be considerated consecutive
    alarmCounter = 0               # Counter of consecutive alarms
    change = list()                # Cumulative alarms


    closingDetected = False
    openingDetected = False
    lastClosing = -1               # Index of last closing
    lastOpening = -1               # Index of last opening
    lastAlarm = -1                 # Index of last alarm



    ### Slope ponderation ####

    slope = list([0])              # Storing slope


    for i in range(0, samples):
        start = max(i - size, 0) 
        end = min(i, len(variable)) 

        calculate_median = variable[start:end]
        calculate_median.sort()
        if(len(calculate_median) > 0): median = calculate_median[len(calculate_median)//2]
        else: median = variable[i]
        variableMedian.append(median)
        
        ###### CUSUM intervals #####
        # Detect growing and decreasing tendences on the median,
        # Results in a list of indexes of changes
        if(i != 0):

            gMax_i, gMin_i = cummulative_sum(i, variableMedian, gMax, gMin, drift)

            alarmDetected = gMax_i > threshold or gMin_i > threshold
            if(alarmDetected): alarms.append(i)

            openingDetected = gMax_i > threshold
            if(openingDetected): opening.append(i)

            closingDetected = gMin_i > threshold
            if(closingDetected): closing.append(i)


        ### Slope ponderation ####
        # Calculate the slope of the median to ponderate with the added value in case 
        # of positive alarm. Helps define the intervals with more precision, solve errors
        # in definition and provides an aproximation of speed

        # (fun(i) - fun(j) / (i-j)) # i-j is constant, j = i - 1
        if(i != 0): slope.append(variableMedian[i] - variableMedian[i-1])


        #### Step Detection #####
        # Apply ponderation an calculate cumulative movement

        if(alarmDetected):
            alarmCounter += (1 * slope[i])
            lastAlarm = i

        elif(lastAlarm > i - alarmInterval):  # Interval exceded
            alarmCounter += (1 * slope[i])

        else:
            alarmCounter = 0

        change.append(alarmCounter)   

        
    return variableMedian, change, opening, closing