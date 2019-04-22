from flask import Flask, render_template, request
import pandas as pd
import pandas_highcharts.core
from sqlalchemy import create_engine
import yaml

app = Flask(__name__)

@app.route('/graph')
def graph():
    with open('config.yml', 'r') as c:
        conf = yaml.load(c)

    db_url = conf['DB']

    engine = create_engine(db_url, echo=False)
    query = ("select cast(value as INTEGER ) temp, sensor, create_date from sensors where sensor = 'temperature' ")

    temp = pd.read_sql(query, engine)

    temp_chart = pandas_highcharts.core.serialize(temp,
                                          title='Temperature',
                                          render_to='Temperature',
                                          output_type='json',
                                          y=['temp'])

    query = ("select cast(value as INTEGER ) hum, sensor, create_date from sensors where sensor = 'humidity' ")

    hum = pd.read_sql(query, engine)

    hum_chart = pandas_highcharts.core.serialize(hum,
                                          title='Humidity',
                                          render_to='Humidity',
                                          output_type='json',
                                          y=['hum'])

    query = ("select cast(value as INTEGER ) led, sensor, create_date from sensors where sensor = 'light' ")

    led = pd.read_sql(query, engine)

    led_chart = pandas_highcharts.core.serialize(led,
                                          title='Light',
                                          render_to='Light',
                                          output_type='json',
                                          y=['led'])

    query = ("select cast(value as INTEGER ) light, sensor, create_date from sensors where sensor = 'light_intensity' ")

    light = pd.read_sql(query, engine)

    light_chart = pandas_highcharts.core.serialize(light,
                                          title='Light Intensity',
                                          render_to='Light_Intensity',
                                          output_type='json',
                                          y=['light'])

    return render_template('index.html', temp_chart=temp_chart, hum_chart=hum_chart, led_chart=led_chart, light_chart=light_chart)