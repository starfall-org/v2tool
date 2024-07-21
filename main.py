import os
from src.application import app

if __name__ == '__main__':
    app.run(port=os.getenv("PORT", default=5000), host='0.0.0.0')
