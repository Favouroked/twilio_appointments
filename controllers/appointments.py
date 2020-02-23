from flask import Blueprint, request

from services import appointments as apt_service
from utils.request import validate_body, parse_appointment
from utils.response import response, error_response

import jobs

appointments = Blueprint('appointments', __name__)


@appointments.route('/', methods=['POST'])
def create():
    body = request.get_json()
    status, missing_field = validate_body(body, ['title', 'phone', 'description', 'time'])
    if not status:
        return error_response(f'{missing_field} is required')
    status, error = parse_appointment(body)
    if not status:
        return error_response(error)
    try:
        apt_service.create_appointment(body)
        jobs.schedule_appointment(body)
        return response(True, 'Appointment created successfully', body)
    except Exception as err:
        print('=====> Error', err)
        return error_response(str(err))


@appointments.route('/')
def view():
    conditions = dict(request.args)
    try:
        data = apt_service.get_appointments(conditions)
        return response(True, 'Appointments', data)
    except Exception as err:
        print('=====> Error', err)
        return error_response(str(err))


@appointments.route('/<appointment_id>')
def view_one(appointment_id):
    try:
        data = apt_service.get_appointment(appointment_id)
        return response(True, 'Appointment', data)
    except Exception as err:
        print('=====> Error', err)
        return error_response(str(err))


@appointments.route('/<appointment_id>', methods=['PUT'])
def update(appointment_id):
    body = request.get_json()
    try:
        parse_appointment(body)
        appointment = apt_service.update_appointment(appointment_id, body)
        jobs.update_scheduled_appointment(appointment_id, appointment)
        return response(True, 'Updated Appointment', appointment)
    except Exception as err:
        print('=====> Error', err)
        return error_response(str(err))


@appointments.route('/<appointment_id>', methods=['DELETE'])
def delete(appointment_id):
    try:
        apt_service.delete_appointment(appointment_id)
        jobs.delete_scheduled_appointment(appointment_id)
        return response(True, 'Appointment deleted successfully', None)
    except Exception as err:
        print('====> Error', err)
        return error_response(str(err))
