from flask import Flask
from app.data_ingestor import DataIngestor
from app.task_runner import ThreadPool
from queue import Queue
import logging

logging.basicConfig(filename='webserver.log', level=logging.INFO)

webserver = Flask(__name__)
webserver.tasks_runner = ThreadPool()

# webserver.tasks_runner.start()

webserver.data_ingestor = DataIngestor("./nutrition_activity_obesity_usa_subset.csv")

webserver.job_counter = 1

# webserver.waiting_queue
# webserver.job_results
# webserver.is_shutdown = False

from app import routes
