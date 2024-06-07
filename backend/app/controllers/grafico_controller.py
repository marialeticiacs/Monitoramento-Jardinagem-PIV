from flask import request, jsonify
from app.services.whatsapp_service import enviar_mensagem_whatsapp
from app.models.sensor_data import insert_sensor_data
from app.models.user_data import update_ultimo_alerta, get_user_by_planta_id
from app import db
from datetime import datetime, timedelta

def get_temperature_data():
    sensor_data = db['sensor_data'].find({}, {'_id': 0, 'data_hora': 1, 'temperatura_ambiente': 1})
    data = list(sensor_data)
    return jsonify(data)

def get_soil_moisture_data():
    sensor_data = db['sensor_data'].find({}, {'_id': 0, 'data_hora': 1, 'umidade_solo': 1})
    data = list(sensor_data)
    return jsonify(data)

def get_air_humidity_data():
    sensor_data = db['sensor_data'].find({}, {'_id': 0, 'data_hora': 1, 'umidade_ar': 1})
    data = list(sensor_data)
    return jsonify(data)
