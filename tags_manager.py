# Responsible for switching the code behavior based on bahave's tags per feature/scenario
from builtins import str
import random
import string
from contextlib import suppress
import os
import re

from datetime import date, timedelta
from random import randrange
from core import execution_logger
from test_data import random_data_generator
from enums.bdd_variables_enum import BddVariablesEnum
from core.api.appointments_api import set_vaccination_dose1_arrived


def set_geolocation(context, latitude, longitude):
    if ('mockGeolocation' in context.scenario.effective_tags) and ('desktop' in context.config.userdata['platform']):
        execution_logger.info(context.log,
                              'Setting geolocation for latitude: ' + str(latitude) + ' / longitude: ' + str(longitude))
        script = """
        navigator.geolocation.getCurrentPosition = function(success, failure) {
            success({ coords: {
                latitude: """ + str(latitude) + """,
                longitude: """ + str(longitude) + """,
            }, timestamp: Date.now() });
        }
        """
        context.js.execute_script(script)
