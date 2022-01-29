import random
import json

pricing_info = None

def calc_price(log):
    # reload pricing info from JSON
    file = open('system_pricing.json')
    pricing_info = json.load(file)

    # add pricings to base price
    price = 0
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
    # floor price to typical price
    price -= .01

    #close file and return final price
    if price > 0:
        return price
    return int(random.random()*940)-.01 + 60

def calc_computer_type(log):
    comp_type_prices = pricing_info['computer_type']
    return comp_type_prices[log.computer_type]
    return 

def calc_cpu_brand(log):
    return

def calc_cpu_model(log):
    return

def calc_cpu_gen(log):
    return

def calc_cpu_speed(log):
    return

def calc_ram(log):
    return

def calc_hdd(log):
    return

def calc_disk_drive(log):
    return

def calc_tags(log):
    return
