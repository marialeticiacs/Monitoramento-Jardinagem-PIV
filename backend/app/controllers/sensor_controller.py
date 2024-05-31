from flask import request, jsonify
from app.services.whatsapp_service import enviar_mensagem_whatsapp
from app.models.sensor_data import insert_sensor_data
from app.models.user_data import update_ultimo_alerta, get_user_by_planta_id
from app import db
from datetime import datetime, timedelta

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
            if not ultimo_alerta or now - ultimo_alerta > timedelta(hours=6):
                alerta = True
                enviar_mensagem_whatsapp(telefone, api_key, "Sua plantinha está com sede, regue-a o mais rápido possível.")
                update_ultimo_alerta(planta_id)
        elif umidade_solo >= 30:
            if ultimo_alerta and now - ultimo_alerta < timedelta(hours=6):
                rega = True
                enviar_mensagem_whatsapp(telefone, api_key, "Muito obrigado por regar sua plantinha!")
                update_ultimo_alerta(planta_id)

    insert_sensor_data(planta_id, temperatura, umidade_solo, umidade_ar, alerta, rega)
    return jsonify({"status": "success"}), 201
