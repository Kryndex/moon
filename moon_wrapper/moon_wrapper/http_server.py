# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

from flask import Flask, jsonify
from flask_restful import Resource, Api
import logging
from moon_wrapper import __version__
from moon_wrapper.api.generic import Status, Logs, API
from moon_wrapper.api.oslowrapper import OsloWrapper
from python_moonutilities.cache import Cache
from python_moonutilities import configuration, exceptions

logger = logging.getLogger("moon.wrapper.http_server")


CACHE = Cache()

__API__ = (
    Status, Logs, API
 )


class Server:
    """Base class for HTTP server"""

    def __init__(self, host="localhost", port=80, api=None, **kwargs):
        """Run a server

        :param host: hostname of the server
        :param port: port for the running server
        :param kwargs: optional parameters
        :return: a running server
        """
        self._host = host
        self._port = port
        self._api = api
        self._extra = kwargs

    @property
    def host(self):
        return self._host

    @host.setter
    def host(self, name):
        self._host = name

    @host.deleter
    def host(self):
        self._host = ""

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, number):
        self._port = number

    @port.deleter
    def port(self):
        self._port = 80

    def run(self):
        raise NotImplementedError()


class Root(Resource):
    """
    The root of the web service
    """
    __urls__ = ("/", )
    __methods = ("get", "post", "put", "delete", "options")

    def get(self):
        tree = {"/": {"methods": ("get",),
                      "description": "List all methods for that service."}}
        for item in __API__:
            tree[item.__name__] = {"urls": item.__urls__}
            _methods = []
            for _method in self.__methods:
                if _method in dir(item):
                    _methods.append(_method)
            tree[item.__name__]["methods"] = _methods
            tree[item.__name__]["description"] = item.__doc__.strip()
        return {
            "version": __version__,
            "tree": tree
        }


class HTTPServer(Server):

    def __init__(self, host="localhost", port=80, **kwargs):
        super(HTTPServer, self).__init__(host=host, port=port, **kwargs)
        self.app = Flask(__name__)
        self.port = port
        conf = configuration.get_configuration("components/orchestrator")
        _hostname = conf["components/orchestrator"].get("hostname",
                                                        "orchestrator")
        _port = conf["components/orchestrator"].get("port", 80)
        _protocol = conf["components/orchestrator"].get("protocol", "http")
        self.orchestrator_url = "{}://{}:{}".format(
            _protocol, _hostname, _port)
        # Todo : specify only few urls instead of *
        # CORS(self.app)
        self.api = Api(self.app)
        self.__set_route()
        self.__hook_errors()

    def __hook_errors(self):

        def get_404_json(e):
            return jsonify({"result": False, "code": 404,
                            "description": str(e)}), 404
        self.app.register_error_handler(404, get_404_json)

        def get_400_json(e):
            return jsonify({"result": False, "code": 400,
                            "description": str(e)}), 400
        self.app.register_error_handler(400, lambda e: get_400_json)
        self.app.register_error_handler(403, exceptions.AuthException)

    def __set_route(self):
        self.api.add_resource(Root, '/')

        for api in __API__:
            self.api.add_resource(api, *api.__urls__)
        self.api.add_resource(OsloWrapper, *OsloWrapper.__urls__,
                              resource_class_kwargs={
                                  "orchestrator_url": self.orchestrator_url,
                                  "cache": CACHE,
                              }
                              )

    def run(self):
        self.app.run(host=self._host, port=self._port)  # nosec

