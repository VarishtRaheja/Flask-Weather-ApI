from flask import Flask, render_template
import pandas as pd


app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/api/v1/<station>/<date>")
def about(station,date):
    file = "weather_data_small/TG_STAID"+str(station).zfill(6)+".txt"
    weather_df = pd.read_csv(file,sep=",",skiprows=20,parse_dates=[2],skipinitialspace=True)
    temperature = weather_df[weather_df['DATE']==date]['TG'].squeeze() * 0.1
    header = ["Station,Date,Temperature(C)"]
    tableData = [{"Station":station, "Date":date, "Temperature":temperature}]
    # return {"Station":station, "Date":date, "Temperature(in C)":temperature}
    return render_template('index.html',headers=header,table_data=tableData)

if __name__ == "__main__":
    app.run(debug=True)