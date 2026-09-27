# Water temperature

A Flask app that shows station readings. The page loads data from `/api/stations`.

> This repository is a disposable test fixture for [Observed](https://github.com/esau-morais/observed).

## Develop

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python app.py   # http://127.0.0.1:5000 (set PORT to change it)
```

Readings are illustrative.

## API

`POST /api/stations/<id>/readings` with `{"value": 13.4}` adds a reading. It
needs `Authorization: Bearer <token>`; the token is not committed. Developers
have it in the `STATIONS_TOKEN` environment variable, and CI reads the
`STATIONS_TOKEN` Actions secret. `GET /api/stations/<id>` returns one station
with its readings. Readings reset when the app restarts.
