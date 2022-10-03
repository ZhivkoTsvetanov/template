import yaml
import json
import logging
import os


class StaticDataLoader:
    def __init__(self):
        logging.basicConfig(level=logging.INFO,
                            format='[%(levelname)-8s %(asctime)s] %(message)s')
        self.logger = logging.getLogger(__name__)

    def load_label_tags_config(self):
        with open('label_tags_config.yaml', 'r') as ymlfile:
            return yaml.safe_load(ymlfile)

    def load_static_data(self, context):
        try:
            with open(os.path.join('test_data', 'static_data.yaml'), 'r') as ymlfile:
                context.static_data = yaml.safe_load(ymlfile)

        except IOError:
            self.logger.error(
                'Could not find one of these files: ui_elements_vault.yaml, static_data.yaml, register_member.json, os_devices_list_members.yaml!')
