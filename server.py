import sys
from gunicorn.app.wsgiapp import run
if __name__ == '__main__':
    sys.argv = "gunicorn --timeout 1200 --bind 0.0.0.0:3000 main:app".split()
    sys.exit(run())