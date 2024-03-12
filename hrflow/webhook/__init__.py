"""Webhook support."""

import hashlib
import hmac
import inspect
import json
import sys

from . import base64Wrapper as base64W
from . import bytesutils, hmacutils

EVENT_PROFILE_PARSE_SUCCESS = "profile.parse.success"
EVENT_PROFILE_PARSE_ERROR = "profile.parse.error"
EVENT_PROFILE_SCORE_SUCCESS = "profile.score.success"
EVENT_PROFILE_SCORE_ERROR = "profile.score.error"
EVENT_JOB_TRAIN_SUCCESS = "job.train.success"
EVENT_JOB_TRAIN_ERROR = "job.train.error"
EVENT_JOB_TRAIN_START = "job.train.start"
EVENT_JOB_SCORE_SUCCESS = "job.score.success"
EVENT_JOB_SCORE_ERROR = "job.score.error"
EVENT_JOB_SCORE_START = "job.score.start"
ACTION_STAGE_SUCCESS = "action.stage.success"
ACTION_STAGE_ERROR = "action.stage.error"
ACTION_RATING_SUCCESS = "action.rating.success"
ACTION_RATING_ERROR = "action.rating.error"


SIGNATURE_HEADER = "HTTP-HRFLOW-SIGNATURE"


class Webhook(object):
    """Class that handles Webhooks."""

    def __init__(self, client):
        """Init."""
        self.client = client
        self.handlers = {
            EVENT_PROFILE_PARSE_SUCCESS: None,
            EVENT_PROFILE_PARSE_ERROR: None,
            EVENT_PROFILE_SCORE_SUCCESS: None,
            EVENT_PROFILE_SCORE_ERROR: None,
            EVENT_JOB_TRAIN_SUCCESS: None,
            EVENT_JOB_TRAIN_ERROR: None,
            EVENT_JOB_TRAIN_START: None,
            EVENT_JOB_SCORE_SUCCESS: None,
            EVENT_JOB_SCORE_ERROR: None,
            EVENT_JOB_SCORE_START: None,
            ACTION_STAGE_SUCCESS: None,
            ACTION_STAGE_ERROR: None,
            ACTION_RATING_SUCCESS: None,
            ACTION_RATING_ERROR: None,
        }

    def check(self, url, type):
        """
        Get response from api for POST webhook/check.

        Args:
            url:              <string>
                              url id
            type:             <type>
                              profile id

        Returns
            Webhook information

        """
        data = {}
        data["url"] = url
        data["type"] = type
        response = self.client.post("webhook/check", json=data)
        return response.json()

    def test(self):
        """Get response from api for POST webhook/check."""
        response = self.client.post("webhook/test")
        return response.json()

    def setHandler(self, event_name, callback):
        """Set an handler for given event."""
        if event_name not in self.handlers:
            raise ValueError("{} is not a valid event".format(event_name))
        if callable(event_name):
            raise TypeError("{} is not callable".format(callback))
        self.handlers[event_name] = callback

    def isHandlerPresent(self, event_name):
        """Check if an event has an handler."""
        if event_name not in self.handlers:
            raise ValueError("{} is not a valid event".format(event_name))
        return self.handlers[event_name] is not None

    def removeHandler(self, event_name):
        """Remove handler for given event."""
        if event_name not in self.handlers:
            raise ValueError("{} is not a valid event".format(event_name))
        self.handlers[event_name] = None

    def _strtr(self, inp, fr, to):
        res = ""
        for c in inp:
            for idx, c_to_replace in enumerate(fr):
                if c == c_to_replace and idx < len(to):
                    c = to[idx]
            res = res + c
        return res

    def _get_signature_header(self, signature_header, request_headers):
        if signature_header is not None:
            return signature_header
        if SIGNATURE_HEADER in request_headers:
            return request_headers[SIGNATURE_HEADER]
        raise ValueError("Error: No {} given".format(SIGNATURE_HEADER))

    def _get_fct_number_of_arg(self, fct):
        """Get the number of argument of a fuction."""
        py_version = sys.version_info[0]
        if py_version >= 3:
            return len(inspect.signature(fct).parameters)
        return len(inspect.getargspec(fct)[0])

    def handle(self, request_headers={}, signature_header=None):
        """Handle request."""
        if self.client.webhook_secret is None:
            raise ValueError("Error: no webhook secret.")
        encoded_header = self._get_signature_header(signature_header, request_headers)
        decoded_request = self._decode_request(encoded_header)
        if "type" not in decoded_request:
            raise ValueError("Error invalid request: no type field found.")
        handler = self._getHandlerForEvent(decoded_request["type"])
        if handler is None:
            return
        if self._get_fct_number_of_arg(handler) == 1:
            handler(decoded_request)
            return
        handler(decoded_request, decoded_request["type"])

    def _base64Urldecode(self, inp):
        inp = self._strtr(inp, "-_", "+/")
        byte_inp = base64W.decodebytes(bytesutils.strtobytes(inp, "ascii"))
        return byte_inp.decode("ascii")

    def _is_signature_valid(self, signature, payload):
        utf8_payload = bytesutils.strtobytes(payload, "utf8")
        utf8_wb_secret = bytesutils.strtobytes(self.client.webhook_secret, "utf8")
        hasher = hmac.new(utf8_wb_secret, utf8_payload, hashlib.sha256)
        exp_sign_digest = hasher.hexdigest()

        return hmacutils.compare_digest(exp_sign_digest, signature)

    def _decode_request(self, encoded_request):
        tmp = encoded_request.split(".", 2)
        if len(tmp) < 2:
            raise ValueError(
                "Error invalid request. Maybe it's not the 'HTTP-HRFLOW-SIGNATURE'"
                " field"
            )
        encoded_sign = tmp[0]
        payload = tmp[1]
        sign = self._base64Urldecode(encoded_sign)
        data = self._base64Urldecode(payload)
        if not self._is_signature_valid(sign, data):
            raise ValueError("Error: invalid signature.")
        return json.loads(data)

    def _getHandlerForEvent(self, event_name):
        if event_name not in self.handlers:
            raise ValueError("{} is not a valid event".format(event_name))
        handler = self.handlers[event_name]
        return handler
