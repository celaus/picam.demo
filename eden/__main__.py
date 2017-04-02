import argh
from collector import StatsCollector
from capture.picameracapture import PiCameraCapture
import toml
from auth import get_token
import asyncio
import logging
from threading import Thread


def capture(config_file_name='config.toml'):
    'Capture and analyze camera input and store the results on a server.'

    logging.basicConfig(level=logging.INFO)
    logging.info('Starting eden picam')

    with open(config_file_name) as conffile:
        config = toml.loads(conffile.read())
    logging.info('Parsed config')

    token = get_token(config["server"]["secret"], config[
                      "agent"]["name"], config["agent"]["role"])
    loop = asyncio.get_event_loop()

    logging.info('Creating collector')
    collector = StatsCollector(loop=loop, token=token, batch_size=config["server"][
        "batch_size"], endpoint=config["server"]["endpoint"])

    camcap = PiCameraCapture(**config["camera"])

    logging.info('Starting event loop')

    t = Thread(target=lambda: camcap.detect(
        collector, **config["haarcascades"]), daemon=True)
    t.start()
    loop.run_forever()


def main():
    argh.dispatch_command(capture)

if __name__ == '__main__':
    main()
