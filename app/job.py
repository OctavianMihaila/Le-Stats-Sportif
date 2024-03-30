from typing import Callable
import json
from app import webserver

JobRoutine = Callable[[dict], None] 

class Job:
    def __init__(self, job_id, job_routine: JobRoutine, request_data):
        self.job_id = job_id
        self.job_routine = job_routine
        self.request_data = request_data
        self.result = None

    def execute(self):
        # Execute the job using the assigned routine
        self.result = self.job_routine(self.job_id, self.request_data)

        return self.result

def states_mean(job_id, request_data):
    data = webserver.data_ingestor.get_data()

    results = calculate_arithmetic_mean(request_data, data)
    # Sort the results by value in ascending order
    results = dict(sorted(results.items(), key=lambda item: item[1]))

    return results

def state_mean(job_id, request_data):
    results = 0
    entries = 0
    data = webserver.data_ingestor.get_data()
    target_state = request_data['state']

    # Calculate arithmetic mean for a single state
    for field in data:
        if (2011 <= int(field['YearStart']) and 
            int(field['YearEnd']) <= 2022 and 
            field['LocationDesc'] == target_state and 
            field['Question'] == request_data['question']):

            results += float(field['Data_Value'])
            entries += 1

    results /= entries
    formatted_results = {target_state: results}

    return formatted_results


def best5(job_id, request_data):
    data = webserver.data_ingestor.get_data()

    results = calculate_arithmetic_mean(request_data, data)
    sort_order = webserver.data_ingestor.get_sort_order(request_data['question'])

    if sort_order == 'asc':
        results = dict(sorted(results.items(), key=lambda item: item[1])[:5])
    else:
        results = dict(sorted(results.items(), key=lambda item: item[1], reverse=True)[:5])

    return results

def worst5(job_id, request_data):
    data = webserver.data_ingestor.get_data()

    results = calculate_arithmetic_mean(request_data, data)
    sort_order = webserver.data_ingestor.get_sort_order(request_data['question'])

    if sort_order == 'asc':
        results = dict(sorted(results.items(), key=lambda item: item[1], reverse=True)[:5])
    else:
        results = dict(sorted(results.items(), key=lambda item: item[1])[:5])

    return results

def global_mean(job_id, request_data):
    result = 0
    entries = 0
    data = webserver.data_ingestor.get_data()
    question = request_data['question']

    # Calculate arithmetic mean for all the entries that match the question
    for field in data:
        if (2011 <= int(field['YearStart']) and
            int(field['YearEnd']) <= 2022 and
            field['Question'] == question):

            result += float(field['Data_Value'])
            entries += 1

    result /= entries
    formatted_results = {'global_mean': result}

    return formatted_results

def diff_from_mean(job_id, request_data):
    results = {}

    states_results = states_mean(job_id, request_data)
    global_mean_val = global_mean(job_id, request_data)

    # Calculate the difference between the global mean and the mean of each state
    for state, value in states_results.items():
        results[state] = global_mean_val['global_mean'] - value

    return results

def state_diff_from_mean(job_id, request_data):
    global_mean_val = global_mean(job_id, request_data)
    state_mean_val = state_mean(job_id, request_data)

    result = global_mean_val['global_mean'] - state_mean_val[request_data['state']]
    formatted_results = {request_data['state']: result}

    return formatted_results

def mean_by_category(job_id, request_data):
    results = {}
    entries = {}
    data = webserver.data_ingestor.get_data()

    for field in data:
        stratification1 = field['Stratification1']
        stratificationCategory1 = field['StratificationCategory1']
        state = field['LocationDesc']

        if (field['Question'] == request_data['question'] 
            and stratificationCategory1 != '' and stratification1 != ''):
            # Using a string format like this one ('Alabama', 'Age (years)', '18 - 24') as key.
            key = '(\'' + state + '\', \'' + stratificationCategory1 + '\', \'' + stratification1 + '\')'
            if key not in results:
                results[key] = float(field['Data_Value'])
                entries[key] = 1
            else:
                results[key] += float(field['Data_Value'])
                entries[key] += 1

    for key in results:
        results[key] /= entries[key]

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
            # Using a string format like this one ('Age (years)', '18 - 24') as key.
            key = '(\'' + stratificationCategory1 + '\', \'' + stratification1 + '\')'
            if key not in results:
                results[key] = float(field['Data_Value'])
                entries[key] = 1
            else:
                results[key] += float(field['Data_Value'])
                entries[key] += 1

    for key in results:
        results[key] /= entries[key]

    formatted_results = {target_state: results}

    return formatted_results

# Helper function to calculate the arithmetic mean (2011 - 2022) for a given question
def calculate_arithmetic_mean(request_data, data):
    results = {}
    entries = {}

    for field in data:
        if (2011 <= int(field['YearStart']) 
            and int(field['YearEnd']) <= 2022 
            and field['Question'] == request_data['question']):
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

