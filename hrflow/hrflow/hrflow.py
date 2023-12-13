import json

import requests as req

from .auth import Auth
from .board import Board
from .job import Job
from .profile import Profile
from .rating import Rating
from .source import Source
from .text import Text
from .tracking import Tracking
from .webhook import Webhook

CLIENT_API_URL = "https://api.hrflow.ai/v1/"


class Hrflow(object):
    """client api wrapper client."""

    def __init__(
        self,
        api_url=CLIENT_API_URL,
        api_secret=None,
        api_user=None,
        webhook_secret=None,
    ):
        """
        Hrflow client. This class is the main entry point to the Hrflow API.

        Args:
            api_url:                <string>
                                    The API URL. Defaults to https://api.hrflow.ai/v1/

            api_secret:             <string>
                                    The API secret key. You can find it in your
                                    Hrflow.ai account.

            api_user:               <string>
                                    The API user email. You can find it in your
                                    Hrflow.ai account.

            webhook_secret:         <string>

        Returns
            Hrflow client object
        """
        self.api_url = api_url
        self.auth_header = {"X-API-KEY": api_secret, "X-USER-EMAIL": api_user}
        self.webhook_secret = webhook_secret
        self.auth = Auth(self)
        self.job = Job(self)
        self.profile = Profile(self)
        self.text = Text(self)
        self.webhooks = Webhook(self)
        self.source = Source(self)
        self.board = Board(self)
        self.tracking = Tracking(self)
        self.rating = Rating(self)

    def _create_request_url(self, resource_url):
        return "{api_endpoint}{resource_url}".format(
            api_endpoint=self.api_url, resource_url=resource_url
        )

    def _fill_headers(self, header, base={}):
        for key, value in header.items():
            base[key] = value
        return base

    def _validate_args(self, bodyparams):
        for key, value in bodyparams.items():
            if isinstance(value, list):
                bodyparams[key] = json.dumps(value)
        return bodyparams

    def get(self, resource_endpoint, query_params={}):
        """
        This a method for internal use only.
        It is used to make a GET request to the Hrflow API.
        It's not meant to be used directly by the user.

        Args:
            resource_endpoint:      <string>
                                    The resource endpoint. For example: "job/indexing"

            query_params:           <dict>
                                    The query parameters to be sent to the API. It
                                    must be a dictionary.

        Returns
            Make the corresponding GET request to the Hrflow API and returns the
            response object.
        """
        url = self._create_request_url(resource_endpoint)
        if query_params:
            query_params = self._validate_args(query_params)
            return req.get(url, headers=self.auth_header, params=query_params)
        else:
            return req.get(url, headers=self.auth_header)

    def post(self, resource_endpoint, data={}, json={}, files=None):
        """
        This a method for internal use only.
        It is used to make a POST request to the Hrflow API.
        It's not meant to be used directly by the user.

        Args:
            resource_endpoint:      <string>
                                    The resource endpoint. For example: "job/indexing"

            data:                   <dict>
                                    The data payload (for multipart/formdata) to be
                                    sent to the API. It must be a dictionary.

            json:                   <dict>
                                    The json payload to be sent to the API. It must
                                    be a dictionary.

            files:                  <dict>
                                    The files payload to be sent to the API. It must
                                    be a dictionary. (ie. {"file": open("file.pdf",
                                    "rb")}

        Returns:
            Makes the corresponding POST request to the Hrflow API and returns the
            response object.
        """
        url = self._create_request_url(resource_endpoint)
        if files:
            data = self._validate_args(data)
            return req.post(url, headers=self.auth_header, files=files, data=data)
        else:
            return req.post(url, headers=self.auth_header, data=data, json=json)

    def patch(self, resource_endpoint, json={}):
        """
        This a method for internal use only.
        It is used to make a PATCH request to the Hrflow API.
        It's not meant to be used directly by the user.

        Args:
            resource_endpoint:      <string>
                                    The resource endpoint. For example: "job/indexing"

            json:                   <dict>
                                    The json payload to be sent to the API. It must
                                    be a dictionary.

        Returns:
            Makes the corresponding PATCH request to the Hrflow API and returns the
            response object.
        """
        url = self._create_request_url(resource_endpoint)
        data = self._validate_args(json)
        return req.patch(url, headers=self.auth_header, json=data)

    def put(self, resource_endpoint, json={}):
        """
        This a method for internal use only.
        It is used to make a PUT request to the Hrflow API.
        It's not meant to be used directly by the user.

        Args:
            resource_endpoint:      <string>
                                    The resource endpoint. For example: "job/indexing"

            json:                   <dict>
                                    The json payload to be sent to the API. It must
                                    be a dictionary.

        Returns:
            Makes the corresponding PUT request to the Hrflow API and returns the
            response object.
        """
        url = self._create_request_url(resource_endpoint)
        return req.put(url, headers=self.auth_header, json=json)
