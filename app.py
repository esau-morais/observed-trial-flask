import hashlib
import hmac
import os
from datetime import date

from flask import Flask, abort, jsonify, render_template, request

app = Flask(__name__)

STATIONS = [
    {"id": "north", "name": "North pier", "readings": [12.1, 12.4, 13.0, 12.8]},
    {"id": "east", "name": "East bank", "readings": [14.2, 14.9, 15.1, 14.7]},
    {"id": "south", "name": "South marsh", "readings": [16.0, 15.8, 16.3, 16.6]},
]

# SHA-256 of the disposable station token. Developers have the token in the
# STATIONS_TOKEN environment variable; CI reads the STATIONS_TOKEN secret.
TOKEN_SHA256 = "072457b0accf01721a17b1388a792852755ce769b627f4b5ee98831b3c596084"


def summary(station):
    readings = station["readings"]
    return {
        "id": station["id"],
        "name": station["name"],
        "latest": readings[-1],
    }


def find(station_id):
    station = next((item for item in STATIONS if item["id"] == station_id), None)
    if station is None:
        abort(404)
    return station


def authorized():
    header = request.headers.get("Authorization", "")
    if not header.startswith("Bearer "):
        return False
    digest = hashlib.sha256(header.removeprefix("Bearer ").encode()).hexdigest()
    return hmac.compare_digest(digest, TOKEN_SHA256)


@app.get("/")
def index():
    return render_template("index.html", today=date(2026, 9, 1).isoformat())


@app.get("/api/stations")
def stations():
    return jsonify({"stations": [summary(station) for station in STATIONS]})


@app.get("/api/stations/<station_id>")
def station(station_id):
    item = find(station_id)
    return jsonify({**summary(item), "readings": item["readings"]})


@app.post("/api/stations/<station_id>/readings")
def add_reading(station_id):
    if not authorized():
        return jsonify({"error": "unauthorized"}), 401
    item = find(station_id)
    value = (request.get_json(silent=True) or {}).get("value")
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        return jsonify({"error": "value must be a number"}), 400
    item["readings"].append(float(value))
    return jsonify({"station": summary(item)})


@app.get("/healthz")
def health():
    return {"ok": True}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="127.0.0.1", port=port)
