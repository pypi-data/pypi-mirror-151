import os
import logging, sys

# Set logger with proper format for backend parsing to status page
from .constants import LOGGER_NAME, API_ENDPOINT

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
log = logging.Logger(LOGGER_NAME)

logger_handler = logging.StreamHandler()
logger_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
log.addHandler(logger_handler)


# authentication process
TOKEN = os.getenv('NG_API_AUTHTOKEN')
LOGIN = os.getenv('LOGIN')
PASSWORD = os.getenv('PASSWORD')

# system env variables
JOB_ID = os.environ.get('JOBID')
PIPELINE_ID = os.environ.get('PIPELINE_ID')
EID = os.environ.get('EID')
ENDPOINT = os.environ.get('NG_API_ENDPOINT', API_ENDPOINT)
COMPONENT_NAME = os.environ.get('NG_COMPONENT_NAME')
GROUP_NAME = os.environ.get('NG_STATUS_GROUP_NAME', '')


# Authentication from Token or login/password
if TOKEN is None or TOKEN == '':
    if LOGIN is None or LOGIN == '':
        raise Exception("No LOGIN found. Set the environment variable with the LOGIN")
    if PASSWORD is None or PASSWORD == '':
        raise Exception("No PASSWORD found. Set the environment variable with the PASSWORD")


# Import the methods
from .DatalakeHandler import *
from .TaskHandler import *
from .StatusHandler import *
from .Timeseries import *
