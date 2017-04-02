import json
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import asyncio
import logging


class StatsCollector:

    def __init__(self, token, endpoint, batch_size, loop):
        self.endpoint = endpoint
        self.headers = {"Content-Type": "application/json charset=utf-8",
                        "Authorization": "Bearer %s" % token}
        self.batch_size = batch_size
        self.batch = []
        self.loop = loop

    async def append_send(self, data):
        ts = data[0]
        readings = data[1]
        meta = data[2]
        stats = {"timestamp": ts, "data": readings, "meta": meta}
        self.batch.append(stats)
        logging.debug('Appending %s', stats)

        if len(self.batch) >= self.batch_size:
            data = json.dumps(self.batch).encode("utf-8")
            l = len(data)
            self.headers.update({"Content-Length": l})
            req = Request(self.endpoint, data, self.headers)
            try:
                logging.info("Sending %d items", len(self.batch))
                response = urlopen(req)
                logging.info('Sent!')
            except HTTPError as e:
                logging.error('Server responded with an error code: ', e.code)
            except URLError as e:
                logging.error('URL error: ', e.reason)

            self.batch = []

    def collect(self, stats):
        self.loop.call_soon_threadsafe(asyncio.ensure_future, self.append_send(stats))
