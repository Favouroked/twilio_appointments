import atexit

from flask import Flask

from controllers.appointments import appointments
from jobs import close_workers, init_workers


def create_app():
    init_workers()
    atexit.register(close_workers)
    return Flask(__name__)


app = create_app()

app.register_blueprint(appointments, url_prefix='/api/appointments')

if __name__ == '__main__':
    app.run()
