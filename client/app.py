from flask import Flask, request, render_template, redirect, url_for, send_file, make_response, jsonify
from flask_cors import CORS
import config
import requests
import pdfkit
from PyPDF2 import PdfFileMerger
import os
import json
import subprocess
from datetime import datetime

app = Flask(__name__)
CORS(app)

#config stuff
setup = config.Config()

# TODO add validation functions to all resources
# TODO replace inneficient forEach calls with every calls
# TODO make sure datetimes are local
# TODO autofocus tech input on submission entry
# TODO go to new location instead of refresh
# TODO remove mass console.logs

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
@app.route('/api/v1/prices', methods=['GET', 'POST'])
def prices_api():
    if request.method == 'GET':
        wo_json = requests.get(f'{setup.DATABASE_URL}/prices').json()
        print(wo_json)
        return make_response(jsonify(wo_json), 200)
    if request.method == 'POST':
        wo_json = requests.post(f'{setup.DATABASE_URL}/prices', data=request.data).json()
        print(wo_json)
        return make_response(jsonify(wo_json), 201)
    return make_response(jsonify({'error': 'invalid HTTP request made to server'}), 400)

# GENERAL PRICES API
@app.route('/api/v1/prices/<price_id>', methods=['PUT', 'DELETE'])
def prices_api_single(price_id):
    if request.method == 'PUT':
        try:
            wo_json = requests.put(f'{setup.DATABASE_URL}/prices/{price_id}', data=request.data).json()
            print(wo_json)
            return make_response(jsonify(wo_json), 200)
        except Exception as e:
            return make_response(jsonify({'err_msg': f'{e}'}))
    if request.method == 'DELETE':
        wo_json = requests.delete(f'{setup.DATABASE_URL}/prices/{price_id}', data=request.data).json()
        print(wo_json)
        return make_response(jsonify(wo_json), 200)
    return make_response(jsonify({'error': 'invalid HTTP request made to server'}), 400)


#Game Prices Page
@app.route('/game-prices')
def game_prices():
    prices = requests.get(f'{setup.DATABASE_URL}/game-prices').json()
    for price in prices:
        price['img_link'] = url_for('static', filename=f'img/img_games/{price["pc_id"]}.jpg')
        pass
    return render_template('game_prices_2.html', host_ip=setup.HOST, p=prices)

#Console Log Prices Page
@app.route('/consolelogs')
def consolelog():
    return render_template('consolelog.html', host_ip=setup.HOST)

# CONSOLE Log API
@app.route('/api/v1/consolelogs',methods=['GET','POST'])
def consolelog_api_mass():
    if request.method == 'GET':
        syslog_json = requests.get(f'{setup.DATABASE_URL}/consolelogs').json()
        print(syslog_json)
        return make_response(jsonify(syslog_json), 200)
    if request.method == 'POST':
        syslog_json =requests.post(f'{setup.DATABASE_URL}/consolelogs', data=request.data).json()
        print(syslog_json)
        return make_response(jsonify(syslog_json), 201)
    return make_response(jsonify({'error': 'invalid HTTP request made to server'}), 400)

# CONSOLE Log API Single
@app.route('/api/v1/consolelogs/<log_id>',methods=['GET','PUT', 'DELETE'])
def consolelog_api_single(log_id):
    if request.method == 'GET':
        syslog_json = requests.get(f'{setup.DATABASE_URL}/consolelogs/{log_id}').json()
        print(syslog_json)
        return make_response(jsonify(syslog_json), 200)
    if request.method == 'PUT':
        syslog_json =requests.put(f'{setup.DATABASE_URL}/consolelogs/{log_id}', data=request.data).json()
        print(syslog_json)
        return make_response(jsonify(syslog_json), 200)
    if request.method == 'DELETE':
        syslog_json =requests.delete(f'{setup.DATABASE_URL}/consolelogs/{log_id}').json()
        print(syslog_json)
        return make_response(jsonify(syslog_json), 200)
    return make_response(jsonify({'error': 'invalid HTTP request made to server'}), 400)

#Console GCOMM Prices Page
@app.route('/console-gcomm')
def console_gcomm():
    return render_template('consolegcomm.html', host_ip=setup.HOST)

# G-COMM Log API
@app.route('/api/v1/consolegcomms',methods=['GET','POST'])
def consolegcomms_api_mass():
    if request.method == 'GET':
        syslog_json = requests.get(f'{setup.DATABASE_URL}/consolegcomms').json()
        print(syslog_json)
        return make_response(jsonify(syslog_json), 200)
    if request.method == 'POST':
        syslog_json =requests.post(f'{setup.DATABASE_URL}/consolegcomms', data=request.data).json()
        print(syslog_json)
        return make_response(jsonify(syslog_json), 201)
    return make_response(jsonify({'error': 'invalid HTTP request made to server'}), 400)

# G-COMM Log API Single
@app.route('/api/v1/consolegcomms/<log_id>',methods=['GET','PUT', 'DELETE'])
def consolegcomms_api_single(log_id):
    if request.method == 'GET':
        syslog_json = requests.get(f'{setup.DATABASE_URL}/consolegcomms/{log_id}').json()
        print(syslog_json)
        return make_response(jsonify(syslog_json), 200)
    if request.method == 'PUT':
        syslog_json =requests.put(f'{setup.DATABASE_URL}/consolegcomms/{log_id}', data=request.data).json()
        print(syslog_json)
        return make_response(jsonify(syslog_json), 200)
    if request.method == 'DELETE':
        syslog_json =requests.delete(f'{setup.DATABASE_URL}/consolegcomms/{log_id}').json()
        print(syslog_json)
        return make_response(jsonify(syslog_json), 200)
    return make_response(jsonify({'error': 'invalid HTTP request made to server'}), 400)

#Techs and Reports Page
@app.route('/techs')
def techs():
    return render_template('techs.html', host_ip=setup.HOST)

# TECH API
@app.route('/api/v1/techs', methods=['GET', 'PUT'])
def techs_api():
    if request.method == 'GET':
        techs_json = requests.get(f'{setup.DATABASE_URL}/techs').json()
        print(techs_json)
        return make_response(jsonify(techs_json), 200)
    if request.method == 'PUT':
        techs_json = requests.put(f'{setup.DATABASE_URL}/techs?old={request.args.get("old")}&new={request.args.get("new")}', data=request.data).json()
        print(techs_json)
        return make_response(jsonify(techs_json), 200)
    return make_response(jsonify({'error': 'invalid HTTP request made to server'}), 400)


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
        html_info = requests.get(f'{setup.DATABASE_URL}/techs/reports?start={start}&end={end}&tech_id={tech_id}', headers=request_headers)
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
        html_info.append([requests.get(f'{setup.DATABASE_URL}/techs/reports?start={start}&end={end}', headers=request_headers).content, f'reports/mass/report_all_{start}_{end}.pdf'])

        # get the list of techs and get their HTML contents
        tech_list = requests.get(f'{setup.DATABASE_URL}/techs').json()
        for tech in tech_list:
            html_info.append([requests.get(f'{setup.DATABASE_URL}/techs/reports?start={start}&end={end}&tech_id={tech["id"]}', headers=request_headers).content, f'reports/mass/report_{tech["id"]}_{start}_{end}.pdf'])
        
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


# SYSTEM PRICE
@app.route('/api/v1/system-prices', methods=['GET', 'PUT'])
def system_price_api():
    if request.method == 'GET':
        price_json = requests.get(f'{setup.DATABASE_URL}/system-prices').json()
        return make_response(jsonify(price_json), 200)
    if request.method == 'PUT':
        response_json = requests.put(f'{setup.DATABASE_URL}/system-prices', data= request.data).json()
        return make_response(jsonify({'message': 'price_updated_successful;ly'}), 200)
    return make_response(jsonify({'error': 'incorrect http request made'}))

# LABELS PAGE
@app.route('/labels')
def labels():
    return render_template('labels.html')

# PRINT
# ARGS: type [CHECKLIST, SYSLOG, SYSCOM, CONLOG, CONCOM, GAME, TWOLINE, TRILINE, PARTS, BARCODE, WORKORDER]
# DATA: json
@app.route('/print-testing')
def print_test():
    print_job = subprocess.run(['./print.sh', './labels/checklist.prn'], capture_output=True, text=True)
    print(f'Output: {print_job.stdout}')
    return make_response(jsonify({'message': 'print complete'}), 200)

def print_label(path_to_file):
    try:
        print_job = subprocess.run(['./print.sh', path_to_file], capture_output=True, text=True)
        print(f'Output: {print_job.stdout}')
        return print_job.returncode
    except Exception as e:
        raise e

def print_game_label(path_to_file):
    try:
        print_job = subprocess.run(['./gameprint.sh', path_to_file], capture_output=True, text=True)
        print(f'Output: {print_job.stdout}')
        return print_job.returncode
    except Exception as e:
        raise e

@app.route('/print', methods=['POST'])
def print_job():
    # if type not found, return error
    try:
        print_type = request.args.get("type")
        if print_type == None:
            return make_response(jsonify({'error': 'no print type found'}), 400)
    except KeyError:
        return make_response(jsonify({'error': 'no print type found'}), 400)
    except:
        return make_response(jsonify({'error': 'server could not extract type properly'}), 500)
    
    # try to get print data
    # if none found, return error
    try:
        print_data = json.loads(request.data)
        if print_data == None:
            return make_response(jsonify({'error': 'print data not provided'}))
    except:
        return make_response(jsonify({'error': 'could not load print data from JSON'}), 400)

    # check if goc is set
    try:
        goc_flag = request.args.get('goc')
    except KeyError:
        goc_flag = False
    except Exception as e:
        return make_response(jsonify({'error': 'could not check goc flag for printing'}), 500)

    # check if quantity is set, otherwise, set to 1
    try:
        print_quantity = request.args.get('quantity')
        if print_quantity == None:
            print_quantity = 1
    except:
        print_quantity = 1

    # try to get ZPL code for printing
    zpl_code = ''
    try:
        if print_type == 'WORKORDER':
            # try to pull correct data from JSON
            try:
                wo_name = f'{print_data["fname"]} {print_data["lname"]}'
                date_string = datetime.now().strftime('%Y.%m.%d')
                wo_comp = print_data["model"]
                wo_pwd = print_data["password"]
                wo_phone_1 = print_data["phone1"]
                wo_phone_2 = print_data["phone2"]
                wo_pfu = print_data["isPurchasedFromUs"]
                wo_war = print_data["isUnderWarranty"]
                wo_pwr = print_data["isWithPowerSupply"]
                wo_oth = print_data["other_items"]
                wo_issue = f'{print_data["issue_category"]}: {print_data["issue_description"]}'
            except Exception as e:
                return make_response(jsonify({'error': 'could not obtain correct WO data', 'err_msg': f'{e}'}), 500)

            # try to open file and read string
            try:
                with open('./labels/templates/LABEL_TEMP_WORKORDER.prn', 'r') as template:
                    zpl_code = str(template.read())
            except Exception as e:
                return make_response(jsonify({'error': 'could not read data from WO template file', 'err_msg': f'{e}'}), 500)

            # try to replace string values
            try:
                zpl_code = zpl_code.replace('[[TOP]]', f'WORK ORDER - {wo_name} - {date_string}')
                zpl_code = zpl_code.replace('[[COMPUTER]]', str(wo_comp))
                zpl_code = zpl_code.replace('[[PASSWORD]]', (wo_pwd if len(wo_pwd) > 0 else "N/A"))
                zpl_code = zpl_code.replace('[[PHONE1]]', f'({wo_phone_1[:3]})-{wo_phone_1[3:6]}-{wo_phone_1[6:]}')
                zpl_code = zpl_code.replace('[[ISSUE]]', str(wo_issue))
                zpl_code = zpl_code.replace('[[PFU]]', ("Yes" if wo_pfu else "No"))
                zpl_code = zpl_code.replace('[[WAR]]', ("Yes" if wo_war else "No"))
                zpl_code = zpl_code.replace('[[PWR]]', ("Yes" if wo_pwr else "No"))
                zpl_code = zpl_code.replace('[[OTH]]', (str(wo_oth) if print_data["isWithOtherItems"] == True else "N/A"))
            except Exception as e:
                return make_response(jsonify({'error': 'could not interpolate values into ZPL template', 'err_msg': f'{e}'}), 500)

            # try to write ZPL code to print file
            try:
                with open('./labels/prints/LABEL_PRINT_WORKORDER.prn', 'w') as final:
                    final.write(zpl_code)
            except Exception as e:
                return make_response(jsonify({'error': 'could not write ZPL code to file', 'err_msg': f'{e}'}), 500)

            # try to print label or send back to client as file
            if goc_flag:
                try:
                    status_code = print_game_label('./labels/prints/LABEL_PRINT_WORKORDER.prn')
                    print(f'Print status code: {status_code}')
                    if status_code != 0:
                            return make_response(jsonify({'error': f'status code \'{status_code}\' given while printing {print_type} labels; potential failure to print at GOC location'}), 500)
                    return make_response(jsonify({'message': 'WORKORDER label print successful'}), 200)
                except:
                    return make_response(jsonify({'error': 'could not print at GOC successfully'}), 500)
            else:
                return send_file('./labels/prints/LABEL_PRINT_WORKORDER.prn', download_name=f'WORKORDER-{datetime.now().strftime("%Y%m%d-%H%M%S")}')  
        if print_type == 'CHECKLIST':
            # try to open file and read string
            try:
                with open('./labels/templates/LABEL_TEMP_CHECKLIST.prn', 'r') as template:
                    zpl_code = str(template.read())
            except Exception as e:
                return make_response(jsonify({'error': 'could not read data from CHECKLIST template file', 'err_msg': f'{e}'}), 500)

            # try to replace string values
            try:
                zpl_code = zpl_code.replace('[[QUANTITY]]', str(print_quantity))
            except Exception as e:
                return make_response(jsonify({'error': 'could not interpolate values into ZPL template', 'err_msg': f'{e}'}), 500)

            # try to write ZPL code to print file
            try:
                with open('./labels/prints/LABEL_PRINT_CHECKLIST.prn', 'w') as final:
                    final.write(zpl_code)
            except Exception as e:
                return make_response(jsonify({'error': 'could not write ZPL code to file', 'err_msg': f'{e}'}), 500)

            # try to print label or send back to client as file
            if goc_flag:
                try:
                    status_code = print_label('./labels/prints/LABEL_PRINT_CHECKLIST.prn')
                    print(f'Print status code: {status_code}')
                    if status_code != 0:
                            return make_response(jsonify({'error': f'status code \'{status_code}\' given while printing {print_type} labels; potential failure to print at GOC location'}), 500)
                    return make_response(jsonify({'message': 'CHECKLIST label print successful'}), 200)
                except:
                    return make_response(jsonify({'error': 'could not print at GOC successfully'}), 500)
            else:
                return send_file('./labels/prints/LABEL_PRINT_CHECKLIST.prn', download_name=f'CHECKLIST-{datetime.now().strftime("%Y%m%d-%H%M%S")}')   
        elif print_type == 'SYSLOG':
            try:
                with open('./labels/templates/LABEL_TEMP_SYSLOG.prn', 'r') as template, open('./labels/prints/LABEL_PRINT_SYSLOG.prn', 'w') as final:
                    zpl_code = str(template.read())
                    # try to do a string replace
                    try:
                        # get values and create strings
                        processor_string = f'{print_data["cpu_model"]} {print_data["cpu_gen"]} - {print_data["cpu_speed"]}Ghz'
                        ram_string = f'{print_data["ram"]} of RAM'
                        hdd_string = f'{print_data["hdd"]} {("SSD" if "SSD" in print_data["tags"] else "HDD")}'
                        disc_string = print_data["disk_drive"] if print_data["disk_drive"] != "None" else "."
                        os_string = print_data["os"]
                        tag_string = ''
                        for tag in print_data["tags"]:
                            if tag != "SSD":
                                tag_string = f'{tag_string} {tag}'
                        price_string = f'{print_data["price"]}'
                        date_from_data = datetime.strptime(print_data['dt_initial_irl_log'], '%a, %d %b %Y %H:%M:%S %Z')
                        stock_string = f'{date_from_data.strftime("%y%m%d")}-{print_data["_id"][-6:]}'

                        # replace template placeholders with value strings
                        zpl_code = zpl_code.replace('[[PROCESSOR]]', processor_string).replace('[[RAM]]', ram_string).replace('[[RAM]]', ram_string).replace('[[HDD]]', hdd_string).replace('[[DISK]]', disc_string).replace('[[OS]]', os_string).replace('[[TAGS]]', tag_string).replace('[[PRICE]]', price_string).replace('[[STOCK_ID]]', stock_string).replace('[[QUANTITY]]', str(print_quantity))
                        # return zpl_code
                    except Exception as e:
                        print(e)
                        return make_response(jsonify({'error': 'could not do string replacements properly', 'err_msg': f'{e}'}), 500)

                    # try to write zpl_code string to final print file
                    try:
                        final.write(zpl_code)
                        pass
                    except Exception as e:
                        return make_response(jsonify({'error': 'could not create syslog label file successfully'}), 500)
            except Exception as e:
                return make_response(jsonify({'error': 'could not open file for printing', 'message': f'{e}'}), 500)
        
            # if goc is true, try to print
            if goc_flag:
                try:
                    status_code = print_label('./labels/prints/LABEL_PRINT_SYSLOG.prn')
                    print(f'Print status code: {status_code}')
                    if status_code != 0:
                            return make_response(jsonify({'error': f'status code \'{status_code}\' given while printing {print_type} labels; potential failure to print at GOC location'}), 500)
                    return make_response(jsonify({'message': 'GOC label print successful'}), 200)
                except:
                    return make_response(jsonify({'error': 'could not print at GOC successfully'}), 500)
            else:
                return send_file('./labels/prints/LABEL_PRINT_SYSLOG.prn', download_name=f'{stock_string}')
            # else return file
        elif print_type == 'SYSCOM':
            # try to pull correct data from JSON
            try:
                brand = str(print_data["brand"])
                model = str(print_data["model"])
                condition = str(print_data["condition"])
                computer_type = str(print_data["computer_type"])
                os = str(print_data["os"])
                laptop_screen_condition = str(print_data["laptop_screen_condition"])
                laptop_screen_size = int(print_data["laptop_screen_size"])
                desktop_gpu_type = str(print_data["desktop_gpu_type"])
                desktop_display_ports = print_data["desktop_display_ports"]
                aio_screen_condition = str(print_data["aio_screen_condition"])
                aio_screen_size = int(print_data["aio_screen_size"])
                cpu_brand = str(print_data["cpu_brand"])
                cpu_model = str(print_data["cpu_model"])
                cpu_speed = print_data["cpu_speed"]
                ram = str(print_data["ram"])
                hdd = str(print_data["hdd"])
                hdd_type = str(print_data["hdd_type"])
                notes = str(print_data["notes"])
                tech = str(print_data["tech"])
                dt_initial_irl_log = datetime.strptime(print_data['dt_initial_irl_log'], '%a, %d %b %Y %H:%M:%S %Z')
            except Exception as e:
                return make_response(jsonify({'error': 'could not obtain correct data', 'err_msg': f'{e}'}), 400)
            
            # try to open file and read string
            try:
                with open('./labels/templates/LABEL_TEMP_SYSCOM.prn', 'r') as template:
                    zpl_code = str(template.read())
            except Exception as e:
                return make_response(jsonify({'error': 'could not read data from TWOLINE template file', 'err_msg': f'{e}'}), 500)

            # try to replace string values
            try:
                zpl_code = zpl_code.replace('[[TOP]]', f'{computer_type} - {brand} {model} - {dt_initial_irl_log.strftime("%Y.%m.%d")}')
                zpl_code = zpl_code.replace('[[CONDITION]]', f'{condition}')
                if cpu_speed < 0:
                    cpu_speed_string = ""
                else:
                    cpu_speed_string = f', {cpu_speed}GHz'
                zpl_code = zpl_code.replace('[[PROCESSOR]]', f'{cpu_brand} {cpu_model}{cpu_speed_string}')
                zpl_code = zpl_code.replace('[[RAM]]', f'{ram} RAM')
                zpl_code = zpl_code.replace('[[HDD]]', f'{hdd} {hdd_type}')
                zpl_code = zpl_code.replace('[[NOTES]]', f'{"" if notes == "None" else notes}')
                if computer_type == "Desktop":
                    zpl_code = zpl_code.replace('[[SCREEN_CONDITION_OR_GPU_TYPE]]', f'{desktop_gpu_type} Graphics')
                    port_string = ''
                    for port in desktop_display_ports:
                        port_string = f'{port}, {port_string}'
                    zpl_code = zpl_code.replace('[[SCREEN_SIZE_OR_VIDEO_CONNECTION]]', f'Video Ports: {port_string[:-2]}')
                elif computer_type == "Laptop":
                    zpl_code = zpl_code.replace('[[SCREEN_CONDITION_OR_GPU_TYPE]]', f'Screen: {laptop_screen_condition}')
                    if laptop_screen_size == -11:
                        zpl_code = zpl_code.replace('[[SCREEN_SIZE_OR_VIDEO_CONNECTION]]', 'Screen Size: Less Than 11in')
                    elif laptop_screen_size == -100:
                        zpl_code = zpl_code.replace('[[SCREEN_SIZE_OR_VIDEO_CONNECTION]]', 'Screen Size: Greater Than 18in')
                    else:
                        zpl_code = zpl_code.replace('[[SCREEN_SIZE_OR_VIDEO_CONNECTION]]', f'Screen Size: {laptop_screen_size}in')
                elif computer_type == "All-In-One":
                    zpl_code = zpl_code.replace('[[SCREEN_CONDITION_OR_GPU_TYPE]]', f'Screen: {aio_screen_condition}')
                    if aio_screen_size == -19:
                        zpl_code = zpl_code.replace('[[SCREEN_SIZE_OR_VIDEO_CONNECTION]]', 'Screen Size: Less Than 19in')
                    elif aio_screen_size == -100:
                        zpl_code = zpl_code.replace('[[SCREEN_SIZE_OR_VIDEO_CONNECTION]]', 'Screen Size: Greater Than 34in')
                    else:
                        zpl_code = zpl_code.replace('[[SCREEN_SIZE_OR_VIDEO_CONNECTION]]', f'Screen Size: {aio_screen_size}in')
                zpl_code = zpl_code.replace('[[TECH]]', f'Tech - {tech}')
                if os == 'N/A':
                    os_string = 'No Operating System'
                else:
                    os_string = os
                zpl_code = zpl_code.replace('[[OS]]', os_string)
                zpl_code = zpl_code.replace('[[QUANTITY]]', str(print_quantity))
            except Exception as e:
                print(e)
                return make_response(jsonify({'error': 'could not interpolate values into ZPL template', 'err_msg': f'{e}'}), 500)

            # try to write ZPL code to print file
            try:
                print(zpl_code)
                with open('./labels/prints/LABEL_PRINT_SYSCOM.prn', 'w') as final:
                    final.write(zpl_code)
            except Exception as e:
                return make_response(jsonify({'error': 'could not write ZPL code to file', 'err_msg': f'{e}'}), 500)

            # try to print label or send back to client as file
            if goc_flag:
                try:
                    status_code = print_label('./labels/prints/LABEL_PRINT_SYSCOM.prn')
                    print(f'Print status code: {status_code}')
                    if status_code != 0:
                            return make_response(jsonify({'error': f'status code \'{status_code}\' given while printing {print_type} labels; potential failure to print at GOC location'}), 500)
                    return make_response(jsonify({'message': 'SYSCOM label print successful'}), 200)
                except:
                    return make_response(jsonify({'error': 'could not print at GOC successfully'}), 500)
            else:
                return send_file('./labels/prints/LABEL_PRINT_SYSCOM.prn', download_name=f'SYSCOM-{datetime.now().strftime("%Y%m%d-%H%M%S")}')
            return str(print_type)
        elif print_type == 'CONLOG':
            # try to pull correct data from JSON

            # try to open template file and read string

            # try to replace string with values

            # try to write final ZPL code to print file

            # try to print file or send back as file or ZPL code
            
            return str(print_type)
        elif print_type == 'CONCOM':
            # try to pull correct data from JSON

            # try to open template file and read string

            # try to replace string with values

            # try to write final ZPL code to print file

            # try to print file or send back as file or ZPL code
            
            return str(print_type)
        elif print_type == 'GAME':
            # check if game condition is given
            try:
                game_cond = request.args.get('game_cond')
                if game_cond == None:
                    return make_response(jsonify({'error': 'could not find game_cond for game printing'}), 400)
                game_cond = game_cond.upper()
                if game_cond not in ['LOOSE', 'CIB', 'NEW']:
                    return make_response(jsonify({'error': f'game_cond \'{game_cond}\' is invalid. Options are \'loose, cib, and new\''}), 400)
            except KeyError as ke:
                return make_response(jsonify({'error': 'could not find game_cond for game printing', 'err_msg': f'{ke}'}), 400)
            except Exception as e:
                return make_response(jsonify({'error': 'server could not extract game_cond', 'err_msg': f'{e}'}), 500)
            
            # try to pull correct data from JSON
            try:
                game_name = str(print_data["name"])
                game_system = str(print_data["system"])
                try:
                    game_price = request.args.get('custom_price')
                    if game_price == None:
                        raise Exception
                except:
                    if game_cond == 'LOOSE':
                        game_price = print_data["price_used"]
                    elif game_cond == 'CIB':
                        game_price = print_data["price_cib"]
                    else:
                        game_price = print_data["price_new"]
                date_string = datetime.now().strftime('%Y-%m-%d')
            except Exception as e:
                return make_response(jsonify({'error': 'could not obtain correct GAME data', 'err_msg': f'{e}'}), 500)
            
            # try to open file and read string
            try:
                with open('./labels/templates/LABEL_TEMP_GAME.prn', 'r') as template:
                    zpl_code = str(template.read())
            except Exception as e:
                return make_response(jsonify({'error': 'could not read data from GAME template file', 'err_msg': f'{e}'}), 500)

            # try to replace string values
            try:
                zpl_code = zpl_code.replace('[[GAME_COND]]', f'{game_cond}')
                zpl_code = zpl_code.replace('[[PRICE]]', f'{game_price}')
                # making price barcode
                game_price_string = str(game_price).replace('.', '')
                zero_pad_amount = 7 - len(game_price_string)
                game_price_barcode = ("0"*zero_pad_amount) + game_price_string
                zpl_code = zpl_code.replace('[[BARCODE_PRICE]]', f'{game_price_barcode}')
                # split game name into two rows
                if len(game_name) > 24:
                    game_name_1, game_name_2 = game_name[:24], game_name[24:]
                else:
                    game_name_1, game_name_2 = game_name, ''
                zpl_code = zpl_code.replace('[[TITLE_ROW_1]]', f'{game_name_1}')
                zpl_code = zpl_code.replace('[[TITLE_ROW_2]]', f'{game_name_2}')
                zpl_code = zpl_code.replace('[[TITLE]]', f'{game_name}')
                zpl_code = zpl_code.replace('[[CONSOLE]]', f'{game_system.upper()}')
                zpl_code = zpl_code.replace('[[QUANTITY]]', str(print_quantity))
                # making console barcode
                if game_system in ['Xbox']:
                    zpl_code = zpl_code.replace('[[BARCODE_CONSOLE]]', '0000210')
                if game_system in ['360', 'Xbox-360']:
                    zpl_code = zpl_code.replace('[[BARCODE_CONSOLE]]', '0000211')
                if game_system in ['PS-1', 'PS1']:
                    zpl_code = zpl_code.replace('[[BARCODE_CONSOLE]]', '0000212')
                if game_system in ['PS-2', 'PS2']:
                    zpl_code = zpl_code.replace('[[BARCODE_CONSOLE]]', '0000213')
                if game_system in ['PS-3', 'PS3']:
                    zpl_code = zpl_code.replace('[[BARCODE_CONSOLE]]', '0000214')
                if game_system in ['PSP']:
                    zpl_code = zpl_code.replace('[[BARCODE_CONSOLE]]', '0000215')
                if game_system in ['NES']:
                    zpl_code = zpl_code.replace('[[BARCODE_CONSOLE]]', '0000216')
                if game_system in ['SNES']:
                    zpl_code = zpl_code.replace('[[BARCODE_CONSOLE]]', '0000217')
                if game_system in ['N64']:
                    zpl_code = zpl_code.replace('[[BARCODE_CONSOLE]]', '0000218')
                if game_system in ['Gamecube']:
                    zpl_code = zpl_code.replace('[[BARCODE_CONSOLE]]', '0000219')
                if game_system in ['Wii', 'WiiU']:
                    zpl_code = zpl_code.replace('[[BARCODE_CONSOLE]]', '0000220')
                if game_system in ['Gameboy', 'GB-Advance', 'GBA', 'VirtualBoy']:
                    zpl_code = zpl_code.replace('[[BARCODE_CONSOLE]]', '0000221')
                if game_system in ['DS', '3-DS', '3DS']:
                    zpl_code = zpl_code.replace('[[BARCODE_CONSOLE]]', '0000222')
                if game_system in ['Genesis', 'Master', 'GameGear', '32X', 'SegaCD', 'Dreamcast', 'Saturn']:
                    zpl_code = zpl_code.replace('[[BARCODE_CONSOLE]]', '0000223')
                if game_system in ['PS-4', 'PS4']:
                    zpl_code = zpl_code.replace('[[BARCODE_CONSOLE]]', '0002174')
                if game_system in ['Xbox-One', 'XOne']:
                    zpl_code = zpl_code.replace('[[BARCODE_CONSOLE]]', '0002175')
                if game_system in ['2600', '5200', '7800']:
                    zpl_code = zpl_code.replace('[[BARCODE_CONSOLE]]', '0002176')

                zpl_code = zpl_code.replace('[[DATE]]', f'{date_string}')

            except Exception as e:
                return make_response(jsonify({'error': 'could not interpolate values into ZPL template', 'err_msg': f'{e}'}), 500)

            # try to write ZPL code to print file
            try:
                with open('./labels/prints/LABEL_PRINT_GAME.prn', 'w') as final:
                    final.write(zpl_code)
            except Exception as e:
                return make_response(jsonify({'error': 'could not write ZPL code to file', 'err_msg': f'{e}'}), 500)

            # try to print label or send back to client as file
            if goc_flag:
                try:
                    status_code = print_game_label('./labels/prints/LABEL_PRINT_GAME.prn')
                    print(f'Print status code: {status_code}')
                    if status_code != 0:
                            return make_response(jsonify({'error': f'status code \'{status_code}\' given while printing {print_type} labels; potential failure to print at GOC location'}), 500)
                    return make_response(jsonify({'message': 'GAME label print successful'}), 200)
                except Exception as e:
                    return make_response(jsonify({'error': 'could not print at GOC successfully', 'err_msg': f'{e}'}), 500)
            else:
                return send_file('./labels/prints/LABEL_PRINT_GAME.prn', download_name=f'GAME-{datetime.now().strftime("%Y%m%d-%H%M%S")}')
            return str(print_type)
            return str(print_type)
        elif print_type == 'TWOLINE':
            # try to pull correct data from JSON
            try:
                row1 = str(print_data["row_1"])
                row2 = str(print_data["row_2"])
            except Exception as e:
                return make_response(jsonify({'error': 'could not obtain correct data', 'err_msg': f'{e}'}), 400)
            
            # try to open file and read string
            try:
                with open('./labels/templates/LABEL_TEMP_TWOLINE.prn', 'r') as template:
                    zpl_code = str(template.read())
            except Exception as e:
                return make_response(jsonify({'error': 'could not read data from TWOLINE template file', 'err_msg': f'{e}'}), 500)

            # try to replace string values
            try:
                zpl_code = zpl_code.replace('[[ROW1]]', row1).replace('[[ROW2]]', row2).replace('[[QUANTITY]]', str(print_quantity))
            except Exception as e:
                return make_response(jsonify({'error': 'could not interpolate values into ZPL template', 'err_msg': f'{e}'}), 500)

            # try to write ZPL code to print file
            try:
                with open('./labels/prints/LABEL_PRINT_TWOLINE.prn', 'w') as final:
                    final.write(zpl_code)
            except Exception as e:
                return make_response(jsonify({'error': 'could not write ZPL code to file', 'err_msg': f'{e}'}), 500)

            # try to print label or send back to client as file
            if goc_flag:
                try:
                    status_code = print_label('./labels/prints/LABEL_PRINT_TWOLINE.prn')
                    print(f'Print status code: {status_code}')
                    if status_code != 0:
                            return make_response(jsonify({'error': f'status code \'{status_code}\' given while printing {print_type} labels; potential failure to print at GOC location'}), 500)
                    return make_response(jsonify({'message': 'TWOLINE label print successful'}), 200)
                except:
                    return make_response(jsonify({'error': 'could not print at GOC successfully'}), 500)
            else:
                return send_file('./labels/prints/LABEL_PRINT_TWOLINE.prn', download_name=f'TWOLINE-{datetime.now().strftime("%Y%m%d-%H%M%S")}')
        elif print_type == 'TRILINE':
            # try to pull correct data from JSON
            try:
                row1 = str(print_data["row_1"])
                row2 = str(print_data["row_2"])
                row3 = str(print_data["row_3"])
            except Exception as e:
                return make_response(jsonify({'error': 'could not obtain correct data', 'err_msg': f'{e}'}), 400)
            
            # try to open file and read string
            try:
                with open('./labels/templates/LABEL_TEMP_TRILINE.prn', 'r') as template:
                    zpl_code = str(template.read())
            except Exception as e:
                return make_response(jsonify({'error': 'could not read data from TRILINE template file', 'err_msg': f'{e}'}), 500)

            # try to replace string values
            try:
                zpl_code = zpl_code.replace('[[ROW1]]', row1).replace('[[ROW2]]', row2).replace('[[ROW3]]', row3).replace('[[QUANTITY]]', str(print_quantity))
            except Exception as e:
                return make_response(jsonify({'error': 'could not interpolate values into TRILINE ZPL template', 'err_msg': f'{e}'}), 500)

            # try to write ZPL code to print file
            try:
                with open('./labels/prints/LABEL_PRINT_TRILINE.prn', 'w') as final:
                    final.write(zpl_code)
            except Exception as e:
                return make_response(jsonify({'error': 'could not write ZPL code to TRILINE file', 'err_msg': f'{e}'}), 500)

            # try to print label or send back to client as file
            if goc_flag:
                try:
                    status_code = print_label('./labels/prints/LABEL_PRINT_TRILINE.prn')
                    print(f'Print status code: {status_code}')
                    if status_code != 0:
                            return make_response(jsonify({'error': f'status code \'{status_code}\' given while printing {print_type} labels; potential failure to print at GOC location'}), 500)
                    return make_response(jsonify({'message': 'TRILINE label print successful'}), 200)
                except:
                    return make_response(jsonify({'error': 'could not print at GOC successfully'}), 500)
            else:
                return send_file('./labels/prints/LABEL_PRINT_TRILINE.prn', download_name=f'TRILINE-{datetime.now().strftime("%Y%m%d-%H%M%S")}')
        elif print_type == 'PARTS':
            # try to pull correct data from JSON
            try:
                price = str(print_data["price"])
                date_string = datetime.now().strftime('%Y-%m-%d')
            except Exception as e:
                return make_response(jsonify({'error': 'could not obtain correct data', 'err_msg': f'{e}'}), 400)
            
            # try to open file and read string
            try:
                with open('./labels/templates/LABEL_TEMP_PARTS.prn', 'r') as template:
                    zpl_code = str(template.read())
            except Exception as e:
                return make_response(jsonify({'error': 'could not read data from PARTS template file', 'err_msg': f'{e}'}), 500)

            # try to replace string values
            try:
                zpl_code = zpl_code.replace('[[PRICE]]', f'{price}').replace('[[DATE]]', date_string)
                zpl_code = zpl_code.replace('[[QUANTITY]]', str(print_quantity))
            except Exception as e:
                return make_response(jsonify({'error': 'could not interpolate values into ZPL template', 'err_msg': f'{e}'}), 500)

            # try to write ZPL code to print file
            try:
                with open('./labels/prints/LABEL_PRINT_PARTS.prn', 'w') as final:
                    final.write(zpl_code)
            except Exception as e:
                return make_response(jsonify({'error': 'could not write ZPL code to file', 'err_msg': f'{e}'}), 500)

            # try to print label or send back to client as file
            if goc_flag:
                try:
                    status_code = print_label('./labels/prints/LABEL_PRINT_PARTS.prn')
                    print(f'Print status code: {status_code}')
                    if status_code != 0:
                            return make_response(jsonify({'error': f'status code \'{status_code}\' given while printing {print_type} labels; potential failure to print at GOC location'}), 500)
                    return make_response(jsonify({'message': 'PARTS label print successful'}), 200)
                except:
                    return make_response(jsonify({'error': 'could not print at GOC successfully'}), 500)
            else:
                return send_file('./labels/prints/LABEL_PRINT_TWOLINE.prn', download_name=f'PARTS-{datetime.now().strftime("%Y%m%d-%H%M%S")}')
            return str(print_type)
        elif print_type == 'BARCODE':
            # try to pull correct data from JSON

            # try to open template file and read string

            # try to replace string with values

            # try to write final ZPL code to print file

            # try to print file or send back as file or ZPL code
            
            return str(print_type)
        else:
            return make_response(jsonify({'error': f'invalid print type of {print_type}'}), 400)
    except Exception as e:
        return make_response(jsonify({'error': 'server could not print', 'err_msg': f'{e}'}), 500)

    # if not GOC return ZPL file for client print script
    # else print normally and return success message
    return make_response(jsonify({'message': 'something is wrong with this print function'}), 500)

#RUN APPLICATION
if __name__ == '__main__':
    app.run(debug=setup.DEBUG, port=setup.PORT, host = setup.HOST)