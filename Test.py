# -*- coding: utf-8 -*-

"""
Description: Andro Sensor

@author: rafaelb1
"""
import pandas as pd
import matplotlib.pyplot as plt

#df_csv = pd.read_csv('androsensor.csv', names=['LUX', 'VOLUME', 'TIME'], header=1)
#print(andro_sensor)
print("The file must be inside of: D:\Training Camp\Module 5 - Python")
print("--------------------------------------------------------------")
FILE_REQUESTED = input("Please write the name of the file: ")
if '.csv' not in FILE_REQUESTED:
    FILE_REQUESTED = FILE_REQUESTED + ".csv"
USER_FILE = pd.read_csv(FILE_REQUESTED)
COLS = USER_FILE.columns.tolist()
NUMBER_COLS = 0
for x in COLS:
    print(x)
    NUMBER_COLS += 1
X_VARIABLE = input("Select the variable above to be in X axis on graphic: ")
Y_VARIABLE = input("Select the variable above to be in Y axis on graphic: ")
i = 0
for x in COLS:
    if X_VARIABLE not in x.lower():
        i += 1
        continue
    break
TESTE = i - NUMBER_COLS + 1
if TESTE == 0:
    TESTE = None
X_LINE = str(COLS[i])
print(format(X_LINE))
X = USER_FILE[X_LINE].as_matrix()
i = 0
for y in COLS:
    if Y_VARIABLE not in y.lower():
        i += 1
        continue
    break
TESTE = i - NUMBER_COLS + 1
if TESTE == 0:
    TESTE = None
Y_LINE = str(COLS[i])
Y = USER_FILE[Y_LINE].as_matrix()
print(format(Y_LINE))
FIG = plt.figure()
AXES = FIG.add_axes([0.1, 1, 0.4, 0.7])
AXES.plot(X, Y, 'b')
AXES.set_xlabel(X_LINE)
AXES.set_ylabel(Y_LINE)
AXES.set_title('Graphic')
