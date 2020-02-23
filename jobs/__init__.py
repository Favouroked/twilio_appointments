from multiprocessing import Process
from datetime import datetime

from .appointments import start_appointment_job

from services.appointments import get_appointments

WORKERS = {}


def terminate_worker(worker):
    try:
        worker.terminate()
        worker.join()
        worker.close()
    except Exception as err:
        print('====> Error occurred terminating process', err)


def schedule_appointment(appointment):
    appointment_id = str(appointment['_id'])
    worker = Process(target=start_appointment_job, args=(appointment,))
    worker.start()
    WORKERS[appointment_id] = worker


def update_scheduled_appointment(appointment_id, updated_appt):
    worker = WORKERS[appointment_id]
    terminate_worker(worker)
    new_worker = Process(target=start_appointment_job, args=(updated_appt,))
    new_worker.start()
    WORKERS[appointment_id] = new_worker


def delete_scheduled_appointment(appointment_id):
    worker = WORKERS[appointment_id]
    terminate_worker(worker)
    del WORKERS[appointment_id]


def init_workers():
    print('=====> Initializing workers')
    appts = get_appointments({})
    for appt in appts:
        if datetime.now() > appt['time']:
            continue
        schedule_appointment(appt)


def close_workers():
    for appointment_id, worker in WORKERS.items():
        terminate_worker(worker)
