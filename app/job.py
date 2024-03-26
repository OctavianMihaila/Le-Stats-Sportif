class Job:
    def __init__(self, job_id, job_endpoint, data):
        self.job_id = job_id
        self.job_endpoint = job_endpoint
        self.data = data
        self.result = None

    def execute(self):
        # TODO
        # Execute the job
        pass

    def save_result(self):
        # TODO
        # Save the result to disk
        pass

    def get_result(self):
        # TODO
        # Return the result
        pass
