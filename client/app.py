from flask import Flask, render_template
from flask_cors import CORS
import config

app = Flask(__name__)
CORS(app)

#config stuff
setup = config.TestConfig()

#HOME
@app.route('/')
def index():
    return render_template('index.html')

#System Logs Page
@app.route('/syslogs')
def syslogs():
    return render_template('syslogs.html', host_ip=setup.HOST)

#G-COMM Logs Page
@app.route('/gcomm')
def gcomm():
    return render_template('gcomm.html', host_ip=setup.HOST)

#RUN APPLICATION
if __name__ == '__main__':
    app.run(debug=setup.DEBUG, port=setup.PORT, host = setup.HOST)