import re
import gunicorn.app.base
import flask
from flask import Flask, request
import backend.weather_service as service
from backend.objects import Cache

app = Flask(__name__)
cache = Cache()

app.template_folder='/home/ubuntu/app/templates'

@app.route('/', methods=['GET'])
def home():
    return flask.render_template('page.html', week=None)


@app.route('/result', methods=['GET', 'POST'])
def result():
    """
        render with week weather
    :return: render
    """
    var = request.form.get('location')
    loc = None
    if len(str(var)) > 85:
        pass
    elif not re.search('^[A-Za-z0-9 ,-]*$', str(var)):
        pass
    elif str(var) == '':
        pass
    else:
        loc = service.get_weather(var, cache)
    return flask.render_template('page.html', week=loc)

if __name__ == '__main__':
    app.run(debug=True)
