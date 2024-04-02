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

    def poll_job_status(self, job_id):
        # Poll job status until it becomes "done"
        while True:
            response = requests.get(f'http://127.0.0.1:5000/api/get_results/{job_id}')
            data = response.json()
            if data['status'] == 'done':
                break
            time.sleep(1)

    def send_request_and_compare(self, req_data, ref_file, endpoint):
        # Send POST request
        response = requests.post("http://127.0.0.1:5000/api/" + endpoint, json=req_data)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Get job_id
        job_id = data['job_id']
        
        # Poll job status until it becomes "done"
        self.poll_job_status(job_id)
        
        # Get results of the job
        response = requests.get(f'http://127.0.0.1:5000/api/get_results/{job_id}')
        self.assertEqual(response.status_code, 200)
        data = response.json()

        # check if the results are as expected
        with open(ref_file, 'r') as file:
            ref_data = json.load(file)
        self.assertEqual(data['data'], ref_data)

    def test_state_mean_1(self):
        req_data = {"question": "Percent of adults aged 18 years and older who have obesity", "state": "Ohio"}
        self.send_request_and_compare(req_data, 'refs/state_mean_1.json', 'state_mean')

    def test_state_mean_2(self):
        req_data = {"question": "Percent of adults who report consuming vegetables less than one time daily", "state": "Texas"}
        self.send_request_and_compare(req_data, 'refs/state_mean_2.json', 'state_mean')

    def test_states_mean_1(self):
        req_data = {"question": "Percent of adults aged 18 years and older who have obesity"}
        self.send_request_and_compare(req_data, 'refs/states_mean_1.json', 'states_mean')

    def test_states_mean_2(self):
        req_data = {"question": "Percent of adults who engage in muscle-strengthening activities on 2 or more days a week"}
        self.send_request_and_compare(req_data, 'refs/states_mean_2.json', 'states_mean')

    def test_best5_1(self):
        req_data = {"question": "Percent of adults aged 18 years and older who have obesity"}
        self.send_request_and_compare(req_data, 'refs/best5_1.json', 'best5')

    def test_best5_2(self):
        req_data = {"question": "Percent of adults who report consuming vegetables less than one time daily"}
        self.send_request_and_compare(req_data, 'refs/best5_2.json', 'best5')

    def test_worst5_1(self):
        req_data = {"question": "Percent of adults who report consuming fruit less than one time daily"}
        self.send_request_and_compare(req_data, 'refs/worst5_1.json', 'worst5')

    def test_worst5_2(self):
        req_data = {"question": "Percent of adults who engage in no leisure-time physical activity"}
        self.send_request_and_compare(req_data, 'refs/worst5_2.json', 'worst5')

    def test_global_mean_1(self):
        req_data = {"question": "Percent of adults aged 18 years and older who have obesity"}
        self.send_request_and_compare(req_data, 'refs/global_mean_1.json', 'global_mean')

    def test_global_mean_2(self):
        req_data = {"question": "Percent of adults who report consuming vegetables less than one time daily"}
        self.send_request_and_compare(req_data, 'refs/global_mean_2.json', 'global_mean')

    def test_diff_from_mean_1(self):
        req_data = {"question": "Percent of adults aged 18 years and older who have obesity", "state": "Ohio"}
        self.send_request_and_compare(req_data, 'refs/diff_from_mean_1.json', 'diff_from_mean')

    def test_diff_from_mean_2(self):
        req_data = {"question": "Percent of adults who report consuming vegetables less than one time daily", "state": "Texas"}
        self.send_request_and_compare(req_data, 'refs/diff_from_mean_2.json', 'diff_from_mean')

    def test_mean_by_category_1(self):
        req_data = {"question": "Percent of adults aged 18 years and older who have obesity"}
        self.send_request_and_compare(req_data, 'refs/mean_by_category_1.json', 'mean_by_category')

    def test_mean_by_category_2(self):
        req_data = {"question": "Percent of adults who report consuming vegetables less than one time daily"}
        self.send_request_and_compare(req_data, 'refs/mean_by_category_2.json', 'mean_by_category')

    def test_state_mean_by_category_1(self):
        req_data = {"question": "Percent of adults aged 18 years and older who have obesity", "state": "Ohio"}
        self.send_request_and_compare(req_data, 'refs/state_mean_by_category_1.json', 'state_mean_by_category')

    def test_state_mean_by_category_2(self):
        req_data = {"question": "Percent of adults who report consuming vegetables less than one time daily", "state": "Texas"}
        self.send_request_and_compare(req_data, 'refs/state_mean_by_category_2.json', 'state_mean_by_category')


if __name__ == '__main__':
    unittest.main()
