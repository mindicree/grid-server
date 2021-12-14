from app import db
from datetime import datetime
import json

class GCommLog (db.Document):
    brand = db.StringField(required=True)
    model = db.StringField(required=True)
    description = db.StringField(required=True)
    computer_type = db.StringField(required=True)
    laptop_screen_condition = db.StringField(required=True)
    laptop_screen_size = db.FloatField(required=True)
    desktop_gpu_type = db.StringField(required=True)
    desktop_display_port = db.StringField(required=True)
    aio_screen_condition = db.StringField(required=True)
    aio_screen_size = db.FloatField(required=True)
    os = db.StringField(required=True)
    hdd = db.StringField(required=True) #incorporate size as well as N/A
    hdd_type = db.StringField(required=True) #HDD, SSD, M.2 SATA, NVME, Embedded
    cpu_brand = db.StringField(required=True)
    cpu_model = db.StringField(required=True)
    cpu_speed = db.FloatField(required=True)
    ram = db.StringField(required=True)
    notes = db.StringField(required=True)
    tech = db.StringField(required=True)
    

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