from typing import List, Dict
import simplejson as json
from flask import Flask, request, Response, redirect
from flask import render_template
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor
from dateutil.parser import parse

app = Flask(__name__)
mysql = MySQL(cursorclass=DictCursor)

app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 32000
app.config['MYSQL_DATABASE_DB'] = 'covidInsight'
mysql.init_app(app)

@app.route('/', methods=['GET'])
def index():
    user = {'username': 'covid Project'}
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT id,date,positive,negative,hospitalizedCurrently,onVentilatorCurrently,death,recovered FROM us_covid19_daily')
    result = cursor.fetchall()
    return render_template('home.html', title='Home', user=user, covid=result)



@app.route('/statistics', methods=['GET'])
def statistics():
    return render_template('chart.html', title='Statistics')


@app.route('/api/v1/covid', methods=['GET'])
def api_browse():
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT id,date,positive,negative,hospitalizedCurrently,onVentilatorCurrently,death,recovered FROM us_covid19_daily')
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp

@app.route('/api/v1/covid/death', methods=['GET'])
def api_death():
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT id,date,death FROM us_covid19_daily order by  date')
    result = cursor.fetchall()
    dates = []
    deaths = []
    for row in result:
        date = parse(row['date'])
        dates.append(date.strftime('%b %d, %y'))
        deaths.append(row['death'])
    result = {
        'dates': dates,
        'deaths': deaths,
    }
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp

@app.route('/api/v1/covid/positive', methods=['GET'])
def api_positive_Negative():
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT id,date,positive,negative FROM us_covid19_daily order by date')
    result = cursor.fetchall()
    dates = []
    postive =[]
    negative = []
    for row in result:
        date = parse(row['date'])
        dates.append(date.strftime('%b %d, %y'))
        postive.append(row['positive'])
        negative.append(row['negative'])
    result = {
        'dates': dates,
        'positive': postive,
        'negative': negative
    }

    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp

@app.route('/api/v1/covid/<chart_type>', methods=['GET'])
def api_covid_type(chart_type):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT id,date,' + chart_type + ' FROM us_covid19_daily order by date')
    result = cursor.fetchall()
    dates = []
    chart_data =[]
    for row in result:
        date = parse(row['date'])
        dates.append(date.strftime('%b %d, %y'))
        if row[chart_type] == None:
            chart_data.append(0)
        else:
            chart_data.append(row[chart_type])
    result = {
        'dates': dates,
        'chart_data': chart_data
    }

    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp

@app.route('/api/v1/covid/Increse', methods=['GET'])
def api_positive_Negative_Increse():
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT substr(date,5,2) as month,sum(positiveIncrease) as positiveIn,sum(negativeIncrease) as negativeIn FROM us_covid19_daily group by substr(date,5,2) ')
    result = cursor.fetchall()
    print(result)
    dates = []
    positiveIncrease = []
    negativeIncrease = []
    for row in result:

        dates.append(row['month'])
        positiveIncrease.append(row['positiveIn'])
        negativeIncrease.append(row['negativeIn'])
    result = {
        'dates': dates,
        'postiveIncrese': positiveIncrease,
        'negativeIncrease': negativeIncrease
    }
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)