import argh
from collector import StatsCollector
from capture.picameracapture import PiCameraCapture
import toml
from auth import get_token
import asyncio
import logging
from threading import Thread
from capture.server import run_server


def capture(config_file_name='config.toml'):
    'Capture and analyze camera input and store the results on a server.'

    logging.basicConfig(level=logging.INFO)
    logging.info('Starting eden picam')

    with open(config_file_name) as conffile:
        config = toml.loads(conffile.read())
    logging.info('Parsed config')

    eden_server_conf = config["eden-server"]
    agent_conf = config["agent"]
    mjpeg_server_conf = config["mjpeg-server"]

    token = get_token(eden_server_conf["secret"], agent_conf[
                      "name"], agent_conf["role"])

    loop = asyncio.get_event_loop()

    logging.info('Creating collector')
    collector = StatsCollector(loop=loop, token=token, batch_size=eden_server_conf[
        "batch_size"], endpoint=eden_server_conf["endpoint"])

    camcap = PiCameraCapture(**config["camera"])

    if mjpeg_server_conf["enable"]:
        logging.info('Starting MJPEG server')
        mjpeg_server = Thread(target=lambda: run_server(camcap, mjpeg_server_conf[
                              "host"], mjpeg_server_conf["port"]), daemon=True)
        mjpeg_server.start()

    logging.info('Starting detector')
    t = Thread(target=lambda: camcap.detect(
        collector, **config["haarcascades"]), daemon=True)
    t.start()

    logging.info('Starting event loop')
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        logging.info("Shutting down...")
    finally:
        camcap.stop()
        t.join()


def main():
    argh.dispatch_command(capture)

if __name__ == '__main__':
    main()
