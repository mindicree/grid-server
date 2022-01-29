import json, time
from flask import Flask, request, jsonify, make_response
from flask_mongoengine import MongoEngine
from flask_cors import CORS
from datetime import datetime, timedelta
from models import *
from functions import *
import config

#App Initialization
app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'grid-database',
    'host': 'localhost',
    'port': 27017
}
#Database initialization and conect
db = MongoEngine()
db.init_app(app)
#CORS app setup
CORS(app)

#Config stuff
setup = config.Config()

#TODO change error return to objects with status, title, message
#TODO make above into a function that returns a response
#TODO try except around all searches by ID
#TODO default time does not work; manually enter time on ORM creation

### ROUTES ###
######################################################################
### HOME ROUTE #######################################################
######################################################################
@app.route('/')
def index():
    return "Hello, GRID!"

######################################################################
### SYSTEM LOG ROUTES ################################################
######################################################################
#SYSTEM LOGS
@app.route('/syslogs', methods=['POST', 'GET'])
def syslogs():
    if request.method == 'GET':
        logs = SystemLog.objects()
        log_data = []
        for log in logs:
            log_data.append(log.get_json())
        response = make_response(jsonify(log_data), 200)
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

    if request.method == 'POST':
        try:
            data = json.loads(request.data)
            log = SystemLog(old_coa=data['old_coa'], new_coa=data['new_coa'], serial_no=data['serial_no'], brand=data['brand'], model=data['model'], os=data['os'], computer_type=data['computer_type'], source=data['source'], cpu_brand=data['cpu_brand'], cpu_model=data['cpu_model'], cpu_gen=data['cpu_gen'], cpu_speed=data['cpu_speed'], ram=data['ram'], hdd = data['hdd'], disk_drive=data['disk_drive'], tags=data['tags'], tech=data['tech'])
            log.price = calc_price(log)
            log.save()
            response = make_response(jsonify(log.get_json()), 201)
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response
        except ValueError:
            return make_response(jsonify({'error': 'Failed to decode JSON properly'}), 400)

    return make_response(jsonify({'error': 'Bad request'}), 400)

#SYSTEM LOG MASS LOAD (FOR TESTING ONLY)
@app.route('/syslogs/mass-data-entry/1', methods=['POST'])
def syslogs_mass():
    if request.method == 'POST':
        try:
            data = json.loads(request.data)
            for l in data:
                log = SystemLog(old_coa=l['old_coa'], new_coa=l['new_coa'], serial_no=l['serial_no'], brand=l['brand'], model=l['model'], os=l['os'], computer_type=l['computer_type'], source=l['source'], cpu_brand=l['cpu_brand'], cpu_model=l['cpu_model'], cpu_gen=l['cpu_gen'], cpu_speed=l['cpu_speed'], ram=l['ram'], hdd = l['hdd'], disk_drive=l['disk_drive'], tags=l['tags'], tech=l['tech'])
                log.price = calc_price(log)
                log.save()
            return make_response(jsonify(log.get_json()), 201)
        except ValueError:
            return make_response(jsonify({'error': 'Failed to decode JSON properly'}), 400)

    return make_response(jsonify({'error': 'Bad request'}), 400)

#SYSTEM LOG BY ID
@app.route('/syslogs/<log_id>', methods=['GET', 'PUT', 'DELETE'])
def syslog(log_id):
    if request.method == 'GET':
        log = SystemLog.objects(id=log_id).first()
        if not log:
            return make_response(jsonify({'error': 'System log with ID [' + log_id + '] not found.'}), 404)
        response = make_response(jsonify(log.get_json()), 200)
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response


    if request.method == 'PUT':
        log = SystemLog.objects(id=log_id).first()
        if not log:
            reponse = make_response(jsonify({'error': 'System log with ID [' + log_id + '] not found.'}), 404)
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response
        data = json.loads(request.data)
        if not data:
            response = make_response(jsonify({'error': 'Bad request - no data recieved'}), 400)
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response
        try:
            log.update(old_coa=data['old_coa'], new_coa=data['new_coa'], serial_no=data['serial_no'], brand=data['brand'], model=data['model'], os=data['os'], computer_type=data['computer_type'], source=data['source'], cpu_brand=data['cpu_brand'], cpu_model=data['cpu_model'], cpu_gen=data['cpu_gen'], cpu_speed=data['cpu_speed'], ram=data['ram'], hdd = data['hdd'], disk_drive=data['disk_drive'], tags=data['tags'], tech=data['tech'], price=data['price'], dt_initial_irl_log=datetime.strptime(data['dt_initial_irl_log'], '%a, %d %b %Y %H:%M:%S %Z'), dt_last_update=datetime.utcnow())
        except:
            log.update(old_coa=data['old_coa'], new_coa=data['new_coa'], serial_no=data['serial_no'], brand=data['brand'], model=data['model'], os=data['os'], computer_type=data['computer_type'], source=data['source'], cpu_brand=data['cpu_brand'], cpu_model=data['cpu_model'], cpu_gen=data['cpu_gen'], cpu_speed=data['cpu_speed'], ram=data['ram'], hdd = data['hdd'], disk_drive=data['disk_drive'], tags=data['tags'], tech=data['tech'], price=data['price'], dt_last_update=datetime.utcnow())
        response = make_response(jsonify({'message': 'System log ['+str(log_id)+'] updated successfully'}), 200)
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

    if request.method == 'DELETE':
        log = SystemLog.objects(id=log_id).first()
        if not log:
            return make_response(jsonify({'message': 'System log not found'}), 404)
        log.delete()
        return make_response(jsonify({'message': 'System log [' + str(log_id) + '] deleted successfully'}), 200)

#SYSTEM LOG PRICE CALCULATOR
@app.route('/syslogs/price/<log_id>', methods=['GET'])
def syslog_price(log_id):
    try:
        log = SystemLog.objects(id=log_id).first()
        if not log:
            return make_response(jsonify({'error': 'System log with id ['+str(log_id)+'] not found'}), 404)
        price = calc_price(log)
        return make_response(jsonify({'price': price}), 200)
    #TODO change to ValidationError somehow
    except: 
        return make_response(jsonify({'error': 'Bad ID request'}), 400)

#TODO setup advanced search for syslogs
#SYSTEM LOG SEARCH BY SERIAL
@app.route('/syslogs/serial/<comp>', methods=['GET'])
def syslog_serial(comp):
    if request.method == 'GET':
        log = SystemLog.objects(serial_no = comp).first()
        if not log:
            return make_response(jsonify({'error': 'System with serial number ['+str(comp)+'] not found'}), 404)
        return make_response(jsonify(log.get_json()), 200)

    return make_response(jsonify({'error': 'Bad request'}), 400)

#SYSTEM LOG SEARCH BY BRAND
@app.route('/syslogs/brand/<comp>', methods=['GET'])
def syslog_brand(comp):
    if request.method == 'GET':
        logs = SystemLog.objects(brand = comp)
        if not logs:
            return make_response(jsonify({'error': 'System(s) with brand name['+str(comp)+'] not found. Please check spelling'}), 404)
        log_data = []
        for log in logs:
            log_data.append(log.get_json())

        return make_response(jsonify(log_data), 200)

    return make_response(jsonify({'error': 'Bad request'}), 400)

#SYSTEM LOG SEARCH BY OS
@app.route('/syslogs/os/<comp>', methods=['GET'])
def syslog_os(comp):
    if request.method == 'GET':
        logs = SystemLog.objects(os = comp)
        if not logs:
            return make_response(jsonify({'error': 'System(s) with OS ['+str(comp)+'] not found. Please check spelling.'}), 404)
        log_data = []
        for log in logs:
            log_data.append(log.get_json())
        return make_response(jsonify(log_data), 200)

    return make_response(jsonify({'error': 'Bad request'}), 400)

#SYSTEM LOG SEARCH BY COMPUTER TYPE
@app.route('/syslogs/comp-type/<comp>', methods=['GET'])
def syslog_comp_type(comp):
    if request.method == 'GET':
        logs = SystemLog.objects(computer_type = comp)
        if not logs:
            return make_response(jsonify({'error': 'System(s) with type ['+str(comp)+'] not found. Please check spelling.'}), 404)
        log_data = []
        for log in logs:
            log_data.append(log.get_json())
        return make_response(jsonify(log_data), 200)

    return make_response(jsonify({'error': 'Bad request'}), 400)

#SYSTEM LOG SEARCH BY SOURCE
@app.route('/syslogs/source/<comp>', methods=['GET'])
def syslog_source(comp):
    if request.method == 'GET':
        logs = SystemLog.objects(source = comp)
        if not logs:
            return make_response(jsonify({'error': 'System(s) with source ['+str(comp)+'] not found. Please check spelling.'}), 404)
        log_data = []
        for log in logs:
            log_data.append(log.get_json())
        return make_response(jsonify(log_data), 200)

    return make_response(jsonify({'error': 'Bad request'}), 400)

#SYSTEM LOG SEARCH BY CPU-BRAND
@app.route('/syslogs/cpu-brand/<comp>', methods=['GET'])
def syslog_cpu_brand(comp):
    if request.method == 'GET':
        logs = SystemLog.objects(cpu_brand = comp)
        if not logs:
            return make_response(jsonify({'error': 'System(s) with CPU Brand ['+str(comp)+'] not found. Please check spelling.'}), 404)
        log_data = []
        for log in logs:
            log_data.append(log.get_json())
        return make_response(jsonify(log_data), 200)

    return make_response(jsonify({'error': 'Bad request'}), 400)

#SYSTEM LOG SEARCH BY CPU-SPEED
@app.route('/syslogs/cpu-speed/<comp>', methods=['GET'])
def syslog_cpu_speed(comp):
    if request.method == 'GET':
        try:
            logs = SystemLog.objects(cpu_speed = comp)
            if not logs:
                return make_response(jsonify({'error': 'System(s) with CPU Speed ['+str(comp)+'] not found.'}), 404)
            log_data = []
            for log in logs:
                log_data.append(log.get_json())
            return make_response(jsonify(log_data), 200)
        except ValueError:
            return make_response(jsonify({'error': 'Invalid argument for CPU Speed. Recieved value: ['+str(comp)+']. Make sure number is recieved.'}), 400)
        
    return make_response(jsonify({'error': 'Bad request'}), 400)

#SYSTEM LOG SEARCH BY RAM
@app.route('/syslogs/ram/<comp>', methods=['GET'])
def syslog_ram(comp):
    if request.method == 'GET':
        logs = SystemLog.objects(ram = comp)
        if not logs:
            return make_response(jsonify({'error': 'System(s) with RAM ['+str(comp)+'] not found. Please check spelling.'}), 404)
        log_data = []
        for log in logs:
            log_data.append(log.get_json())
        return make_response(jsonify(log_data), 200)

    return make_response(jsonify({'error': 'Bad request'}), 400)

#SYSTEM LOG SEARCH BY HDD
@app.route('/syslogs/hdd/<comp>', methods=['GET'])
def syslog_hdd(comp):
    if request.method == 'GET':
        logs = SystemLog.objects(hdd = comp)
        if not logs:
            return make_response(jsonify({'error': 'System(s) with HDD size ['+str(comp)+'] not found. Please check spelling.'}), 404)
        log_data = []
        for log in logs:
            log_data.append(log.get_json())
        return make_response(jsonify(log_data), 200)

    return make_response(jsonify({'error': 'Bad request'}), 400)

#SYSTEM LOG SEARCH BY DISC DRIVE
@app.route('/syslogs/disk-drive/<comp>', methods=['GET'])
def syslog_disk_drive(comp):
    if request.method == 'GET':
        logs = SystemLog.objects(disk_drive = comp)
        if not logs:
            return make_response(jsonify({'error': 'System(s) with Disk Drive ['+str(comp)+'] not found. Please check spelling.'}), 404)
        log_data = []
        for log in logs:
            log_data.append(log.get_json())
        return make_response(jsonify(log_data), 200)

    return make_response(jsonify({'error': 'Bad request'}), 400)

#SYSTEM LOG SEARCH BY TAGS
@app.route('/syslogs/tags', methods=['GET'])
def syslog_tags():
    if request.method == 'GET':
        data = json.loads(request.data)
        
        #TLDR, IF A GIVEN LOG HAS ALL TAGS LISTED IN REQUEST, ADD TO VALID LIST
        valid_query_list = []
        for log in SystemLog.objects():
            tags = log.tags
            valid_log = True
            for t in data:
                if t not in tags:
                    valid_log = False
                    break
            if valid_log:
                valid_query_list.append(log.get_json())
        
        if len(valid_query_list) <= 0:
            return make_response(jsonify({'error': 'System(s) with tags ['+str(data)+'] not found.'}), 404)
        return make_response(jsonify(valid_query_list), 200)

    return make_response(jsonify({'error': 'Bad request'}), 400)

#SYSTEM LOG SEARCH BY TECH
@app.route('/syslogs/tech/<comp>', methods=['GET'])
def syslog_tech(comp):
    if request.method == 'GET':
        logs = SystemLog.objects(tech = comp)
        if not logs:
            return make_response(jsonify({'error': 'System(s) with Tech Initials ['+str(comp)+'] not found. Please check spelling.'}), 404)
        log_data = []
        for log in logs:
            log_data.append(log.get_json())
        return make_response(jsonify(log_data), 200)

    return make_response(jsonify({'error': 'Bad request'}), 400)

#SYSTEM LOG SEARCH BY Date (YYYY-MM-DD)
@app.route('/syslogs/date/<date>', methods=['GET'])
def syslog_date(date):
    if request.method == 'GET':
        try:
            log_date = datetime.strptime(date, '%Y-%m-%d')
            log_date_2 = log_date + timedelta(1)
            #date2 = SystemLog.objects().first().dt_last_update.date()
            #return make_response(jsonify({'date': log_date, 'date2': log_date_2}))
        except ValueError:
            return make_response(jsonify({'error': 'Invalid date provided.'}), 400)
        except:
            return make_response(jsonify({'error': 'Cannot convert date. Please check formart is in YYYY-MM-DD.'}), 400)

    raw_date_query = {'dt_initial_irl_log': {'$gte': log_date, '$lte': log_date_2}}
    logs = SystemLog.objects(__raw__=raw_date_query)
    
    if not logs:
        return make_response(jsonify({'error': 'No system logs found on date ['+str(log_date)+'].'}), 404)
    log_data = []
    for log in logs:
        log_data.append(log.get_json())
    return make_response(jsonify(log_data), 200)    

    return make_response(jsonify({'error': 'Bad request'}), 400)

#SYSTEM LOG SEARCH BY Date Range(YYYY-MM-DD)
@app.route('/syslogs/date/<date_one>/<date_two>', methods=['GET'])
def syslog_date_range(date_one, date_two):
    if request.method == 'GET':
        try:
            log_date = datetime.strptime(date_one, '%Y-%m-%d')
            log_date_2 = datetime.strptime(date_two, '%Y-%m-%d') + timedelta(1)
            #date2 = SystemLog.objects().first().dt_last_update.date()
            #return make_response(jsonify({'date': log_date, 'date2': log_date_2}))
            if (log_date >= log_date_2):
                return make_response(jsonify({'error': 'Invalid date range'}), 400)
        
        except ValueError:
            return make_response(jsonify({'error': 'Invalid date provided.'}), 400)
        except:
            return make_response(jsonify({'error': 'Cannot convert date. Please check formart is in YYYY-MM-DD.'}), 400)

    raw_date_query = {'dt_initial_irl_log': {'$gte': log_date, '$lte': log_date_2}}
    logs = SystemLog.objects(__raw__=raw_date_query)
    
    if not logs:
        return make_response(jsonify({'error': 'No system logs found between ['+str(log_date)+'] and [' + str(log_date_2) + '].'}), 404)
    log_data = []
    for log in logs:
        log_data.append(log.get_json())
    return make_response(jsonify(log_data), 200)    

    return make_response(jsonify({'error': 'Bad request'}), 400)

#SYSTEM LOG SEARCH BY Date Before(YYYY-MM-DD)
@app.route('/syslogs/date-before/<date_one>', methods=['GET'])
def syslog_date_before(date_one):
    if request.method == 'GET':
        try:
            log_date = datetime.strptime(date_one, '%Y-%m-%d')
            #log_date_2 = datetime.strptime(date_two, '%Y-%m-%d') + timedelta(1)
            #date2 = SystemLog.objects().first().dt_last_update.date()
            #return make_response(jsonify({'date': log_date, 'date2': log_date_2}))
        
        except ValueError:
            return make_response(jsonify({'error': 'Invalid date provided.'}), 400)
        except:
            return make_response(jsonify({'error': 'Cannot convert date. Please check formart is in YYYY-MM-DD.'}), 400)

    raw_date_query = {'dt_initial_irl_log': {'$lt': log_date}}
    logs = SystemLog.objects(__raw__=raw_date_query)
    
    if not logs:
        return make_response(jsonify({'error': 'No system logs found before ['+str(log_date)+'].'}), 404)
    log_data = []
    for log in logs:
        log_data.append(log.get_json())
    return make_response(jsonify(log_data), 200)    

    return make_response(jsonify({'error': 'Bad request'}), 400)

#SYSTEM LOG SEARCH BY Date Before Including(YYYY-MM-DD)
@app.route('/syslogs/date-before-inc/<date_one>', methods=['GET'])
def syslog_date_before_inc(date_one):
    if request.method == 'GET':
        try:
            log_date = datetime.strptime(date_one, '%Y-%m-%d')+timedelta(1)
            #log_date_2 = datetime.strptime(date_two, '%Y-%m-%d') + timedelta(1)
            #date2 = SystemLog.objects().first().dt_last_update.date()
            #return make_response(jsonify({'date': log_date, 'date2': log_date_2}))
        
        except ValueError:
            return make_response(jsonify({'error': 'Invalid date provided.'}), 400)
        except:
            return make_response(jsonify({'error': 'Cannot convert date. Please check formart is in YYYY-MM-DD.'}), 400)

    raw_date_query = {'dt_initial_irl_log': {'$lt': log_date}}
    logs = SystemLog.objects(__raw__=raw_date_query)
    
    if not logs:
        return make_response(jsonify({'error': 'No system logs found before or including ['+str(log_date)+'].'}), 404)
    log_data = []
    for log in logs:
        log_data.append(log.get_json())
    return make_response(jsonify(log_data), 200)    

    return make_response(jsonify({'error': 'Bad request'}), 400)

#SYSTEM LOG SEARCH BY Date After(YYYY-MM-DD)
@app.route('/syslogs/date-after/<date_one>', methods=['GET'])
def syslog_date_after(date_one):
    if request.method == 'GET':
        try:
            log_date = datetime.strptime(date_one, '%Y-%m-%d') + timedelta(1)
            #log_date_2 = datetime.strptime(date_two, '%Y-%m-%d') + timedelta(1)
            #date2 = SystemLog.objects().first().dt_last_update.date()
            #return make_response(jsonify({'date': log_date, 'date2': log_date_2}))
        
        except ValueError:
            return make_response(jsonify({'error': 'Invalid date provided.'}), 400)
        except:
            return make_response(jsonify({'error': 'Cannot convert date. Please check formart is in YYYY-MM-DD.'}), 400)

    raw_date_query = {'dt_initial_irl_log': {'$gt': log_date}}
    logs = SystemLog.objects(__raw__=raw_date_query)
    
    if not logs:
        return make_response(jsonify({'error': 'No system logs found before ['+str(log_date)+'].'}), 404)
    log_data = []
    for log in logs:
        log_data.append(log.get_json())
    return make_response(jsonify(log_data), 200)    

    return make_response(jsonify({'error': 'Bad request'}), 400)

#SYSTEM LOG SEARCH BY Date After Including(YYYY-MM-DD)
@app.route('/syslogs/date-after-inc/<date_one>', methods=['GET'])
def syslog_date_after_inc(date_one):
    if request.method == 'GET':
        try:
            log_date = datetime.strptime(date_one, '%Y-%m-%d')
            #log_date_2 = datetime.strptime(date_two, '%Y-%m-%d') + timedelta(1)
            #date2 = SystemLog.objects().first().dt_last_update.date()
            #return make_response(jsonify({'date': log_date, 'date2': log_date_2}))
        
        except ValueError:
            return make_response(jsonify({'error': 'Invalid date provided.'}), 400)
        except:
            return make_response(jsonify({'error': 'Cannot convert date. Please check formart is in YYYY-MM-DD.'}), 400)

    raw_date_query = {'dt_initial_irl_log': {'$gt': log_date}}
    logs = SystemLog.objects(__raw__=raw_date_query)
    
    if not logs:
        return make_response(jsonify({'error': 'No system logs found before or including ['+str(log_date)+'].'}), 404)
    log_data = []
    for log in logs:
        log_data.append(log.get_json())
    return make_response(jsonify(log_data), 200)    

    return make_response(jsonify({'error': 'Bad request'}), 400)

######################################################################
### GCommLOG ROUTES ##################################################
######################################################################
@app.route('/gcommlogs', methods=['POST', 'GET'])
def gcommlogs():
    if request.method == 'GET':
        logs = GCommLog.objects()
        log_data = []
        for log in logs:
            log_data.append(log.get_json())
        response = make_response(jsonify(log_data), 200)
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

    if request.method == 'POST':
        try:
            data = json.loads(request.data)
            log = GCommLog(brand=data['brand'], model=data['model'], condition=data['condition'], os=data['os'], computer_type=data['computer_type'], laptop_screen_condition=data['laptop_screen_condition'], laptop_screen_size=data['laptop_screen_size'], desktop_gpu_type=data['desktop_gpu_type'], desktop_display_ports=data['desktop_display_ports'], aio_screen_condition=data['aio_screen_condition'], aio_screen_size=data['aio_screen_size'], cpu_brand=data['cpu_brand'], cpu_model=data['cpu_model'], cpu_speed=data['cpu_speed'], ram=data['ram'], hdd = data['hdd'], hdd_type = data['hdd_type'], tech=data['tech'])
            log.save()
            response = make_response(jsonify(log.get_json()), 201)
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response
        except ValueError:
            return make_response(jsonify({'error': 'Failed to decode JSON properly'}), 400)

    return make_response(jsonify({'error': 'Bad request'}), 400)

#SYSTEM LOG BY ID
@app.route('/gcommlogs/<log_id>', methods=['GET', 'PUT', 'DELETE'])
def gcommlog(log_id):
    if request.method == 'GET':
        log = GCommLog.objects(id=log_id).first()
        if not log:
            return make_response(jsonify({'error': 'GCOMM log with ID [' + log_id + '] not found.'}), 404)
        response = make_response(jsonify(log.get_json()), 200)
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response


    if request.method == 'PUT':
        log = GCommLog.objects(id=log_id).first()
        if not log:
            response = make_response(jsonify({'error': 'GCOMM log with ID [' + log_id + '] not found.'}), 404)
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response
        data = json.loads(request.data)
        if not data:
            response = make_response(jsonify({'error': 'Bad request - no data recieved'}), 400)
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response
        try:
            log.update(brand=data['brand'], model=data['model'], condition=data['condition'], os=data['os'], computer_type=data['computer_type'], laptop_screen_condition=data['laptop_screen_condition'], laptop_screen_size=data['laptop_screen_size'], desktop_gpu_type=data['desktop_gpu_type'], desktop_display_ports=data['desktop_display_ports'], aio_screen_condition=data['aio_screen_condition'], aio_screen_size=data['aio_screen_size'], cpu_brand=data['cpu_brand'], cpu_model=data['cpu_model'], cpu_speed=data['cpu_speed'], ram=data['ram'], hdd = data['hdd'], hdd_type = data['hdd_type'], tech=data['tech'], dt_initial_irl_log=datetime.strptime(data['dt_initial_irl_log'], '%a, %d %b %Y %H:%M:%S %Z'), dt_last_update = datetime.utcnow())
        except:
            log.update(brand=data['brand'], model=data['model'], condition=data['condition'], os=data['os'], computer_type=data['computer_type'], laptop_screen_condition=data['laptop_screen_condition'], laptop_screen_size=data['laptop_screen_size'], desktop_gpu_type=data['desktop_gpu_type'], desktop_display_ports=data['desktop_display_ports'], aio_screen_condition=data['aio_screen_condition'], aio_screen_size=data['aio_screen_size'], cpu_brand=data['cpu_brand'], cpu_model=data['cpu_model'], cpu_speed=data['cpu_speed'], ram=data['ram'], hdd = data['hdd'], hdd_type = data['hdd_type'], tech=data['tech'], dt_last_update = datetime.utcnow())
        response = make_response(jsonify({'message': 'GCOMM log ['+str(log_id)+'] updated successfully'}), 200)
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

    if request.method == 'DELETE':
        log = GCommLog.objects(id=log_id).first()
        if not log:
            return make_response(jsonify({'message': 'GCOMM log not found'}), 404)
        log.delete()
        return make_response(jsonify({'message': 'GCOMM log [' + str(log_id) + '] deleted successfully'}), 200)

######################################################################
### ITEM/PRICING ROUTES ##############################################
######################################################################
#FULL PRICE LIST
@app.route('/prices', methods=['POST', 'GET'])
def prices():
    if request.method == 'GET':
        price = Price.objects()
        price_data = []
        for p in price:
            price_data.append(p.get_json())
        return make_response(jsonify(price_data), 200)

    if request.method == 'POST':
        try:
            data = json.loads(request.data)
            current_list = Price.objects(type_0__icontains=data['type_0'], type_1__icontains=data['type_1'], name__icontains=data['name'])
            if len(current_list) > 0:
                return make_response(jsonify({'error': str(data['type_0']).title() + ' with name [' + data['name'] + '] already exists.'}), 409)
            price = Price(type_0=data['type_0'], type_1=data['type_1'], type_2=data['type_2'], name=data['name'], price=data['price'])
            price.price_history.append({
                'price': price.price,
                'date': datetime.utcnow()
            })
            price.save()
            return make_response(jsonify(price.get_json()), 201)
        except ValueError:
            return make_response(jsonify({'error': 'Failed to decode JSON properly'}), 400)

    return make_response(jsonify({'error': 'Bad request'}), 400)

#PRICE BY ID
@app.route('/prices/<price_id>', methods=['GET', 'PUT', 'DELETE'])
def prices_by_id(price_id):
    if request.method == 'GET':
        price = Price.objects(id=price_id).first()
        if not price:
            return make_response(jsonify({'error': 'Price information with ID [' + price_id + '] not found.'}), 404)
        return make_response(jsonify(price.get_json()), 200);

    if request.method == 'PUT':
        price = Price.objects(id=price_id).first()
        if not price:
            return make_response(jsonify({'error': 'Price information with ID [' + price_id + '] not found.'}), 404)
        data = json.loads(request.data)
        if not data:
            return make_response(jsonify({'error': 'Bad request - no data recieved'}), 400)
        history = price.price_history
        #print('History before:\n' + str(history))
        history.append({'price': data['price'],'date': datetime.utcnow()})
        #print('History after:\n' + str(history))
        price.update(type_0=data['type_0'], type_1=data['type_1'], type_2=data['type_2'], name=data['name'], price=data['price'], dt_last_update = datetime.utcnow(), price_history = history)
        #print('History stored:\n' + str(price.price_history))
        return make_response(jsonify({'message': 'System log ['+str(price_id)+'] updated successfully'}), 200)

    if request.method == 'DELETE':
        price = Price.objects(id=price_id).first()
        if not price:
            return make_response(jsonify({'error': 'Price information with ID [' + price_id + '] not found.'}), 404)
        price_name = price.name
        price.delete()
        return make_response(jsonify({'message': 'Price information for [' + str(price_name) + '] deleted successfully'}), 200)

#PRICE BY NAME CONTAINS
@app.route('/prices/name/<comp>', methods=['GET'])
def prices_name(comp):
    if request.method == 'GET':
        prices = Price.objects(name__icontains = comp)
        if not prices:
            return make_response(jsonify({'error': 'Price information for ['+str(comp).title()+'] not found. Please check spelling.'}), 404)
        price_data = []
        for price in prices:
            price_data.append(price.get_json())
        return make_response(jsonify(price_data), 200)

    return make_response(jsonify({'error': 'Bad request'}), 400)

#PRICE BY TYPE 0  CONTAINS
@app.route('/prices/type-0/<comp>', methods=['GET'])
def prices_type_0(comp):
    if request.method == 'GET':
        prices = Price.objects(type_0__icontains = comp)
        if not prices:
            return make_response(jsonify({'error': 'Price information for ['+str(comp).title()+'] not found. Please check spelling.'}), 404)
        price_data = []
        for price in prices:
            price_data.append(price.get_json())
        return make_response(jsonify(price_data), 200)

    return make_response(jsonify({'error': 'Bad request'}), 400)

#PRICE BY TYPE 1 CONTAINS
#TODO add similar endpoint but return error for it when igven only one (expected 2 arguments)
@app.route('/prices/type-1/<comp>/<comp1>', methods=['GET'])
def prices_type_1(comp, comp1):
    if request.method == 'GET':
        prices = Price.objects(type_0__icontains = comp, type_1__icontains=comp1)
        if not prices:
            return make_response(jsonify({'error': 'Price information for ['+str(comp).title() + ', ' + str(comp1).title()+'] not found. Please check spelling.'}), 404)
        price_data = []
        for price in prices:
            price_data.append(price.get_json())
        return make_response(jsonify(price_data), 200)

    return make_response(jsonify({'error': 'Bad request'}), 400)

#PRICE BY TYPE 2 CONTAINS
#TODO add similar endpoint but return error for it when igven only one (expected 2 arguments)
#TODO format price error in responses
@app.route('/prices/type-2/<comp>/<comp1>/<comp2>', methods=['GET'])
def prices_type_2(comp, comp1, comp2):
    if request.method == 'GET':
        prices = Price.objects(type_0__icontains = comp, type_1__icontains=comp1, type_2__icontains=comp2)
        if not prices:
            return make_response(jsonify({'error': 'Price information for ['+str(comp).title() + ', ' + str(comp1).title() + ', ' + str(comp2).title()+'] not found. Please check spelling.'}), 404)
        price_data = []
        for price in prices:
            price_data.append(price.get_json())
        return make_response(jsonify(price_data), 200)

    return make_response(jsonify({'error': 'Bad request'}), 400)

#PRICE BY PRICE LT
@app.route('/prices/lt/<comp>', methods=['GET'])
def prices_lt(comp):
    if request.method == 'GET':
        prices = Price.objects(price__lt = comp)
        if not prices:
            return make_response(jsonify({'error': 'Price information for items less than $'+str(comp).title()+' not found.'}), 404)
        price_data = []
        for price in prices:
            price_data.append(price.get_json())
        return make_response(jsonify(price_data), 200)

    return make_response(jsonify({'error': 'Bad request'}), 400)

#PRICE BY PRICE LTE
@app.route('/prices/lte/<comp>', methods=['GET'])
def prices_lte(comp):
    if request.method == 'GET':
        prices = Price.objects(price__lte = comp)
        if not prices:
            return make_response(jsonify({'error': 'Price information for items less than or equal to $'+str(comp).title()+' not found.'}), 404)
        price_data = []
        for price in prices:
            price_data.append(price.get_json())
        return make_response(jsonify(price_data), 200)

    return make_response(jsonify({'error': 'Bad request'}), 400)

#PRICE BY PRICE GT
@app.route('/prices/gt/<comp>', methods=['GET'])
def prices_gt(comp):
    if request.method == 'GET':
        prices = Price.objects(price__gt = comp)
        if not prices:
            return make_response(jsonify({'error': 'Price information for items greater than $'+str(comp).title()+' not found.'}), 404)
        price_data = []
        for price in prices:
            price_data.append(price.get_json())
        return make_response(jsonify(price_data), 200)

    return make_response(jsonify({'error': 'Bad request'}), 400)

#PRICE BY PRICE GTE
@app.route('/prices/gte/<comp>', methods=['GET'])
def prices_gte(comp):
    if request.method == 'GET':
        prices = Price.objects(price__gte = comp)
        if not prices:
            return make_response(jsonify({'error': 'Price information for items greater than or equal to $'+str(comp).title()+' not found.'}), 404)
        price_data = []
        for price in prices:
            price_data.append(price.get_json())
        return make_response(jsonify(price_data), 200)

    return make_response(jsonify({'error': 'Bad request'}), 400)

#PRICE BY PRICE RANGE
@app.route('/prices/price/<comp>/<comp2>', methods=['GET'])
def prices_price_range(comp, comp2):
    if request.method == 'GET':
        if comp2 <= comp:
            return make_response(jsonify({'error': 'Invalid price range provided'}), 400)
        range_0, range_1 = float("{:.2f}".format(float(comp))), float("{:.2f}".format(float(comp2)))
        raw_query = {'price': {'$gte': range_0, '$lte': range_1}}
        prices = Price.objects(__raw__=raw_query)
        if not prices:
            return make_response(jsonify({'error': 'Price information for items in range $'+str(range_0)+' to $' + str(range_1) + ' not found.'}), 404)
        price_data = []
        for price in prices:
            price_data.append(price.get_json())
        return make_response(jsonify(price_data), 200)

    return make_response(jsonify({'error': 'Bad request'}), 400)

#PRICE SEARCH BY Date (YYYY-MM-DD)
@app.route('/prices/date/<date>', methods=['GET'])
def prices_date(date):
    if request.method == 'GET':
        try:
            log_date = datetime.strptime(date, '%Y-%m-%d')
            log_date_2 = log_date + timedelta(1)
            #date2 = SystemLog.objects().first().dt_last_update.date()
            #return make_response(jsonify({'date': log_date, 'date2': log_date_2}))
        except ValueError:
            return make_response(jsonify({'error': 'Invalid date provided.'}), 400)
        except:
            return make_response(jsonify({'error': 'Cannot convert date. Please check formart is in YYYY-MM-DD.'}), 400)

    raw_date_query = {'dt_last_update': {'$gte': log_date, '$lte': log_date_2}}
    logs = Price.objects(__raw__=raw_date_query)
    
    if not logs:
        return make_response(jsonify({'error': 'No price updates found on date ['+str(log_date)+'].'}), 404)
    log_data = []
    for log in logs:
        log_data.append(log.get_json())
    return make_response(jsonify(log_data), 200)    

    return make_response(jsonify({'error': 'Bad request'}), 400)

#PRICE LOG SEARCH BY Date Range(YYYY-MM-DD)
@app.route('/prices/date/<date_one>/<date_two>', methods=['GET'])
def prices_date_range(date_one, date_two):
    if request.method == 'GET':
        try:
            log_date = datetime.strptime(date_one, '%Y-%m-%d')
            log_date_2 = datetime.strptime(date_two, '%Y-%m-%d') + timedelta(1)
            #date2 = SystemLog.objects().first().dt_last_update.date()
            #return make_response(jsonify({'date': log_date, 'date2': log_date_2}))
            if (log_date >= log_date_2):
                return make_response(jsonify({'error': 'Invalid date range'}), 400)
        
        except ValueError:
            return make_response(jsonify({'error': 'Invalid date provided.'}), 400)
        except:
            return make_response(jsonify({'error': 'Cannot convert date. Please check formart is in YYYY-MM-DD.'}), 400)

    raw_date_query = {'dt_last_update': {'$gte': log_date, '$lte': log_date_2}}
    logs = Price.objects(__raw__=raw_date_query)
    
    if not logs:
        return make_response(jsonify({'error': 'No price updates found between ['+str(log_date)+'] and [' + str(log_date_2) + '].'}), 404)
    log_data = []
    for log in logs:
        log_data.append(log.get_json())
    return make_response(jsonify(log_data), 200)    

    return make_response(jsonify({'error': 'Bad request'}), 400)

#SYSTEM LOG SEARCH BY Date Before(YYYY-MM-DD)
@app.route('/prices/date-before/<date_one>', methods=['GET'])
def prices_date_before(date_one):
    if request.method == 'GET':
        try:
            log_date = datetime.strptime(date_one, '%Y-%m-%d')
            #log_date_2 = datetime.strptime(date_two, '%Y-%m-%d') + timedelta(1)
            #date2 = SystemLog.objects().first().dt_last_update.date()
            #return make_response(jsonify({'date': log_date, 'date2': log_date_2}))
        
        except ValueError:
            return make_response(jsonify({'error': 'Invalid date provided.'}), 400)
        except:
            return make_response(jsonify({'error': 'Cannot convert date. Please check formart is in YYYY-MM-DD.'}), 400)

    raw_date_query = {'dt_last_update': {'$lt': log_date}}
    logs = Price.objects(__raw__=raw_date_query)
    
    if not logs:
        return make_response(jsonify({'error': 'No price updates found before ['+str(log_date)+'].'}), 404)
    log_data = []
    for log in logs:
        log_data.append(log.get_json())
    return make_response(jsonify(log_data), 200)    

    return make_response(jsonify({'error': 'Bad request'}), 400)

#SYSTEM LOG SEARCH BY Date Before Including(YYYY-MM-DD)
@app.route('/prices/date-before-inc/<date_one>', methods=['GET'])
def prices_date_before_inc(date_one):
    if request.method == 'GET':
        try:
            log_date = datetime.strptime(date_one, '%Y-%m-%d')+timedelta(1)
            #log_date_2 = datetime.strptime(date_two, '%Y-%m-%d') + timedelta(1)
            #date2 = SystemLog.objects().first().dt_last_update.date()
            #return make_response(jsonify({'date': log_date, 'date2': log_date_2}))
        
        except ValueError:
            return make_response(jsonify({'error': 'Invalid date provided.'}), 400)
        except:
            return make_response(jsonify({'error': 'Cannot convert date. Please check formart is in YYYY-MM-DD.'}), 400)

    raw_date_query = {'dt_last_update': {'$lt': log_date}}
    logs = Price.objects(__raw__=raw_date_query)
    
    if not logs:
        return make_response(jsonify({'error': 'No price updates found before or including ['+str(log_date)+'].'}), 404)
    log_data = []
    for log in logs:
        log_data.append(log.get_json())
    return make_response(jsonify(log_data), 200)    

    return make_response(jsonify({'error': 'Bad request'}), 400)

#SYSTEM LOG SEARCH BY Date After(YYYY-MM-DD)
@app.route('/prices/date-after/<date_one>', methods=['GET'])
def prices_date_after(date_one):
    if request.method == 'GET':
        try:
            log_date = datetime.strptime(date_one, '%Y-%m-%d') + timedelta(1)
            #log_date_2 = datetime.strptime(date_two, '%Y-%m-%d') + timedelta(1)
            #date2 = SystemLog.objects().first().dt_last_update.date()
            #return make_response(jsonify({'date': log_date, 'date2': log_date_2}))
        
        except ValueError:
            return make_response(jsonify({'error': 'Invalid date provided.'}), 400)
        except:
            return make_response(jsonify({'error': 'Cannot convert date. Please check formart is in YYYY-MM-DD.'}), 400)

    raw_date_query = {'dt_last_update': {'$gt': log_date}}
    logs = Price.objects(__raw__=raw_date_query)
    
    if not logs:
        return make_response(jsonify({'error': 'No price updates found before ['+str(log_date)+'].'}), 404)
    log_data = []
    for log in logs:
        log_data.append(log.get_json())
    return make_response(jsonify(log_data), 200)    

    return make_response(jsonify({'error': 'Bad request'}), 400)

#SYSTEM LOG SEARCH BY Date After Including(YYYY-MM-DD)
@app.route('/prices/date-after-inc/<date_one>', methods=['GET'])
def prices_date_after_inc(date_one):
    if request.method == 'GET':
        try:
            log_date = datetime.strptime(date_one, '%Y-%m-%d')
            #log_date_2 = datetime.strptime(date_two, '%Y-%m-%d') + timedelta(1)
            #date2 = SystemLog.objects().first().dt_last_update.date()
            #return make_response(jsonify({'date': log_date, 'date2': log_date_2}))
        
        except ValueError:
            return make_response(jsonify({'error': 'Invalid date provided.'}), 400)
        except:
            return make_response(jsonify({'error': 'Cannot convert date. Please check formart is in YYYY-MM-DD.'}), 400)

    raw_date_query = {'dt_last_update': {'$gt': log_date}}
    logs = Price.objects(__raw__=raw_date_query)
    
    if not logs:
        return make_response(jsonify({'error': 'No price updates found before or including ['+str(log_date)+'].'}), 404)
    log_data = []
    for log in logs:
        log_data.append(log.get_json())
    return make_response(jsonify(log_data), 200)    

    return make_response(jsonify({'error': 'Bad request'}), 400)

######################################################################
### WORK ORDERS ROUTES ###############################################
######################################################################
@app.route('/work-orders', methods=['POST', 'GET'])
def work_orders():
    if request.method == 'GET':
        logs = WorkOrder.objects()
        log_data = []
        for log in logs:
            log_data.append(log.get_json())
        response = make_response(jsonify(log_data), 200)
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

    if request.method == 'POST':
        try:
            data = json.loads(request.data)
            log = WorkOrder(fname=data['fname'], lname=data['lname'], phone1=data['phone1'], phone2=data['phone2'], computer_type=data['computer_type'], model=data['model'], password=data['password'], isPurchasedFromUs=data['isPurchasedFromUs'], isUnderWarranty=data['isUnderWarranty'], isWithPowerSupply=data['isWithPowerSupply'], isWithOtherItems=data['isWithOtherItems'], other_items=data['other_items'], issue_category=data['issue_category'], issue_description=data['issue_description'], cashier=data['cashier'], dt_recieved=datetime.utcnow(), dt_last_updated=datetime.utcnow())
            print(log.dt_recieved)
            log.save()
            response = make_response(jsonify(log.get_json()), 201)
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response
        except ValueError:
            return make_response(jsonify({'error': 'Failed to decode JSON properly'}), 400)

    return make_response(jsonify({'error': 'Bad request'}), 400)

@app.route('/work-orders/current', methods=['GET'])
def work_orders_current():
    if request.method == 'GET':
        logs = WorkOrder.objects()
        log_data = []
        for log in logs:
            if (log.status != 'Picked Up' and log.status != 'Donated'):
                log_data.append(log.get_json())
        response = make_response(jsonify(log_data), 200)
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

    return make_response(jsonify({'error': 'Bad request'}), 400)

@app.route('/work-orders/archive', methods=['GET'])
def work_orders_archive():
    if request.method == 'GET':
        logs = WorkOrder.objects()
        log_data = []
        for log in logs:
            if (log.status == 'Picked Up' or log.status == 'Donated'):
                log_data.append(log.get_json())
        response = make_response(jsonify(log_data), 200)
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

    return make_response(jsonify({'error': 'Bad request'}), 400)

#SYSTEM LOG BY ID
@app.route('/work-orders/<log_id>', methods=['GET', 'PUT', 'DELETE'])
def work_order(log_id):
    if request.method == 'GET':
        try:
            log = WorkOrder.objects(id=log_id).first()
        except:
            return make_response(jsonify({'error': 'Invalid ID provided. Please check URI'}), 404)
        if not log:
            return make_response(jsonify({'error': 'Work Order with ID [' + log_id + '] not found.'}), 404)
        response = make_response(jsonify(log.get_json()), 200)
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response


    if request.method == 'PUT':
        try:
            log = WorkOrder.objects(id=log_id).first()
        except:
            return make_response(jsonify({'error': 'Invalid ID provided. Please check URI'}), 404)
        if not log:
            response = make_response(jsonify({'error': 'GCOMM log with ID [' + log_id + '] not found.'}), 404)
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response
        data = json.loads(request.data)
        if not data:
            response = make_response(jsonify({'error': 'Bad request - no data recieved'}), 400)
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response

        log.update(fname=data['fname'], lname=data['lname'], phone1=data['phone1'], phone2=data['phone2'], computer_type=data['computer_type'], model=data['model'], password=data['password'], isPurchasedFromUs=data['isPurchasedFromUs'], isUnderWarranty=data['isUnderWarranty'], isWithPowerSupply=data['isWithPowerSupply'], issue_category=data['issue_category'], issue_description=data['issue_description'], cashier=data['cashier'], status=data['status'], starting_tech=data['starting_tech'], finishing_tech=data['finishing_tech'], notes=data['notes'], price=data['price'], dt_last_updated=datetime.utcnow())
        #status list
        #Dropped Off, In Progress, Awaiting Part, Completed, Picked Up, Donated
        if data['status'] == 'Completed' or data['status'] == 'Donated':
            log.update(dt_completed=datetime.utcnow())
            if len(data['finishing_tech']) < 1 or not data['finishing_tech']:
                log.update(finishing_tech = log.starting_tech)
        if data['status'] == 'Picked Up':
            log.update(dt_picked_up=datetime.utcnow())
            if not log.dt_completed:
                log.update(dt_completed=datetime.utcnow())
            if len(data['finishing_tech']) < 1 or not data['finishing_tech']:
                log.update(finishing_tech = log.starting_tech)
        response = make_response(jsonify({'message': 'Work Order ['+str(log_id)+'] updated successfully'}), 200)
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

    if request.method == 'DELETE':
        try:
            log = WorkOrder.objects(id=log_id).first()
        except:
            return make_response(jsonify({'error': 'Invalid ID provided. Please check URI'}), 404)
        if not log:
            return make_response(jsonify({'message': 'Work Order not found'}), 404)
        log.delete()
        return make_response(jsonify({'message': 'Work Order [' + str(log_id) + '] deleted successfully'}), 200)


@app.route('/work-orders/claim', methods=['POST', 'PUT'])
def work_orders_claim():
    if request.method == 'POST' or request.method == 'PUT':
        # check if argument provided
        if not request.args.get('id') or not request.args.get('tech'):
                return make_response(jsonify({'error': 'Bad request - missing arguments'}), 400)

        # check id if available
        log = WorkOrder.objects(id=request.args.get('id')).first()
        if not log:
            return make_response(jsonify({'message': 'Work Order not found'}), 404)

        # update work order to in progress
        log.update(status='In Progress', starting_tech=request.args.get('tech'), dt_last_updated=datetime.utcnow())

        return make_response(jsonify({'message': 'Work Order [' + str(log.id) + '] claimed by ' + request.args.get('tech')}), 200)

    return make_response(jsonify({'error': 'Bad request'}), 400)

@app.route('/work-orders/complete', methods=['POST', 'PUT'])
def work_orders_complete():
    if request.method == 'POST' or request.method == 'PUT':
        # check if argument provided
        if not request.args.get('id') or not request.args.get('tech'):
                return make_response(jsonify({'error': 'Bad request - missing arguments'}), 400)

        # check id if available
        log = WorkOrder.objects(id=request.args.get('id')).first()
        if not log:
            return make_response(jsonify({'message': 'Work Order not found'}), 404)

        # update work order to in progress
        log.update(status='Completed', finishing_tech=request.args.get('tech'), dt_last_updated=datetime.utcnow(), dt_completed=datetime.utcnow())

        return make_response(jsonify({'message': 'Work Order [' + str(log.id) + '] completed by ' + request.args.get('tech')}), 200)

    return make_response(jsonify({'error': 'Bad request'}), 400)

@app.route('/work-orders/pickup', methods=['POST', 'PUT'])
def work_orders_pickup():
    if request.method == 'POST' or request.method == 'PUT':
        # check if argument provided
        if not request.args.get('id') or not request.args.get('sig'):
                return make_response(jsonify({'error': 'Bad request - missing arguments'}), 400)

        # check id if available
        log = WorkOrder.objects(id=request.args.get('id')).first()
        if not log:
            return make_response(jsonify({'message': 'Work Order not found'}), 404)

        # update work order to in progress
        log.update(status='Picked Up', dt_last_updated=datetime.utcnow(), dt_picked_up=datetime.utcnow(), signature=request.args.get('sig'))

        return make_response(jsonify({'message': 'Work Order [' + str(log.id) + '] picked up and archived.'}), 200)

    return make_response(jsonify({'error': 'Bad request'}), 400)
#RUN APPLICATION
if __name__ == '__main__':
    app.run(debug=setup.DEBUG, port=setup.PORT, host = setup.HOST)