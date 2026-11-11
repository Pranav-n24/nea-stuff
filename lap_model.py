import fastf1
import xgboost as xgb
import pandas as pd
from info import getStopLoss, getLaps, getStopTime
def predictBaseLapTime(track, air_temp, surface_temp, compound, tyre_life):
    return 0
#final lap time
def getFinalLapTime(inp_track, inp_at, inp_st, inp_compound, inp_tl, pit_lap):
    base_time = predictBaseLapTime(inp_track, inp_at, inp_st, inp_compound, inp_tl)
    if pit_lap:
        base_time += getStopLoss(inp_track)
        base_time += getStopTime()
    return base_time
##data loader for loading data from the fastf1 api to cache
#def loadData():
#    years = [2024, 2025] # <- step 1
#    years = [2022, 2023] # <- step 2
#    for year in years:
#        schedule = fastf1.get_event_schedule(year)
#        for i, event in schedule.iterrows():
#            try:
#                session = fastf1.get_session(year, event['EventName'], 'R')
#                session.load()
#                print(year, event['EventName'], "loaded")
#            except Exception as e:
#                print("Failed:", year, event['EventName'], e)
##enabling cache
#fastf1.Cache.enable_cache(r"C:\Users\geniu\Desktop\Pranav\Coding\NEA\non-code\cache")
##building the dataset csv
#def buildDataset(target_driver):
#    years = [2022, 2023, 2024, 2025]
#    all_laps = []
#    for year in years:
#        print(f"Processing: {year} season")
#        schedule = fastf1.get_event_schedule(year)
#        #filtering out pre-season testing weekends if any
#        gp_events = schedule[schedule["EventFormat"] != "testing"]
#        for i, event in gp_events.iterrows():
#            try:
#                #load the session, load laps and weather, but not the telemetry
#                session = fastf1.get_session(year, event["EventName"], 'R')
#                session.load(laps = True, telemetry  = False, weather = True)
#                #pulling lap and weather data
#                laps = session.laps.copy()
#                weather = session.weather_data[["Time", "AirTemp", "TrackTemp"]].copy()
#                #data only for max verstappen
#                driver_laps = laps[laps["Driver"] == target_driver].copy()
#                #skip if he DNFed or something
#                if driver_laps.empty:
#                    continue
#                #sort data by time
#                driver_laps = driver_laps.sort_values(by = "Time")
#                weather = weather.sort_values(by = "Time")
#                #merge driver and weather data based on nearest timestamp
#                merged_data = pd.merge_asof(driver_laps, weather, on = "Time", direction = "nearest")
#                #create trackname column (with the event name)
#                merged_data["TrackName"] = event["EventName"]
#                #append data of one race to the main list
#                all_laps.append(merged_data)
#                print(f"Successfully got {target_driver} data for {event["EventName"]}")
#            except Exception as e:
#                print(f"Skipped {year} {event["EventName"]}: {e}")
#    if all_laps:
#        master_df = pd.concat(all_laps, ignore_index = True)
#        master_df["LapTimeSeconds"] = master_df["LapTime"].dt.total_seconds()
#        requested_columns = ["TrackName", "AirTemp", "TrackTemp", "Compound", "TyreLife", "LapTimeSeconds"]
#        final_dataset = master_df[requested_columns].dropna(subset = ["LapTimeSeconds"])
#        return final_dataset
#    else:
#        print("No data found")
#        return None
##building dataset
#def buildDataset():
#    dataset = buildDataset("VER")
#    if dataset is not None:
#        dataset.to_excel(r"C:\Users\geniu\Desktop\Pranav\Coding\NEA\non-code\VerDriverData.xlsx", index = False, sheet_name = "Lap Data")
#    print(f"Data has been successfuly saved to excel")
#none of the 3 methods above need to be used again
#base time predictor