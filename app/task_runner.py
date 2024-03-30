from queue import Queue
from threading import Thread, Event, Lock
import time
import os
import json

class ThreadPool:
    def __init__(self):
        # You must implement a ThreadPool of TaskRunners
        # Your ThreadPool should check if an environment variable TP_NUM_OF_THREADS is defined
        # If the env var is defined, that is the number of threads to be used by the thread pool
        # Otherwise, you are to use what the hardware concurrency allows
        # You are free to write your implementation as you see fit, but
        # You must NOT:
        #   * create more threads than the hardware concurrency allows
        #   * recreate threads for each task

        if 'TP_NUM_OF_THREADS' in os.environ:
            self.num_threads = int(os.environ['TP_NUM_OF_THREADS'])
        else:
            self.num_threads = os.cpu_count()

        # Jobs that are waiting to be executed or are currently being executed
        self.waiting_jobs = Queue()
        
        # Jobs that are finished
        self.job_results = {}

        self.shutdown_event = Event()
        self.file_write_lock = Lock()

        threads = []

        for _ in range(self.num_threads):
            thread = TaskRunner(self)
            threads.append(thread)
            thread.start()
    
    def get_waiting_jobs(self):
        return self.waiting_jobs

    def get_first_waiting_job(self):
        return self.waiting_jobs.get()

class TaskRunner(Thread):
    def __init__(self, thread_pool):
        Thread.__init__(self)
        self.thread_pool = thread_pool

    def run(self):
        while not self.thread_pool.shutdown_event.is_set():
            # TODO
            # Get pending job
            job = self.thread_pool.get_first_waiting_job()
            # Execute the job and save the result to disk
            results = job.execute()
            # print('Results are: ', results)
            with self.thread_pool.file_write_lock:
                with open(f"results/{job.job_id}", "w") as f:
                    f.write(json.dumps(results))