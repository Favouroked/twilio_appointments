from datetime import datetime


def validate_body(data, required_fields):
    for field in required_fields:
        if field not in data:
            return False, field
    return True, None


def parse_appointment(body):
    try:
        if body.get('time'):
            time_obj = datetime.strptime(body['time'], '%Y-%m-%d %H:%M')
            body['time'] = time_obj
        return True, None
    except Exception as err:
        return False, str(err)
