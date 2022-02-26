from flask import Flask, request, render_template, redirect, url_for
from flask_cors import CORS
import config

app = Flask(__name__)
CORS(app)

#config stuff
setup = config.Config()

# TODO add validation functions to all resources

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

#Work Orders Page
@app.route('/work-orders')
def work_orders():
    return render_template('work-orders.html', host_ip=setup.HOST)

#Work Orders Archive Page
@app.route('/work-orders-archive')
def work_orders_archive():
    return render_template('work-orders-archive.html', host_ip=setup.HOST)

#Work Orders Edit Page
@app.route('/work-orders-edit')
def work_orders_edit():
    if not request.args.get('id'):
        return redirect(url_for('work_orders'))
    else:
        return render_template('work-orders-edit.html', host_ip=setup.HOST, wo_id=request.args.get('id'))

#General Prices Page
@app.route('/prices')
def prices():
    return render_template('prices.html', host_ip=setup.HOST)

#Game Prices Page
@app.route('/game-prices')
def game_prices():
    return render_template('game_prices.html', host_ip=setup.HOST)

#Console Log Prices Page
@app.route('/consolelogs')
def consolelog():
    return render_template('consolelog.html', host_ip=setup.HOST)

#RUN APPLICATION
if __name__ == '__main__':
    app.run(debug=setup.DEBUG, port=setup.PORT, host = setup.HOST)