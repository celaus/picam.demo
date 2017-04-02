import argh
from collector import StatsCollector
from capture.picameracapture import PiCameraCapture
import toml
from auth import get_token
import asyncio


def capture(config_file_name='config.toml'):
    'Capture and analyze camera input and store the results on a server.'

    with open(config_file_name) as conffile:
        config = toml.loads(conffile.read())
    token = get_token(config["server"]["secret"], config[
                      "agent"]["name"], config["agent"]["role"])
    loop = asyncio.get_event_loop()
    collector = StatsCollector(loop=loop, token=token, batch_size=config["server"][
        "batch_size"], endpoint=config["server"]["endpoint"])

    loop.call_later(3, lambda: camcap.detect(
        collector, **config["haarcascades"]))
    loop.run_forever()


def main():
    argh.dispatch_command(capture)

if __name__ == '__main__':
    main()
