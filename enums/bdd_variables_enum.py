# Responsible for storing the supported keywords used as variables in the BDD layer
from builtins import object


class BddVariablesEnum(object):
    def __init__(self):
        pass

    ALLERGY_ACTION_EDIT = 'Edit'
    EXTRA_SHORT_ELEMENT_WAIT = 5
    SHORT_ELEMENT_WAIT = 10
    MEDIUM_ELEMENT_WAIT = 20
    LONG_ELEMENT_WAIT = 40
    EXTRA_LONG_ELEMENT_WAIT = 120
    MAX_LONG_ELEMENT_WAIT = 240

