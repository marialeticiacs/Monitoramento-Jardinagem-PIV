from app import db
from datetime import datetime
from bson.objectid import ObjectId

def insert_user_data(telefone, api_key, planta_id, email, senha, nome):
    user_collection = db.users
    user_collection.insert_one({
        "telefone": telefone,
        "api_key": api_key,
        "planta_id": planta_id,
        "email": email,
        "senha": senha,
        "nome": nome,
        "ultimo_alerta": None,
        "data_hora": datetime.now()
    })

def get_user_data():
    user_collection = db.users
    users = user_collection.find()
    return [convert_objectid_to_str(user) for user in users]

def get_user_by_email(email):
    user_collection = db.users
    user = user_collection.find_one({"email": email})
    return convert_objectid_to_str(user) if user else None

def update_user_data(user_id, telefone, api_key):
    user_collection = db.users
    update_fields = {}
    
    if telefone:
        update_fields['telefone'] = telefone
    if api_key:
        update_fields['api_key'] = api_key

    result = user_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": update_fields}
    )
    return result.modified_count > 0

def delete_user_data(user_id):
    user_collection = db.users
    result = user_collection.delete_one({"_id": ObjectId(user_id)})
    return result.deleted_count > 0

def convert_objectid_to_str(user):
    user['_id'] = str(user['_id'])
    return user

def update_ultimo_alerta(planta_id):
    user_collection = db.users
    result = user_collection.update_one(
        {"planta_id": planta_id},
        {"$set": {"ultimo_alerta": datetime.now()}}
    )
    return result.modified_count > 0

def get_user_by_planta_id(planta_id):
    user_collection = db.users
    user = user_collection.find_one({"planta_id": planta_id})
    return user