import sys
from gunicorn.app.wsgiapp import run
from multiprocessing import Process
from application.contentdownload import runserver

def run_gunicorn():
    sys.argv = "gunicorn --timeout 1200 --bind 0.0.0.0:3000 application.flask:app".split()
    sys.exit(run())

if __name__ == '__main__':
    gunicorn_process = Process(target=run_gunicorn)
    runserver_process = Process(target=runserver)

    gunicorn_process.start()
    runserver_process.start()

    gunicorn_process.join()
    runserver_process.join()