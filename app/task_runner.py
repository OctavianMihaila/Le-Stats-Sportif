from queue import Queue
from threading import Thread, Event
import time
import os

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
    
    def get_waiting_jobs(self):
        return self.waiting_jobs

    def get_first_waiting_job(self):
        return self.waiting_jobs.get()
    
    def get_job_results(self):
        return self.job_results
    
    def graceful_shutdown(self):
        self.graceful_shutdown = True

    # def check_job_in_waiting_queue(self, job_id):
    #     queue_copy = self.waiting_jobs.queue
    #     for job in queue_copy:
    #         if job.job_id == job_id:
    #             return True
            
    #     return False

class TaskRunner(Thread):
    def __init__(self):
        pass

    def run(self):
        while not self.shutdown_event.is_set():
            # TODO
            # Get pending job
            job = ThreadPool.get_first_waiting_job()
            # Execute the job and save the result to disk
            job.execute()