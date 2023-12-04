import sys
from uvicorn.main import run
from main_fastapi import app

if __name__ == '__main__':
    sys.argv = ["uvicorn", "main_fastapi:app", "--host", "0.0.0.0", "--port", "3000", "--timeout", "1200"]
    sys.exit(run(app))