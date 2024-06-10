from flask import request, jsonify
from app.services.whatsapp_service import enviar_mensagem_whatsapp
from app.models.sensor_data import insert_sensor_data
from app.models.user_data import update_ultimo_alerta, get_user_by_planta_id
from app import db
from datetime import datetime, timedelta
from bson.json_util import dumps

def receive_data():
    data = request.json
    planta_id = data.get('planta_id')
    temperatura = data.get('temperatura_ambiente')
    umidade_solo = data.get('umidade_solo')
    umidade_ar = data.get('umidade_ar')
    alerta = True
    rega = True

    user = get_user_by_planta_id(planta_id)

    if user:
        telefone = user.get('telefone')
        api_key = user.get('api_key')
        ultimo_alerta = user.get('ultimo_alerta')

        now = datetime.now()
        if umidade_solo < 30:
            if not ultimo_alerta or now - ultimo_alerta > timedelta(hours=2):
                alerta = True
                rega = False
                enviar_mensagem_whatsapp(telefone, api_key, "Sua plantinha está com sede, regue-a o mais rápido possível.")
                update_ultimo_alerta(planta_id)
        elif umidade_solo >= 30:
            alerta = False
            if ultimo_alerta and now - ultimo_alerta > timedelta(hours=2):
                enviar_mensagem_whatsapp(telefone, api_key, "Muito obrigado por regar sua plantinha!")
                update_ultimo_alerta(planta_id)

    insert_sensor_data(planta_id, temperatura, umidade_solo, umidade_ar, alerta, rega)
    return jsonify({"status": "success"}), 201

def get_latest_sensor_data():
    sensor_data = db.sensor_data.find().sort('data_hora', -1).limit(1)
    try:
        data = next(sensor_data)
        return jsonify({
            'temperatura': data['temperatura_ambiente'],
            'umidade_solo': data['umidade_solo'],
            'alerta': data.get('alerta')  # Adicione a informação sobre o alerta
        }), 200
    except StopIteration:
        return jsonify({'error': 'No data found'}), 404

def get_daily_average(date):
    start = datetime.strptime(date, "%Y-%m-%d")
    end = start + timedelta(days=1)
    average_data = db.sensor_data.aggregate([
        {"$match": {"data_hora": {"$gte": start, "$lt": end}}},
        {"$group": {
            "_id": None,
            "temperatura_ambiente": {"$avg": "$temperatura_ambiente"},
            "umidade_solo": {"$avg": "$umidade_solo"},
            "umidade_ar": {"$avg": "$umidade_ar"}
        }}
    ])
    return jsonify(dumps(average_data))

def get_sensor_data():
    sensor_data = db.sensor_data.find().sort('data_hora', -1)
    data = [{
        'data_hora': entry['data_hora'].isoformat(),
        'temperatura_ambiente': entry['temperatura_ambiente'],
        'umidade_solo': entry['umidade_solo'],
        'umidade_ar': entry['umidade_ar']
    } for entry in sensor_data]
    return jsonify(data)