from traceback import format_tb
from functools import wraps
from config.topic_config import TOPIC_PARAMS
from flask import make_response, request, Response
import json


def catch_error(func):
    @wraps(func)
    def _handle(*k, **v):
        try:
            return func(*k, **v)
        except Exception as error:
            print(format_tb(error.__traceback__), type(error), error)
            # resp = Response(json.dumps(response[-200]))
            # resp = Response(json.dumps(error))
            # resp.headers['Access-Control-Allow-Origin'] = '*'
            # resp.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
            # resp.headers['Access-Control-Allow-Headers'] = 'token'
            # return resp
    return _handle

