import tornado.httpclient
import urllib.parse

import httpserver.handler


class CTestClientHandler(httpserver.handler.CRequestHandler):

    def do_get(self, *args, **kwargs):
        params = self.get_query_params()
        method = params.get("method", "GET")
        url = params.get("url", "http://www.baidu.com")

        async_client = tornado.httpclient.AsyncHTTPClient()
        request = tornado.httpclient.HTTPRequest(
            url, method=method, **kwargs)
        async_client.fetch(request, callback=self.on_response)

    def on_response(self, response):
        if response.error:
            print(">>>>>Error:", response.error)
        else:
            print(">>>>>Body:", response.body)

        response_data = {
            "status_code": 200,
            "message": "success",
            "payload": self.get_query_params(),
            "in_client": "in_client",
        }
        self.response_to_web(response_data)