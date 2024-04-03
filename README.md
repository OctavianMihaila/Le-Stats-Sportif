# Le Stats Sportif

Author: Mihaila Octavian-Iulian
Group: 333CB

## Overview

Le Stats Sportif is a web application designed to provide users with statistics analysis using Python Flask. The app exposes an API to receive requests from clients, allowing users to submit specific queries for data analysis (nutrition and activity in the US). Utilizing a thread pool, the app efficiently processes these requests in the background, ensuring optimal performance without disrupting the user experience.

## Structure

- **app**
  - **\_\_init\_\_.py**: initializes the Flask app
  - **data_ingestion.py**: contains the data ingestion logic
  - **routes.py**: contains the API routes
  - **job.py**: contains the routines that are used to query the data
  - **task_runner.py**: contains the thread pool logic

## How to Run

1. Initialize virtual environment and install dependencies:
  ```
  python3 -m venv venv
  ```
  ```
  source venv/bin/activate
  ```
  ```
  pip install -r requirements.txt
  ```
2. Open two shells with the virtual environment activated:
- In the first shell, run the server:
  ```
  make run_server
  ```
- In the second shell, you can run any code that makes requests to the server (e.g., to test the functionality):
  ```
  make run_tests
  ```

## Implementation

- The API exposed by the server is implemented in `routes.py`, where requests are processed and jobs are created and stored in a waiting queue. Additionally, there are endpoints for querying the status of the jobs and for retrieving the results of the jobs or the number of jobs that are currently in the system along with their status.

- A thread pool processes incoming jobs. It uses a number of threads equal to the environment variable `TP_NUM_OF_THREADS` or the system's CPU count if the variable is unset. Threads start when the server starts, waiting for jobs in the queue. They process jobs and store results in the `results/` directory until shutdown is triggered.

- The query logic is implemented in `job.py`, where a class (`Job`) represents the object that is created when a query is received. There are also routines for each type of query that are referenced in the `Job` object that is created. When the job's execute method is called by a thread, the routine is called along with the necessary parameters, and the result is returned and then written to a file with the name as the job's id.

- All the data is taken from the CSV file `nutrition_activity_obesity_us_subset.csv` and is processed by the `data_ingestor`, which is also responsible for deciding whether the data should be sorted ascending or descending based on the question that is asked.

## Testing

- Unit tests were created to cover all the endpoints from `routes.py`. These unit tests are placed in `unittests/TestWebserver.py` and can be run only if the server is running. The tests are run using the `unittest` module from Python.

## Logging

- The server logs are stored in `webserver.log` files created using `RotatingFileHandler` from Python's `logging` module. The logs are stored in the root directory of the project and are 256KB in size. There can be a maximum of 20 log files created. The coverage of the logs is for the requests that are made to the server, along with the data that is received and returned to the client (max first 100 chars of the returned data in order to be able to understand what is going on in that log file.).

## Other Details

- The implementation is considered efficient and well-structured.
- The assignment is considered useful but has too little to do with this course.
- More tests should be added to ensure that in case of a functionality extension, there will be no bugs.

## Resources

- [Course Material 01](https://ocw.cs.pub.ro/courses/asc/laboratoare/01)
- [Course Material 02](https://ocw.cs.pub.ro/courses/asc/laboratoare/02)
- [Course Material 03](https://ocw.cs.pub.ro/courses/asc/laboratoare/03)
- [Python Logging Documentation](https://docs.python.org/3/library/logging.html)
- [Python Unittest Documentation](https://docs.python.org/3/library/unittest.html)

## Git Repository

[Le Stats Sportif](https://github.com/OctavianMihaila/Le-Stats-Sportif)
