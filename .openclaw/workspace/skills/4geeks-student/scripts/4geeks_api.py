#!/usr/bin/env python3
"""
4Geeks BreatheCode student API helper (Giacomo skill).

Reads the student token from ~/.4geeks_token (must be mode 0600) and performs
HTTP calls against the BreatheCode API. The token is NEVER printed.

Usage:
  python3 4geeks_api.py GET /v1/admissions/user/me
  python3 4geeks_api.py GET /v1/assignment/user/me/task -q limit=100 -q task_type=PROJECT
  python3 4geeks_api.py GET /v1/assignment/task/996403
  python3 4geeks_api.py PUT /v1/assignment/task/996403 -b '{"github_url": "https://..."}'
  python3 4geeks_api.py POST /v1/assignment/task/996403/deliver
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

BASE_URL = "https://breathecode.herokuapp.com"
TOKEN_FILE = os.path.expanduser("~/.4geeks_token")


def get_token():
    if not os.path.exists(TOKEN_FILE):
        sys.stderr.write(f"ERRORE: file token non trovato: {TOKEN_FILE}\n")
        sys.exit(2)
    mode = os.stat(TOKEN_FILE).st_mode & 0o777
    if mode != 0o600:
        sys.stderr.write(f"ERRORE: permessi del file token ({oct(mode)}) non sicuri; esegui: chmod 600 {TOKEN_FILE}\n")
        sys.exit(2)
    with open(TOKEN_FILE) as f:
        tok = f.read().strip()
    if not tok:
        sys.stderr.write("ERRORE: file token vuoto\n")
        sys.exit(2)
    return tok


def api_call(method, path, query=None, body=None):
    token = get_token()
    url = BASE_URL + path
    if query:
        url += "?" + urllib.parse.urlencode(query)
    data = None
    headers = {"Authorization": f"Token {token}"}
    if body is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = resp.read().decode("utf-8", "replace")
            try:
                return resp.status, json.loads(raw)
            except ValueError:
                return resp.status, raw
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", "replace")
        try:
            return e.code, json.loads(raw)
        except ValueError:
            return e.code, raw


def main():
    ap = argparse.ArgumentParser(description="4Geeks BreatheCode student API (Giacomo)")
    ap.add_argument("method", choices=["GET", "POST", "PUT", "PATCH", "DELETE"])
    ap.add_argument("path", help="percorso API, es. /v1/admissions/user/me")
    ap.add_argument("-q", "--query", action="append", default=[], metavar="k=v", help="parametro query (ripetibile)")
    ap.add_argument("-b", "--body", default=None, metavar="JSON", help="corpo JSON per POST/PUT/PATCH")
    args = ap.parse_args()

    query = {}
    for kv in args.query:
        if "=" in kv:
            k, v = kv.split("=", 1)
            query[k] = v
    body = json.loads(args.body) if args.body else None

    status, data = api_call(args.method, args.path, query, body)
    if isinstance(data, str):
        print(data)
    else:
        print(json.dumps(data, indent=2, ensure_ascii=False))
    sys.exit(0 if 200 <= status < 300 else 1)


if __name__ == "__main__":
    main()
