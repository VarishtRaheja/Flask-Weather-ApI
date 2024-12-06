# Importing the required libraries.

import time
from flask import Flask, render_template
import pandas as pd
from datetime import datetime

app = Flask(__name__)

# Import the stations.txt file. Only keeping about 90 ids.
station_filepath = "weather_data_small/stations.txt"
stations = pd.read_csv(station_filepath,skiprows=17,skipinitialspace=True)[:92]
stations.columns = stations.columns.str.strip()

# Creating the webpages

@app.route("/")
def home():
    # Home page
    return render_template("home.html",station_data= stations.to_html())

@app.route("/api/v1/<station>/<date>")
def about(station,date):
    # Creating columns by values and filtering station, date.
    file = "weather_data_small/TG_STAID"+str(station).zfill(6)+".txt"
    weather_df = pd.read_csv(file,sep=",",skiprows=20,parse_dates=[2],skipinitialspace=True)
    temperature = round(weather_df[weather_df['DATE']==date]['TG'].squeeze() * 0.1,2)
    header = ["Station,Date,Temperature(C)"]
    tableData = [{"Station":station, "Date":date, "Temperature":temperature}]
    return render_template('index.html',headers=header,table_data=tableData)



@app.route("/api/v1/<station>/")
def single_station(station):
    # Filtering temp by station specific
    file = "weather_data_small/TG_STAID"+str(station).zfill(6)+".txt"
    weather_df = pd.read_csv(file,sep=",",skiprows=20,skipinitialspace=True)
    # Drop all row with -9999
    weather_df = weather_df.drop(weather_df[weather_df['TG']==-9999].index)
    
    # Grabbing the station_id and parsing dates.
    station_id = weather_df['STAID'].unique()
    temperature = round(weather_df[weather_df['STAID']==int(station)]['TG'].squeeze()*0.1,2)
    weather_df['DATE'] = weather_df['DATE'].astype("string")
    dates = weather_df['DATE'].apply(lambda x: datetime.strptime(x,"%Y%m%d").strftime("%Y-%m-%d"))

    # Create dictionary
    data = list(zip(dates,temperature))
    return render_template("station.html",station_id=station_id,data=data)


@app.route("/api/v1/yearly/<station>/<year>")
def data_by_year(station,year):
    # Creating JSON records of temp for station,year
    file = "weather_data_small/TG_STAID" + str(station).zfill(6) + ".txt"
    weather_df = pd.read_csv(file, sep=",", skiprows=20, skipinitialspace=True)
    weather_df['DATE'] = weather_df['DATE'].astype(str)
    result = weather_df[weather_df["DATE"].str.startswith(str(year))].to_dict(orient='records')
    return result



# Running the app.

if __name__ == "__main__":
    app.run(debug=True)
    time.sleep(1)