from flask import Flask, request, render_template, redirect, url_for, send_file, make_response, jsonify
from flask_cors import CORS
import config
import requests
import pdfkit
from PyPDF2 import PdfFileMerger
import os
import json

app = Flask(__name__)
CORS(app)

#config stuff
setup = config.Config()

# TODO add validation functions to all resources
# TODO replace all forEach calls with every calls
# TODO remove instances of bootstrap and just use link
# TODO make sure datetimes are local
# TODO convert all tech initials to capital upon entry
# TODO autofocus tech input on submission entry
# TODO go to new location instead of refresh

#HOME
@app.route('/')
def index():
    return render_template('index.html')

#System Logs Page
@app.route('/syslogs')
def syslogs():
    return render_template('syslogs.html', host_ip=setup.HOST)

# System Log API
@app.route('/api/v1/syslogs',methods=['GET','POST'])
def syslogs_api_mass():
    if request.method == 'GET':
        syslog_json = requests.get(f'{setup.DATABASE_URL}/syslogs').json()
        print(syslog_json)
        return make_response(jsonify(syslog_json), 200)
    if request.method == 'POST':
        syslog_json =requests.post(f'{setup.DATABASE_URL}/syslogs', data=request.data).json()
        print(syslog_json)
        return make_response(jsonify(syslog_json), 201)
    return make_response(jsonify({'error': 'invalid HTTP request made to server'}), 400)

# System Log API Single
@app.route('/api/v1/syslogs/<log_id>',methods=['GET','PUT', 'DELETE'])
def syslogs_api_single(log_id):
    if request.method == 'GET':
        syslog_json = requests.get(f'{setup.DATABASE_URL}/syslogs/{log_id}').json()
        print(syslog_json)
        return make_response(jsonify(syslog_json), 200)
    if request.method == 'PUT':
        syslog_json =requests.put(f'{setup.DATABASE_URL}/syslogs/{log_id}', data=request.data).json()
        print(syslog_json)
        return make_response(jsonify(syslog_json), 200)
    if request.method == 'DELETE':
        syslog_json =requests.delete(f'{setup.DATABASE_URL}/syslogs/{log_id}').json()
        print(syslog_json)
        return make_response(jsonify(syslog_json), 200)
    return make_response(jsonify({'error': 'invalid HTTP request made to server'}), 400)

#G-COMM Logs Page
@app.route('/gcomm')
def gcomm():
    return render_template('gcomm.html', host_ip=setup.HOST)

# G-COMM Log API
@app.route('/api/v1/gcommlogs',methods=['GET','POST'])
def gcomms_api_mass():
    if request.method == 'GET':
        syslog_json = requests.get(f'{setup.DATABASE_URL}/gcommlogs').json()
        print(syslog_json)
        return make_response(jsonify(syslog_json), 200)
    if request.method == 'POST':
        syslog_json =requests.post(f'{setup.DATABASE_URL}/gcommlogs', data=request.data).json()
        print(syslog_json)
        return make_response(jsonify(syslog_json), 201)
    return make_response(jsonify({'error': 'invalid HTTP request made to server'}), 400)

# G-COMM Log API Single
@app.route('/api/v1/gcommlogs/<log_id>',methods=['GET','PUT', 'DELETE'])
def gcomms_api_single(log_id):
    if request.method == 'GET':
        syslog_json = requests.get(f'{setup.DATABASE_URL}/gcommlogs/{log_id}').json()
        print(syslog_json)
        return make_response(jsonify(syslog_json), 200)
    if request.method == 'PUT':
        syslog_json =requests.put(f'{setup.DATABASE_URL}/gcommlogs/{log_id}', data=request.data).json()
        print(syslog_json)
        return make_response(jsonify(syslog_json), 200)
    if request.method == 'DELETE':
        syslog_json =requests.delete(f'{setup.DATABASE_URL}/gcommlogs/{log_id}').json()
        print(syslog_json)
        return make_response(jsonify(syslog_json), 200)
    return make_response(jsonify({'error': 'invalid HTTP request made to server'}), 400)

#Work Orders Page
@app.route('/work-orders')
def work_orders():
    return render_template('work-orders.html', host_ip=setup.HOST)

# WorkOrders Log API
@app.route('/api/v1/work-orders',methods=['GET','POST'])
def wo_api_mass():
    if request.method == 'GET':
        syslog_json = requests.get(f'{setup.DATABASE_URL}/work-orders').json()
        print(syslog_json)
        return make_response(jsonify(syslog_json), 200)
    if request.method == 'POST':
        syslog_json =requests.post(f'{setup.DATABASE_URL}/work-orders', data=request.data).json()
        print(syslog_json)
        return make_response(jsonify(syslog_json), 201)
    return make_response(jsonify({'error': 'invalid HTTP request made to server'}), 400)

# WorkOrders Log API
@app.route('/api/v1/work-orders/current',methods=['GET','POST'])
def wo_api_mass_current():
    if request.method == 'GET':
        syslog_json = requests.get(f'{setup.DATABASE_URL}/work-orders/current').json()
        print(syslog_json)
        return make_response(jsonify(syslog_json), 200)
    return make_response(jsonify({'error': 'invalid HTTP request made to server'}), 400)

# WorkOrders Claim API
@app.route('/api/v1/work-orders/claim',methods=['POST','PUT'])
def wo_api_claim():
    if request.method == 'POST' or request.method == 'PUT':
        syslog_json = requests.post(f'{setup.DATABASE_URL}/work-orders/claim?id={request.args.get("id")}&tech={request.args.get("tech")}').json()
        print(syslog_json)
        return make_response(jsonify(syslog_json), 200)
    return make_response(jsonify({'error': 'invalid HTTP request made to server'}), 400)

# WorkOrders Complete API
@app.route('/api/v1/work-orders/complete',methods=['POST','PUT'])
def wo_api_complete():
    if request.method == 'POST' or request.method == 'PUT':
        syslog_json = requests.post(f'{setup.DATABASE_URL}/work-orders/complete?id={request.args.get("id")}&tech={request.args.get("tech")}').json()
        print(syslog_json)
        return make_response(jsonify(syslog_json), 200)
    return make_response(jsonify({'error': 'invalid HTTP request made to server'}), 400)

# WorkOrders Pickup API
@app.route('/api/v1/work-orders/pickup',methods=['POST','PUT'])
def wo_api_pickup():
    if request.method == 'POST' or request.method == 'PUT':
        syslog_json = requests.post(f'{setup.DATABASE_URL}/work-orders/pickup?id={request.args.get("id")}&sig={request.args.get("sig")}').json()
        print(syslog_json)
        return make_response(jsonify(syslog_json), 200)
    return make_response(jsonify({'error': 'invalid HTTP request made to server'}), 400)

# WorkOrders Log API Single
@app.route('/api/v1/work-orders/<log_id>',methods=['GET','PUT', 'DELETE'])
def wo_api_single(log_id):
    if request.method == 'GET':
        syslog_json = requests.get(f'{setup.DATABASE_URL}/work-orders/{log_id}').json()
        print(syslog_json)
        return make_response(jsonify(syslog_json), 200)
    if request.method == 'PUT':
        syslog_json =requests.put(f'{setup.DATABASE_URL}/work-orders/{log_id}', data=request.data).json()
        print(syslog_json)
        return make_response(jsonify(syslog_json), 200)
    if request.method == 'DELETE':
        syslog_json =requests.delete(f'{setup.DATABASE_URL}/work-orders/{log_id}').json()
        print(syslog_json)
        return make_response(jsonify(syslog_json), 200)
    return make_response(jsonify({'error': 'invalid HTTP request made to server'}), 400)

#Work Orders Archive Page
@app.route('/work-orders-archive')
def work_orders_archive():
    return render_template('work-orders-archive.html', host_ip=setup.HOST)

# WORK ORDERS ARCHIVE API
@app.route('/api/v1/work-orders/archive', methods=['GET'])
def wo_archive_api():
    if request.method == 'GET':
        wo_json = requests.get(f'{setup.DATABASE_URL}/work-orders/archive')
        print(wo_json)
        return make_response(jsonify(wo_json), 200)

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

# GENERAL PRICES API
@app.route('/api/v1/prices', methods=['GET'])
def prices_api():
    if request.method == 'GET':
        wo_json = requests.get(f'{setup.DATABASE_URL}/prices').json()
        print(wo_json)
        return make_response(jsonify(wo_json), 200)
    return make_response(jsonify({'error': 'invalid HTTP request made to server'}), 400)


#Game Prices Page
@app.route('/game-prices')
def game_prices():
    prices = requests.get('http://localhost:5000/game-prices').json()
    for price in prices:
        price['img_link'] = url_for('static', filename=f'img/img_games/{price["pc_id"]}.jpg')
        pass
    return render_template('game_prices_2.html', host_ip=setup.HOST, p=prices)

#Console Log Prices Page
@app.route('/consolelogs')
def consolelog():
    return render_template('consolelog.html', host_ip=setup.HOST)

#Console GCOMM Prices Page
@app.route('/console-gcomm')
def console_gcomm():
    return render_template('consolegcomm.html', host_ip=setup.HOST)

#Techs and Reports Page
@app.route('/techs')
def techs():
    return render_template('techs.html', host_ip=setup.HOST)

#Report Generation Page
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

    pdf_options = {
        'page-size': 'Letter',
        'margin-top': '0.5in',
        'margin-right': '0.5in',
        'margin-bottom': '0.5in',
        'margin-left': '0.5in',
        'encoding': 'UTF-8'
    }

    if tech_id:
        html_info = requests.get(f'http://{setup.HOST}:5000/techs/reports?start={start}&end={end}&tech_id={tech_id}', headers=request_headers)
        file_name = f'report_{tech_id}_{start}_{end}'
        pdfkit.from_string(str(html_info.content).replace('b\'', '').replace('\'', ''), f'reports/{file_name}.pdf', options=pdf_options)
        # pdfkit.from_url(f'http://{setup.HOST}:5000/techs/reports?start={start}&end={end}&tech_id={tech_id}', f'reports/{file_name}.pdf', options=pdf_options)
        # pdfkit.from_file(f'reports/{file_name}.html', f'reports/{file_name}.pdf', options=pdf_options)
        # pdfkit.from_string(html_string, f'reports/{file_name}.pdf', options=pdf_options)
        return send_file(f'reports/{file_name}.pdf', download_name=f'{file_name}.pdf')
    else:
        # delete all files in the mass directory if any
        for file in os.listdir('reports/mass'):
            os.remove(os.path.join('reports/mass', file))

        # HTML content array
        html_info = []

        # adding main summary content to array
        html_info.append([requests.get(f'http://{setup.HOST}:5000/techs/reports?start={start}&end={end}', headers=request_headers).content, f'reports/mass/report_all_{start}_{end}.pdf'])

        # get the list of techs and get their HTML contents
        tech_list = requests.get(f'http://{setup.HOST}:5000/techs').json()
        for tech in tech_list:
            html_info.append([requests.get(f'http://{setup.HOST}:5000/techs/reports?start={start}&end={end}&tech_id={tech["id"]}', headers=request_headers).content, f'reports/mass/report_{tech["id"]}_{start}_{end}.pdf'])
        
        # create PDF merger
        pdf_merger = PdfFileMerger()

        # generate PDF files for each element in HTML info
        for info in html_info:
            pdfkit.from_string(str(info[0]).replace('b\'', '').replace('\'', ''), info[1], options=pdf_options)
            pdf_merger.append(info[1])

        # create final file
        pdf_merger.write('reports/mass/result.pdf')
        pdf_merger.close()

        # return final file
        return send_file('reports/mass/result.pdf', download_name=f'report_mass_{start}_{end}.pdf')

    

    # html_string = ''
    # with open(f'reports/{file_name}.html', 'w') as file:
    #     file.write(html_info.text)
    # with open(f'reports/{file_name}.html') as file:
    #     html_string = file.read()
    #     print(html_string)

# ADMIN
@app.route('/admin')
def admin():
    return render_template('admin.html')

# ADMIN PAGES
@app.route('/admin/<page>')
def admin_page(page):
    try:
        return render_template(f'admin-{page}.html')
    except:
        return render_template('admin.html')

#RUN APPLICATION
if __name__ == '__main__':
    app.run(debug=setup.DEBUG, port=setup.PORT, host = setup.HOST)