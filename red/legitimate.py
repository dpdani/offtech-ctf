import random
import time
import urllib.error
import urllib.request

from loguru import logger

from red.config import config


def main():
    i = -1
    while True:
        i += 1
        resource = config.legitimate.resources[i % len(config.legitimate.resources)]
        url = f"http://{config.server_host}:{config.server_port}/{resource}"
        logger.info(f"Requesting {url}")
        try:
            contents = urllib.request.urlopen(url, timeout=9).read()  # GET requests the server
        except urllib.error.HTTPError as e:
            logger.info(f"Got: {e}")  # Handle 404 and ignores it because be actually want to request a 404
        except Exception as e:
            logger.error(f"Error: {e}")
        else:
            logger.info(f"Got: {contents}")
        time.sleep(config.legitimate.rate + random.uniform(-1, 1))  # Sleeps a random number of seconds between rate-1 and rate+1


if __name__ == '__main__':
    main()
