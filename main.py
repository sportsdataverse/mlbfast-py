from mlbfast.players import *
from mlbfast.stats import *
import pandas as pd


#pullCopyrightInfo()
#print('Improper input for the isActive input. \nIf you want active players, set isActive to "Y" or "Yes". \nIf you want inactive players, set isActive to "N" or "No".\n\nIn the meantime, your search will search for all players in MLB history.')
df = getSeasonHittingStats(493316,"R",2017)
print(df)
df.to_csv('test.csv')