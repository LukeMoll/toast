import hmac

from flask import Request

def validate_payload(req : Request, secret: str) -> bool:
    signature = req.headers["X-Hub-Signature-256"]

    h = hmac.new(secret.encode('utf-8'), msg=req.get_data(), digestmod='sha256')
    return hmac.compare_digest('sha256=' + h.hexdigest(), signature)