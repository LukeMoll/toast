import re
from flask import Flask, request

from .config import get_slice
from .github import validate_payload

app = Flask(__name__)

from .ansible import worker


@app.post("/hook/github/")
def hook_github():
    if "X-GitHub-Event" not in request.headers:
        return "Missing header: X-GitHub-Event", 400

    if request.headers["X-GitHub-Event"] == "ping":
        print("Recieved 'ping' event from GitHub")
        return "pong", 200

    if request.headers["X-GitHub-Event"] != "push":
        # return f"Unsupported event: {request.headers['X-GitHub-Event']}", 400
        print(f"Allowing unsupported event: {request.headers['X-GitHub-Event']}")

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

        if not validate_payload(request, slice_cfg["secret"]):
            return "Signature mismatch (X-Hub-Signature-256)", 400

    ##
    worker.queue_slice(slice_cfg)
    ##
    return "", 204


@app.route("/")
def index():
    return "Hello, world!"
