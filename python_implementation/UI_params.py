import streamlit as st
import pandas as pd
import time

from UI_params_functions import *

def importDataset(dfSelected, varSelected):
    if(dfSelected == "Door1"):
        door1 = pd.read_csv("labeled_door1.csv")
        var = door1[varSelected]
        var_label = door1[f"{varSelected}_label"]

        return var_label, var
    if(dfSelected == "Door2"):
        st.warning("Door2 not supported yet")

def resultplot(pltRange, var, correctAlarms, falseAlarms, missedAlarms):
    fig = plt.figure()
    for i in correctAlarms:
        if(i > pltRange[0] and i < pltRange[1]):
            line1 = plt.axvline(x=i, color='limegreen', linestyle='-')
    for i in falseAlarms:
        if(i > pltRange[0] and i < pltRange[1]):
            line2 = plt.axvline(x=i, color='red', linestyle='-')
    for i in missedAlarms:
        if(i > pltRange[0] and i < pltRange[1]):
            line3 = plt.axvline(x=i, color='dodgerblue', linestyle='-')
    plt.yticks([])
    plt.plot(var[pltRange[0]:pltRange[1]], color = "black", linewidth=1.9)


    if(len(correctAlarms) == 0): fig.legend([line2, line3], ['False label', 'Missed label'])
    elif(len(falseAlarms) == 0): fig.legend([line1, line3], ['Correct label', 'Missed label'])
    elif(len(missedAlarms) == 0): fig.legend([line1, line2], ['Correct label', 'False label'])
    else: fig.legend([line1, line2, line3], ['Correct label', 'False label', 'Missed label'])

    return fig


def main():


    falseAlarms, missedAlarms, correctAlarms, totalAlarms = [], [], [], 0

    st.title("Accuracy Calculator")

    dfSelected = st.selectbox('Door', ("Door1", "Door2"))
    varSelected = st.selectbox('Variable', ('x', 'y', 'z'))

    drift = float(st.text_input("Drift", value=0.07))
    threshold = float(st.text_input("Threshold", value=0.01))


    varRange = [0, 1000000]
    var_label, var = importDataset(dfSelected, varSelected)

    if st.button("Calculate"):

        start = time.time()
        falseAlarms, missedAlarms, correctAlarms, totalAlarms = alarmLabeling(drift, threshold, var, var_label, varRange)
        end = time.time()

        col1, col2 = st.beta_columns(2)
        with col1:
            falseAlarms_percent = round(len(falseAlarms)/totalAlarms*100, 2)
            missedAlarms_percent = round(len(missedAlarms)/totalAlarms*100, 2)
            correctAlarms_percent = round(len(correctAlarms)/totalAlarms*100, 2)
            st.write("False alarms: ", len(falseAlarms), f"{falseAlarms_percent}%")
            st.write("Missed Alarms: ", len(missedAlarms), f"{missedAlarms_percent}%")
            st.write("Correct Alarms: ", len(correctAlarms), f"{correctAlarms_percent}%")
            st.write("Total Alarms: ", totalAlarms)
            st.write("Execution Time: ", f"{round(end-start, 1)}s")
        with col2:
            st.warning("warnong")

    st.title("Result plot")
    a = st.number_input('Plot range min', min_value=varRange[0], max_value=varRange[1], value=0)
    b = st.number_input('Plot range max', min_value=a, max_value=varRange[1], value=5000)

    if(st.button("Plot")):
        falseAlarms, missedAlarms, correctAlarms, totalAlarms = alarmLabeling(drift, threshold, var, var_label, varRange)
        fig = resultplot([a, b], var, correctAlarms, falseAlarms, missedAlarms)
        st.pyplot(fig)

    with st.beta_expander("How to choose the parameters"):
        st.write("""
            Start with a very large threshold \n
            Choose drift to one half of the expected change, or adjust drift such that g = 0 more than 50% of the time. \n
            Then set the threshold so the required number of false alarms (this can be done automatically) or delay for detection is obtained. \n
            If faster detection is sought, try to decrease drift \n
            If fewer false alarms are wanted, try to increase drift \n
            If there is a subset of the change times that does not make sense, try to increase drift \n
        """)

main()
