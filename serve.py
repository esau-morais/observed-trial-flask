import os

from app import app

app.run(host="127.0.0.1", port=int(os.environ["PORT"]))
