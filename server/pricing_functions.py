import random
import json

pricing_info = None

def calc_price(log):
    # reload pricing info from JSON
    file = open('system_pricing.json')
    pricing_info = json.load(file)
    console.log('System Pricing info loaded: \n' + str(pricing_info))

    # calculate price
    price = 0
    try:
        price += calc_brand(log)
        price += calc_computer_type(log)
        price += calc_cpu_brand(log)
        price += calc_cpu_model(log)
        price += calc_cpu_gen(log)
        price += calc_cpu_speed(log)
        price += calc_ram(log)
        price += calc_hdd(log)
        price += calc_disk_drive(log)
        price += calc_tags(log)
        price += calc_computer_type(log)
        price += calc_computer_type(log)
    except:
        console.log('Error in price calculation function')
    # make the price "typical"
    price = round_to_nearest_multiple(price) - 0.01

    #close file and return final price
    file.close()
    if price > 0:
        return price
    return int(random.random()*940)-.01 + 60

def calc_brand(log):
    return 0
def calc_computer_type(log):
    #comp_type_prices = pricing_info['computer_type']
    #return comp_type_prices[log.computer_type]
    return 0 

def calc_os(log):
    return 0

def calc_cpu_brand(log):
    return 0

def calc_cpu_model(log):
    return 0

def calc_cpu_gen(log):
    return 0

def calc_cpu_speed(log):
    return 0

def calc_ram(log):
    return 0

def calc_hdd(log):
    return 0

def calc_disk_drive(log):
    return 0

def calc_tags(log):
    return 0

def round_to_nearest_multiple(num, mul):
    # credit to kite.com for formula
    # https://www.kite.com/python/answers/how-to-round-to-the-nearest-multiple-of-5-in-python
    return mul * round(num/base)
