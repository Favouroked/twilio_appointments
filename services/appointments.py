from bson.objectid import ObjectId
from pymongo import MongoClient

client = MongoClient('mongodb://localhost/')

appointments = client['twilio']['appointments']


def create_appointment(data):
    appointments.insert_one(data)


def get_appointment(appointment_id):
    result = appointments.find_one({'_id': ObjectId(appointment_id)})
    return dict(result) if result else None


def get_appointments(conditions):
    if '_id' in conditions:
        conditions['_id'] = ObjectId(conditions['_id'])
    results = appointments.find(conditions)
    data = []
    for result in results:
        data.append(dict(result))
    return data


def update_appointment(appointment_id, data):
    appointment = appointments.find_one_and_update({'_id': ObjectId(appointment_id)}, {'$set': data},
                                                   return_document=True)
    return appointment


def delete_appointment(appointment_id):
    appointments.find_one_and_delete({'_id': ObjectId(appointment_id)})
