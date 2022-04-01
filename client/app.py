from flask import Flask, request, render_template, redirect, url_for, send_file
from flask_cors import CORS
import config
import requests
import pdfkit

app = Flask(__name__)
CORS(app)

#config stuff
setup = config.Config()

# TODO add validation functions to all resources
# TODO replace all forEach calls with every calls
# TODO remove instances of bootstrap and just use link
# TODO make sure datetimes are local
# TODO convert all tech initials to capital upon entry


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

#Console Log Prices Page
@app.route('/console-gcomm')
def console_gcomm():
    return render_template('consolegcomm.html', host_ip=setup.HOST)

#Console Log Prices Page
@app.route('/techs')
def techs():
    return render_template('techs.html', host_ip=setup.HOST)

#Console Log Prices Page
@app.route('/generate-report')
def generate_report():
    if not request.args:
        return redirect('techs')
    try:
        start = request.args['start']
        end = request.args['end']
    except KeyError:
        return 'Missing or invalid arguments'
    try:
        tech_id = request.args['tech_id']
    except KeyError:
        tech_id = None

    request_headers = {
        'content-type': 'text/html'
    }

    if tech_id:
        html_info = requests.get(f'http://{setup.HOST}:5000/techs/reports?start={start}&end={end}&tech_id={tech_id}', headers=request_headers)
        file_name = f'report_{tech_id}_{start}_{end}'
    else:
        html_info = requests.get(f'http://{setup.HOST}:5000/techs/reports?start={start}&end={end}', headers=request_headers)
        file_name = f'report_all_{start}_{end}'
    

    # html_string = ''
    # with open(f'reports/{file_name}.html', 'w') as file:
    #     file.write(html_info.text)
    # with open(f'reports/{file_name}.html') as file:
    #     html_string = file.read()
    #     print(html_string)

    pdf_options = {
        'page-size': 'Letter',
        'margin-top': '0.5in',
        'margin-right': '0.5in',
        'margin-bottom': '0.5in',
        'margin-left': '0.5in',
        'encoding': 'UTF-8'
    }
    pdfkit.from_string(str(html_info.content).replace('b\'', '').replace('\'', ''), f'reports/{file_name}.pdf', options=pdf_options)
    # pdfkit.from_url(f'http://{setup.HOST}:5000/techs/reports?start={start}&end={end}&tech_id={tech_id}', f'reports/{file_name}.pdf', options=pdf_options)
    # pdfkit.from_file(f'reports/{file_name}.html', f'reports/{file_name}.pdf', options=pdf_options)
    # pdfkit.from_string(html_string, f'reports/{file_name}.pdf', options=pdf_options)

    return send_file(f'reports/{file_name}.pdf', download_name=f'{file_name}.pdf')

#RUN APPLICATION
if __name__ == '__main__':
    app.run(debug=setup.DEBUG, port=setup.PORT, host = setup.HOST)