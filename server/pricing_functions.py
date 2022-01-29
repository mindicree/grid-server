import random
import json

def calc_price(log):
    # reload pricing info from JSON
    file = open('system_pricing.json')
    global pricing_info
    pricing_info = json.load(file)
    # print('System Pricing info loaded: \n' + str(pricing_info))

    # calculate price
    price = 0
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

    # make the price "typical"
    price = get_typical_price(price)

    #close file and return final price
    file.close()
    if price > 0:
        return price
    return int(random.random()*940) + 60

def calc_brand(log):
    brand_prices = pricing_info['brand']
    try:
        return brand_prices[log.brand]
    except:
        print('Brand \'' + str(log.brand) + '\' is not specialized')
        return 0
def calc_computer_type(log):
    #comp_type_prices = pricing_info['computer_type']
    #return comp_type_prices[log.computer_type]
    comp_prices = pricing_info['computer_type']
    return comp_prices[log.computer_type]

def calc_cpu_brand(log):
    comp_prices = pricing_info['cpu_brand']
    return comp_prices[log.cpu_brand]

def calc_cpu_model(log):
    comp_prices = pricing_info['cpu_model']
    try:
        return comp_prices[log.cpu_model]
    except:
        print('Error: could not find system price for cpu_model \'' + str(log.cpu_model) + '\'')
        return 0

def calc_cpu_gen(log):
    comp_prices = pricing_info['cpu_gen']
    try:
        return comp_prices[log.cpu_gen]
    except:
        print('Error: could not find system price for cpu_gen \'' + str(log.cpu_gen) + '\'')
        return 0

def calc_cpu_speed(log):
    comp_prices = pricing_info['cpu_speed']
    base_speed, base_price, inc_speed, inc_price = comp_prices['base_speed'], comp_prices['base_price'], comp_prices['increment_speed'], comp_prices['increment_price']
    try:
        base_price += ((log.cpu_speed - base_speed)/inc_speed) * inc_price 
        return base_price
    except:
        print('Error: could not find system price for cpu_speed \'' + str(log.cpu_speed) + '\'')
        return 0

def calc_ram(log):
    comp_prices = pricing_info['ram']
    try:
        return comp_prices[log.ram]
    except:
        print('Error: could not find system price for ram \'' + str(log.ram) + '\'')
        return 0

def calc_hdd(log):
    comp_prices = pricing_info['hdd']
    multiplier = 1.0
    tag_list = []
    for t in log.tags:
        if t == 'SSD':
            multiplier = comp_prices['SSD']
    return comp_prices[log.hdd] * multiplier
    return 0

def calc_disk_drive(log):
    comp_prices = pricing_info['disk_drive']
    try:
        return comp_prices[log.disk_drive]
    except:
        print('Error: could not find system price for disk_drive \'' + str(log.disk_drive) + '\'')
        return 0

def calc_tags(log):
    comp_prices = pricing_info['tags']
    base = 0
    try:
        for t in log.tags:
            if '2nd Drive' not in t:
                base += comp_prices[t]
            else:
                size = str(t).replace('2nd Drive - ', '')
                hdd_prices = pricing_info['hdd']
                base += hdd_prices[size] 
        return base
    except:
        print('Error: could not find system price for tags \'' + str(log.tags) + '\'')
        return 0

def get_typical_price(price):
    new_price = round_to_nearest_multiple(price, 5)
    if price % 10 == 0:
        new_price -= 1
    new_price -= .01
    return new_price


def round_to_nearest_multiple(num, mul):
    # credit to kite.com for formula
    # https://www.kite.com/python/answers/how-to-round-to-the-nearest-multiple-of-5-in-python
    return mul * round(num/mul)
