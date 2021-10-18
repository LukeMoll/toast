import re
from flask import Flask, request

from .config import config, get_slice
from .github import validate_payload

app = Flask(__name__)

@app.post('/hook/github/')
def hook_github():
    body = request.get_json()
    if body is None:
        return "Body types other than JSON not supported", 415

    origin_repo = body["repository"]["full_name"]
    slice_cfg = get_slice(origin_repo)
    if slice_cfg is None:
        return "No repository found matching the payload", 404

    if "secret" in slice_cfg:
        if "X-Hub-Signature-256" not in request.headers:
            return "Missing header: X-Hub-Signature-256", 400

        if not validate_payload(request, slice['secret']):
            return "Signature mismatch (X-Hub-Signature-256)", 400



    return "", 204

@app.route('/')
def index():
    return "Hello, world!"