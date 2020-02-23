import time
from datetime import datetime

from utils.whatsapp import send_message


def start_appointment_job(appointment):
    print(f"=====> Scheduled Appointment {appointment['_id']} for :> {appointment['time']}")
    if datetime.now() > appointment['time']:
        return
    diff = appointment['time'] - datetime.now()
    time.sleep(diff.seconds)
    send_message(appointment)
