from app import db
from datetime import datetime
import json

class WorkOrder (db.Document):
    fname = db.StringField(required=True)
    lname = db.StringField(required=True)
    phone1 = db.StringField(required=True)
    phone2 = db.StringField()
    computer_type = db.StringField(required=True)
    model = db.StringField(required=True)
    password = db.StringField()
    isPurchasedFromUs = db.BooleanField()
    isUnderWarranty = db.BooleanField()
    isWithPowerSupply = db.BooleanField()
    isWithOtherItems = db.BooleanField()
    other_items = db.StringField()
    issue_category = db.StringField(required=True)
    issue_description = db.StringField()
    cashier = db.StringField(required=True)
    status = db.StringField(default='Dropped Off')
    starting_tech = db.StringField(default='')
    finishing_tech = db.StringField(default='')
    notes = db.StringField(default='')
    dt_recieved = db.DateTimeField()
    dt_last_updated = db.DateTimeField()
    dt_completed = db.DateTimeField()
    dt_picked_up = db.DateTimeField()
    price = db.FloatField()
    signature = db.StringField()

    def get_json(self):
        return {
            "_id": str(self.id),
            "fname": self.fname,
            "lname": self.lname,
            "phone1": self.phone1,
            "phone2": self.phone2,
            "computer_type": self.computer_type,
            "model": self.model,
            "password": self.password,
            "isPurchasedFromUs": self.isPurchasedFromUs,
            "isUnderWarranty": self.isUnderWarranty,
            "isWithPowerSupply": self.isWithPowerSupply,
            "isWithOtherItems": self.isWithOtherItems,
            "other_items": self.other_items,
            "issue_category": self.issue_category,
            "issue_description": self.issue_description,
            "cashier": self.cashier,
            "status": self.status,
            "starting_tech": self.starting_tech,
            "finishing_tech": self.finishing_tech,
            "notes": self.notes, 
            "dt_recieved": self.dt_recieved, 
            "dt_last_updated": self.dt_last_updated, 
            "dt_completed": self.dt_completed, 
            "dt_picked_up": self.dt_picked_up,
            "price": self.price,
            "signature": self.signature
        }

class GCommLog (db.Document):
    brand = db.StringField(required=True)
    model = db.StringField(required=True)
    condition = db.StringField(required=True)
    computer_type = db.StringField(required=True)
    laptop_screen_condition = db.StringField(required=True) 
    laptop_screen_size = db.FloatField(required=True) #provide a list N/A (-1), <11(-11), 11, 13, 14, 15, 17, 18, >18 (-100)
    desktop_gpu_type = db.StringField(required=True) #prompt for name if dedicated
    desktop_display_ports = db.ListField() #VGA, DVI, DMS, DP, HDMI, MINI DP, MINI HDMI, USB-C
    aio_screen_condition = db.StringField(required=True)
    aio_screen_size = db.FloatField(required=True)
    os = db.StringField(required=True)
    cpu_brand = db.StringField(required=True)
    cpu_model = db.StringField(required=True)
    cpu_speed = db.FloatField(required=True)
    hdd = db.StringField(required=True) #incorporate size as well as N/A
    hdd_type = db.StringField(required=True) #N/A HDD, SSD, M.2 SATA, NVME, Embedded
    ram = db.StringField(required=True) #None, <1GB - 32GB
    notes = db.StringField()
    tech = db.StringField(required=True)
    dt_initial_system_log = db.DateTimeField(default = datetime.utcnow())
    dt_initial_irl_log = db.DateTimeField(default = datetime.utcnow())
    dt_last_update = db.DateTimeField(default = datetime.utcnow())

    def get_json(self):
        return {
            "_id": str(self.id),
            "brand": self.brand,
            "model": self.model,
            "condition": self.condition,
            "computer_type": self.computer_type,
            "os": self.os,
            "laptop_screen_condition": self.laptop_screen_condition,
            "laptop_screen_size": self.laptop_screen_size,
            "desktop_gpu_type": self.desktop_gpu_type,
            "desktop_display_ports": self.desktop_display_ports,
            "aio_screen_condition": self.aio_screen_condition,
            "aio_screen_size": self.aio_screen_size,
            "cpu_brand": self.cpu_brand,
            "cpu_model": self.cpu_model,
            "cpu_speed": self.cpu_speed,
            "ram": self.ram,
            "hdd": self.hdd,
            "hdd_type": self.hdd_type,
            "notes": self.notes,
            "tech": self.tech,
            "dt_initial_system_log": self.dt_initial_system_log,
            "dt_initial_irl_log": self.dt_initial_irl_log,
            "dt_last_update": self.dt_last_update
        }
    

class Price(db.Document):
    type_0 = db.StringField()
    type_1 = db.StringField()
    type_2 = db.StringField()
    name = db.StringField()
    price = db.FloatField()
    price_history = db.ListField()
    dt_last_update = db.DateTimeField(default = datetime.utcnow())

    def get_json(self):
        return {
            '_id': str(self.id),
            'name': self.name,
            'type_0': self.type_0,
            'type_1': self.type_1,
            'type_2': self.type_2,
            'price': self.price,
            'dt_last_update': self.dt_last_update,
            'price_history': self.price_history
        }

class SystemLog(db.Document):
    old_coa = db.StringField(default='N/A')
    new_coa = db.StringField(required=True)
    serial_no = db.StringField(required=True)
    brand = db.StringField(required=True)
    model = db.StringField(required=True)
    os = db.StringField(required=True)
    computer_type = db.StringField(required=True)
    source = db.StringField(required=True)
    cpu_brand = db.StringField()
    cpu_model = db.StringField()
    cpu_gen = db.StringField()
    cpu_speed = db.FloatField()
    ram = db.StringField()
    hdd = db.StringField()
    disk_drive = db.StringField()
    tags = db.ListField()
    tech = db.StringField()
    price = db.FloatField()
    dt_initial_system_log = db.DateTimeField(default = datetime.utcnow())
    dt_initial_irl_log = db.DateTimeField(default = datetime.utcnow())
    dt_last_update = db.DateTimeField(default = datetime.utcnow())

    def get_json(self):
        #print('Logging: ' + str(self.dt_initial_system_log))
        return {
            "_id": str(self.id),
            "old_coa": self.old_coa,
            "new_coa": self.new_coa,
            "serial_no": self.serial_no,
            "brand": self.brand,
            "model": self.model,
            "os": self.os,
            "computer_type": self.computer_type,
            "source": self.source,
            "cpu_brand": self.cpu_brand,
            "cpu_gen": self.cpu_gen,
            "cpu_model": self.cpu_model,
            "cpu_speed": self.cpu_speed,
            "ram": self.ram,
            "hdd": self.hdd,
            "disk_drive": self.disk_drive,
            "tags": self.tags,
            "tech": self.tech,
            "price": round(self.price, 2),
            "dt_initial_system_log": self.dt_initial_system_log,
            "dt_initial_irl_log": self.dt_initial_irl_log,
            "dt_last_update": self.dt_last_update
        }