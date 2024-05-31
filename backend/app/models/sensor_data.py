from app import db
from datetime import datetime

def insert_sensor_data(planta_id, temperatura, umidade_solo, umidade_ar, alerta, rega):
    sensor_collection = db.sensor_data
    sensor_collection.insert_one({
        "planta_id": planta_id,
        "temperatura_ambiente": temperatura,
        "umidade_solo": umidade_solo,
        "umidade_ar": umidade_ar,
        "alerta": alerta,
        "rega": rega,
        "data_hora": datetime.now()
    })
