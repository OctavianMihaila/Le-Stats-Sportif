from queue import Queue
from threading import Thread, Lock
import os
import json

class ThreadPool:
    def __init__(self):
        # TP_NUM_OF_THREADS is the environment variable that will be used to set the number of threads
        if 'TP_NUM_OF_THREADS' in os.environ:
            self.num_threads = int(os.environ['TP_NUM_OF_THREADS'])
        else: # If the environment variable is not set, use the number of CPUs the machine has
            self.num_threads = os.cpu_count()

        self.waiting_jobs = Queue()
        self.shutdown_trigger = False
        self.queue_lock = Lock()
        threads = []

        for _ in range(self.num_threads):
            thread = TaskRunner(self)
            threads.append(thread)
            thread.start()
    
    def get_waiting_jobs(self):
        return self.waiting_jobs

    def get_first_waiting_job(self):
        return self.waiting_jobs.get()
    
    def is_shutdown(self):
        return self.shutdown_trigger
    
    def set_shutdown_event(self):
        self.shutdown_trigger = True

class TaskRunner(Thread):
    def __init__(self, thread_pool):
        Thread.__init__(self)
        self.thread_pool = thread_pool

    def run(self):
        while not self.thread_pool.shutdown_trigger:
            # Get pending job
            self.thread_pool.queue_lock.acquire()
            job = self.thread_pool.get_first_waiting_job()
            self.thread_pool.queue_lock.release()
            # Execute the job and save the result to disk
            results = job.execute()

            # Save the results to disk
            with open(f"results/{job.job_id}", "w") as f:
                f.write(json.dumps(results))