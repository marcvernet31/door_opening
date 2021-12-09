import streamlit as st
import pandas as pd

from UI_params_functions import *

st.title("Tilte")


def importDataset():
    door1 = pd.read_csv("labeled_door1.csv")
    var = door1.x
    var_label = door1.x_label

    return var_label, var

def resultplot(pltRange, var, correctAlarms, falseAlarms, missedAlarms):
    fig = plt.figure()
    for i in correctAlarms:
        if(i > pltRange[0] and i < pltRange[1]):
            plt.axvline(x=i, color='limegreen', linestyle='-')
    for i in falseAlarms:
        if(i > pltRange[0] and i < pltRange[1]):
            plt.axvline(x=i, color='red', linestyle='-')
    for i in missedAlarms:
        if(i > pltRange[0] and i < pltRange[1]):
            plt.axvline(x=i, color='dodgerblue', linestyle='-')
    plt.yticks([])
    plt.plot(var[pltRange[0]:pltRange[1]], color = "black", linewidth=1.9)

    return fig


def main():
    falseAlarms, missedAlarms, correctAlarms, totalAlarms = [], [], [], 0

    varRange = [0, 1000000]
    var_label, var = importDataset()

    drift = float(st.text_input("Drift", value=0.07))
    threshold = float(st.text_input("Threshold", value=0.01))

    if st.button("Calculate"):
        falseAlarms, missedAlarms, correctAlarms, totalAlarms = alarmLabeling(drift, threshold, var, var_label, varRange)
        st.write("falseAlarms", len(falseAlarms))
        st.write("missedAlarms", len(missedAlarms))
        st.write("correctAlarms", len(correctAlarms))
        st.write("totalAlarms", totalAlarms)

        #pltRange = [267000, 272000]

    pltRange = st.slider(
     'Select a range of values',
     varRange[0], varRange[1], (varRange[0], varRange[1]//2))

    if(st.button("Plot")):
        falseAlarms, missedAlarms, correctAlarms, totalAlarms = alarmLabeling(drift, threshold, var, var_label, varRange)
        varRange = pltRange


        fig = resultplot(pltRange, var, correctAlarms, falseAlarms, missedAlarms)
        st.pyplot(fig)


    #st.warning("hola")
    #st.success("ei")
    #st.error("nop")





main()
