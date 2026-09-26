import json
import os
from datetime import date

from flask import Flask, jsonify, render_template

app = Flask(__name__)
SETTINGS = json.load(open(os.path.join(os.path.dirname(__file__), "data", "settings.json")))

STATIONS = [
    {"id": "north", "name": "North pier", "readings": [12.1, 12.4, 13.0, 12.8]},
    {"id": "east", "name": "East bank", "readings": [14.2, 14.9, 15.1, 14.7]},
    {"id": "south", "name": "South marsh", "readings": [16.0, 15.8, 16.3, 16.6]},
]


def summary(station):
    readings = station["readings"]
    return {
        "id": station["id"],
        "name": station["name"],
        "latest": readings[-1],
        "average": round(sum(readings) / len(readings), 1),
    }


@app.get("/")
def index():
    return render_template("index.html", today=date(2026, 9, 1).isoformat())


@app.get("/api/stations")
def stations():
    return jsonify({"stations": [summary(station) for station in STATIONS]})


@app.get("/healthz")
def health():
    return {"ok": True}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="127.0.0.1", port=port)
