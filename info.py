import numpy as np
from scipy.stats import lognorm
#info for each track
#1. pit loss (excluding the stop), 2. no. of laps
track_info = {
    #pit loss, laps, min and max air temp, min and max track temp
    "bahrain": [20.4, 57, 15, 42.6, 22, 56],
    "saudiArabia": [17.2, 50, 24, 35, 32, 61],
    "australia": [16.8, 58, 12.8, 38.2, 19, 50],
    "azerbaijan": [17.2, 51, 21, 33, 25, 52],
    "miami": [16.3, 57, 21.5, 34, 39.8, 56.8],
    "monaco": [17.5, 78, 15, 31.8, 24, 53.9],
    "spain": [19.7, 57, 14, 35, 22, 55],
    "canada": [15.8, 70, 4, 28, 16, 49],
    "austria": [17.8, 71, 13, 35, 20, 58],
    "britain": [17.4, 52, 11, 31, 18, 54],
    "hungary": [18, 70, 14, 35, 22, 58.6],
    "belgium": [16.3, 44, 8, 30, 15, 47],
    "netherlands": [20.3, 72, 14, 24, 18, 32.4],
    "italy": [21.8, 53, 14, 36, 20, 57.1],
    "singapore": [26.6, 62, 24, 33, 32, 40],
    "japan": [21.3, 53, 6, 28, 17, 42],
    "austin": [18.1, 56, 11, 35, 18, 52],
    "mexico": [19.4, 71, 10, 26, 20, 50],
    "saoPaulo": [18.3, 71, 13, 38.2, 18, 60],
    "abuDhabi": [18.5, 58, 22, 30, 28, 47]
}
#function for getting pitting loss 
def getStopLoss(track):
    return track_info[track][0]
#function for grtting the no. of laps
def getLaps(track):
    return track_info[track][1]
#function for getting a random stop loss 
def getStopTime():
    stop_time = lognorm.rvs(s=0.35, loc=1.8, scale=0.9, size=1)[0]
    # 3% chance of a pitstop blunder
    if np.random.random() < 0.03:
        stop_time += np.random.uniform(5, 20)
    return round(stop_time, 2)

def getAtLimit(track):
    return track_info[track][2], track_info[track][3]

def getTtLimit(track):
    return track_info[track][4], track_info[track][5]