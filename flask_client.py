from flask import Flask, render_template, request
import pandas as pd
import pandas_highcharts.core
from sqlalchemy import create_engine
import yaml

app = Flask(__name__)

# creating an endpoint /graphs
@app.route('/graph')
def graph():
    # loading config.yml file
    with open('config.yml', 'r') as c:
        conf = yaml.load(c)

    # extracting db connection
    db_url = conf['DB']

    # opening connection to the db
    engine = create_engine(db_url, echo=False)
    # query string for temp values
    query = ("select cast(value as INTEGER ) temp, sensor, create_date from sensors where sensor = 'temperature' order by create_date desc limit 100 ")

    temp = pd.read_sql(query, engine)

    # setting pandas_higcharts for temp graph
    temp_chart = pandas_highcharts.core.serialize(temp,
                                          title='Temperature',
                                          render_to='Temperature',
                                          output_type='json',
                                          y=['temp'])
    # query string for hum values
    query = ("select cast(value as INTEGER ) hum, sensor, create_date from sensors where sensor = 'humidity' order by create_date desc limit 100 ")

    hum = pd.read_sql(query, engine)
    # setting pandas_higcharts for hum graph
    hum_chart = pandas_highcharts.core.serialize(hum,
                                          title='Humidity',
                                          render_to='Humidity',
                                          output_type='json',
                                          y=['hum'])
    # query string for led values
    query = ("select cast(value as INTEGER ) led, sensor, create_date from sensors where sensor = 'light' order by create_date desc limit 100 ")

    led = pd.read_sql(query, engine)
    # setting pandas_higcharts for led graph
    led_chart = pandas_highcharts.core.serialize(led,
                                          title='Light',
                                          render_to='Light',
                                          output_type='json',
                                          y=['led'])
    # query string for light sensor values
    query = ("select cast(value as INTEGER ) light, sensor, create_date from sensors where sensor = 'light_intensity' order by create_date desc limit 100 ")

    light = pd.read_sql(query, engine)
    # setting pandas_higcharts for light sensor graph
    light_chart = pandas_highcharts.core.serialize(light,
                                          title='Light Intensity',
                                          render_to='Light_Intensity',
                                          output_type='json',
                                          y=['light'])

    # rendering objects into index.html
    return render_template('index.html', temp_chart=temp_chart, hum_chart=hum_chart, led_chart=led_chart, light_chart=light_chart)