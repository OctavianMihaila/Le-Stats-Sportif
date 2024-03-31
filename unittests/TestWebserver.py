import os
import unittest
import requests
import json
import time

class TestWebserver(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Checking if the server is up.
        server_url = 'http://127.0.0.1:5000'
        for _ in range(5): 
            try:
                response = requests.get(server_url)
                if response.status_code == 200:
                    break
            except requests.ConnectionError:
                time.sleep(1) # Wait before retrying
        else:
            raise EnvironmentError("Server is not available. Cannot perform tests.")

    def setUp(self):
        # Create a few jobs before running each test method
        job_data = {"question": "Percent of adults aged 18 years and older who have obesity"}
        endpoints = [
            '/api/states_mean',
            '/api/best5',
            '/api/worst5',
            '/api/global_mean',
            '/api/diff_from_mean',
            '/api/mean_by_category',
        ]
        
        for endpoint in endpoints:
            response = requests.post(f'http://127.0.0.1:5000{endpoint}', json=job_data)
            # Ensure that the job creation was successful
            self.assertEqual(response.status_code, 200)

    def tearDown(self):
        # Delete everyting in the results folder
        for file in os.listdir('../results'):
            os.remove(f'../results/{file}')

    def test_get_results(self):
        # Test when job_id is valid and job is not in waiting queue
        response = requests.get('http://127.0.0.1:5000/api/get_results/1')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'error')

        # Test when job_id is not valid
        response = requests.get('http://127.0.0.1:5000/api/get_results/100')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'error')

        # Create a job so that we will have a job_id in the waiting queue
        req_data = {"question": "Percent of adults aged 18 years and older who have an overweight classification"}
        response = requests.post("http://127.0.0.1:5000/api/best5", json=req_data)
        self.assertEqual(response.status_code, 200)
        job_id = response.json()['job_id']

        # Test when job_id is done or is running
        response = requests.get(f'http://127.0.0.1:5000/api/get_results/{job_id}')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        # It can be both running or done
        self.assertTrue(data['status'] == 'running' or data['status'] == 'done')

    def test_get_jobs_info(self):
        response = requests.get('http://127.0.0.1:5000/api/jobs')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(isinstance(data, dict))
        
    def test_get_num_jobs(self):
        response = requests.get('http://127.0.0.1:5000/api/num_jobs')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        # Check if the response contains the expected key
        self.assertTrue('num_jobs' in data)
        # Check if the value is an integer
        self.assertTrue(isinstance(data['num_jobs'], int))
        self.assertTrue(data['num_jobs'] >= 0)

    def test_graceful_shutdown(self):
        response = requests.get('http://127.0.0.1:5000/api/graceful_shutdown')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        # Check if the response contains the expected key
        self.assertTrue('status' in data)
        # Check if the status is 'shutting down'
        self.assertEqual(data['status'], 'shutting down')

if __name__ == '__main__':
    unittest.main()
