import json
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import asyncio



class StatsCollector:

    def __init__(self, token, endpoint, batch_size, loop):
        self.endpoint = endpoint
        self.auth = {"Authorization": "Bearer %s" % token}
        self.batch_size = batch_size
        self.batch = []
        self.loop = loop

    def append_send(self, data):
        self.batch.append(stats)
        if len(self.batch) >= self.batch_size:
            data = json.dumps(self.batch)

            req = Request(self.endpoint, data, )
            try:
                response = urlopen(req)
            except HTTPError as e:
                print('The server couldn\'t fulfill the request.')
                print('Error code: ', e.code)
            except URLError as e:
                print('We failed to reach a server.')
                print('Reason: ', e.reason)

            self.batch = []

    def collect(self, stats):
        self.loop.call_soon(lambda s: self.batch.append(s), stats)
