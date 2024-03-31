from flask import Flask
from app.data_ingestor import DataIngestor
from app.task_runner import ThreadPool
from queue import Queue
import logging
from logging.handlers import RotatingFileHandler
import time

# Max size of the log file is 1MB, and we keep 20 backup copies
handler = RotatingFileHandler('webserver.log', maxBytes=256*256, backupCount=20)
handler.setLevel(logging.INFO)

# Define a custom formatter to format log records with UTC/GMT time
class UTCFormatter(logging.Formatter):
    converter = time.gmtime

formatter = UTCFormatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Add the rotating file handler to the logger
logging.getLogger().addHandler(handler)
logging.getLogger().setLevel(logging.INFO)

webserver = Flask(__name__)
webserver.tasks_runner = ThreadPool()
webserver.data_ingestor = DataIngestor("./nutrition_activity_obesity_usa_subset.csv")
webserver.job_counter = 1

from app import routes
