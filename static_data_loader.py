import yaml
import json
import logging
import os


class StaticDataLoader:
    def __init__(self):
        logging.basicConfig(level=logging.INFO,
                            format='[%(levelname)-8s %(asctime)s] %(message)s')
        self.logger = logging.getLogger(__name__)

    def load_static_data(self, context):
        try:
            with open(os.path.join('test_data', 'static_data.yaml'), 'r') as ymlfile:
                context.static_data = yaml.safe_load(ymlfile)

        except IOError:
            self.logger.error(
                'Something went wrong')
