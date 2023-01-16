import docker
from datetime import datetime
import time, sys, os
import logging as log


def run():
    logging = log.getLogger('docker-watcher')
    logging.setLevel(log.INFO)
    # logging is a singleton, make sure we don't duplicate the handlers and spawn additional log messages
    if not logging.handlers:
        logHandler = log.StreamHandler()
        logHandler.setLevel(log.INFO)
        logHandler.setFormatter(log.Formatter("{%(pathname)s:%(lineno)d} %(asctime)s - %(levelname)s - %(message)s", '%m/%d/%Y %I:%M:%S %p'))
        logging.addHandler(logHandler)
        logging = log.LoggerAdapter(logging)

    while True:
        client = docker.from_env()

        for img in client.images.list(all=True):
            for tag in img.tags:
                logging.info(f"Pulling: {tag}")
                try:
                    res = client.images.pull(tag)
                    logging.info(f"Successfully pulled: {res}")
                except Exception as error:
                    logging.error(error)
                
                if os.environ.get('DOCKER_REGISTRY'):
                    if not tag.startswith(os.environ.get('DOCKER_REGISTRY')):
                        try:
                            tstatus = img.tag(os.environ.get('DOCKER_REGISTRY') + tag)
                            if tstatus:
                                logging.info(f"Tagging: {os.environ.get('DOCKER_REGISTRY') + tag}")
                            else:
                                logging.error(f"Unable to set tag: {os.environ.get('DOCKER_REGISTRY') + tag}")
                            resp = client.images.push(os.environ.get('DOCKER_REGISTRY') + tag, stream=True, decode=True)
                            logging.info(f"Pushed {os.environ.get('DOCKER_REGISTRY') + tag}, received response: {resp}")
                        except Exception as error:
                            logging.error(error)
                else:
                    logging.warning("DOCKER_REGISTRY is not set")

        try:
            # cleanup and prune dangling images, only unused and untagged images
            logging.info("Starting to prune dangling images")
            pruned = client.images.prune(filters={"dangling": True})
            logging.info(f"Pruned: {pruned}")
        except Exception as error:
            logging.error(error)

        logging.info("Sleeping for one hour")
        time.sleep(60 * 60)
        

if __name__ == '__main__':
    run()