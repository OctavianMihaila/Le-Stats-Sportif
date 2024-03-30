from typing import Callable
# from flask import jsonify
import json
# from app import data_ingestor
from app import webserver

# Strategy interface
JobRoutine = Callable[[dict], None]

class Job:
    def __init__(self, job_id, job_routine: JobRoutine, request_data):

        self.job_id = job_id
        print('Created job with id ', job_id)
        self.job_routine = job_routine
        self.request_data = request_data
        self.result = None

    def execute(self):
        # Execute the job using the assigned routine
        self.result = self.job_routine(self.job_id, self.request_data)
        

    def save_result(self):
        # Implement saving result to disk
        print(f"Saving result for {self.job_id}: {self.result}")

    def get_result(self):
        # Return the result
        return self.result

def states_mean(job_id, request_data):
    data = webserver.data_ingestor.get_data()

    results = calculate_arithmetic_mean(request_data, data)
    results = dict(sorted(results.items(), key=lambda item: item[1]))

    # print to results/<job_id>
    with open(f"results/{job_id}", "w") as f:
        print('Writing the file with job_id: ', job_id)
        # print('Results are: ', results)
        f.write(json.dumps(results))

    return results

def state_mean(job_id, request_data):
    results = 0
    entries = 0
    data = webserver.data_ingestor.get_data()
    target_state = request_data['state']

    # calculate arithmetic mean for a single state
    for field in data:
        if 2011 <= int(field['YearStart']) and int(field['YearEnd']) <= 2022 and field['LocationDesc'] == target_state and field['Question'] == request_data['question']:
            results += float(field['Data_Value'])
            entries += 1

    results /= entries

    formatted_results = {target_state: results}

    with open(f"results/{job_id}", "w") as f:
        f.write(json.dumps(formatted_results))

    return results


def best5(job_id, request_data):
    data = webserver.data_ingestor.get_data()

    results = calculate_arithmetic_mean(request_data, data)

    # get only the top 5
    results = dict(sorted(results.items(), key=lambda item: item[1], reverse=True)[:5])

    with open(f"results/{job_id}", "w") as f:
        f.write(json.dumps(results))

    return results

def worst5(job_id, request_data):
    data = webserver.data_ingestor.get_data()

    results = calculate_arithmetic_mean(request_data, data)

    # get only the bottom 5
    results = dict(sorted(results.items(), key=lambda item: item[1])[:5])

    with open(f"results/{job_id}", "w") as f:
        f.write(json.dumps(results))

def global_mean(job_id, request_data):
    result = 0
    entries = 0
    data = webserver.data_ingestor.get_data()
    question = request_data['question']

    # calculate arithmetic mean for all the entries that match the question
    for field in data:
        if 2011 <= int(field['YearStart']) and int(field['YearEnd']) <= 2022 and field['Question'] == question:
            result += float(field['Data_Value'])
            entries += 1

    result /= entries

    with open(f"results/{job_id}", "w") as f:
        f.write(json.dumps(result))

    return result

def diff_from_mean(job_id, request_data):
    results = {}

    states_results = states_mean(job_id, request_data)
    global_mean_val = global_mean(job_id, request_data)

    for state, value in states_results.items():
        results[state] = global_mean_val - value

    with open(f"results/{job_id}", "w") as f:
        print('Succesfully wrote to file')
        f.write(json.dumps(results))

    return results

def state_diff_from_mean(job_id, request_data):
    global_mean_val = global_mean(job_id, request_data)
    state_mean_val = state_mean(job_id, request_data)

    return global_mean_val - state_mean_val

def mean_by_category(job_id, request_data):
    results = {}
    entries = {}
    data = webserver.data_ingestor.get_data()

    for field in data:
        stratification1 = field['Stratification1']
        stratificationCategory1 = field['StratificationCategory1']
        state = field['LocationDesc']

        if field['Question'] == request_data['question']:
            # data_tuple = (state, stratification1, stratificationCategory1)
            # make a string hash out of the 3 values by concatenating them
            data_tuple = state + stratification1 + stratificationCategory1
            if data_tuple not in results:
                results[data_tuple] = float(field['Data_Value'])
                entries[data_tuple] = 1
            else:
                results[data_tuple] += float(field['Data_Value'])
                entries[data_tuple] += 1

    for key in results:
        results[key] /= entries[key]

    with open(f"results/{job_id}", "w") as f:
        f.write(json.dumps(results))

    return results

def state_mean_by_category(job_id, request_data):
    results = {}
    entries = {}
    data = webserver.data_ingestor.get_data()
    target_state = request_data['state']
    question = request_data['question']

    for field in data:
        stratification1 = field['Stratification1']
        stratificationCategory1 = field['StratificationCategory1']
        state = field['LocationDesc']

        if field['Question'] == question and state == target_state:
            # data_tuple = (state, stratification1, stratificationCategory1)
            # make a string hash out of the 3 values by concatenating them
            data_tuple = stratification1 + stratificationCategory1
            if data_tuple not in results:
                results[data_tuple] = float(field['Data_Value'])
                entries[data_tuple] = 1
            else:
                results[data_tuple] += float(field['Data_Value'])
                entries[data_tuple] += 1

    for key in results:
        results[key] /= entries[key]

    with open(f"results/{job_id}", "w") as f:
        f.write(json.dumps(results))

    return results

def calculate_arithmetic_mean(request_data, data):
    results = {}
    entries = {}

    for field in data:
        if 2011 <= int(field['YearStart']) and int(field['YearEnd']) <= 2022 and field['Question'] == request_data['question']:
            location_desc = field['LocationDesc']
            if location_desc not in results:
                results[location_desc] = float(field['Data_Value'])
                entries[location_desc] = 1
            else:
                results[location_desc] += float(field['Data_Value'])
                entries[location_desc] += 1

    for key in results:
        results[key] /= entries[key]

    return results

