from typing import Callable
from flask import jsonify
from app import data_ingestor

# Strategy interface
JobRoutine = Callable[[dict], None]

def states_mean(job_id, request_data):
    results = {}
    entries = {}
    data = data_ingestor.get_data()

    calculate_arithmetic_mean(request_data, results, entries, data)

    results['LocationDesc'] /= entries['LocationDesc']
    results = dict(sorted(results.items(), key=lambda item: item[1]))

    # print to results/<job_id>
    with open(f"results/{job_id}", "w") as f:
        f.write(jsonify(results))

    return results

def state_mean(job_id, request_data):
    results = 0
    entries = 0
    data = data_ingestor.get_data()
    target_state = request_data['state']

    # calculate arithmetic mean for a single state
    for field in data:
        if 2011 <= field['YearStart'] and field['YearEnd'] <= 2022 and field['LocationDesc'] == target_state and field['Question'] == request_data['question']:
            results += field['Data_Value']
            entries += 1

    results /= entries

    with open(f"results/{job_id}", "w") as f:
        f.write(jsonify(results))

    return results


def best5(job_id, request_data):
    results = {}
    entries = {}

    calculate_arithmetic_mean(request_data, results, entries)

    # get only the top 5
    results = dict(sorted(results.items(), key=lambda item: item[1], reverse=True)[:5])

    results = jsonify(results)

    with open(f"results/{job_id}", "w") as f:
        f.write(results)

def worst5(job_id, request_data):
    results = {}
    entries = {}

    calculate_arithmetic_mean(request_data, results, entries)

    # get only the bottom 5
    results = dict(sorted(results.items(), key=lambda item: item[1])[:5])
    results = jsonify(results)

    with open(f"results/{job_id}", "w") as f:
        f.write(results)

def global_mean(job_id, request_data):
    result = 0
    entries = 0
    data = data_ingestor.get_data()
    question = request_data['question']

    # calculate arithmetic mean for all the entries that match the question
    for field in data:
        if 2011 <= field['YearStart'] and field['YearEnd'] <= 2022 and field['Question'] == question:
            result += field['Data_Value']
            entries += 1

    result /= entries

    with open(f"results/{job_id}", "w") as f:
        f.write(jsonify(result))

    return result

def diff_from_mean(job_id, request_data):
    results = {}

    states_results = states_mean(job_id, request_data)
    global_mean = global_mean(job_id, request_data)

    for state, value in states_results.items():
        results[state] = global_mean - value

    with open(f"results/{job_id}", "w") as f:
        f.write(jsonify(results))

    return results

def state_diff_from_mean(job_id, request_data):
    global_mean = global_mean(job_id, request_data)
    state_mean = state_mean(job_id, request_data)

    return global_mean - state_mean

def mean_by_category(job_id, request_data):
    results = {}
    entries = {}
    data = data_ingestor.get_data()

    for field in data:
        stratification1 = field['Stratification1']
        stratificationCategory1 = field['StratificationCategory1']
        state = field['LocationDesc']

        if field['Question'] == request_data['question']:
            data_tuple = (state, stratification1, stratificationCategory1)
            if data_tuple not in results:
                results[data_tuple] = field['Data_Value']
                entries[data_tuple] = 1
            else:
                results[data_tuple] += field['Data_Value']
                entries[data_tuple] += 1

    for key in results:
        results[key] /= entries[key]

    with open(f"results/{job_id}", "w") as f:
        f.write(jsonify(results))

    return results

def state_mean_by_category(job_id, request_data):
    results = {}
    entries = {}
    data = data_ingestor.get_data()
    target_state = request_data['state']
    question = request_data['question']

    for field in data:
        stratification1 = field['Stratification1']
        stratificationCategory1 = field['StratificationCategory1']
        state = field['LocationDesc']

        if field['Question'] == question and state == target_state:
            data_tuple = (state, stratification1, stratificationCategory1)
            if data_tuple not in results:
                results[data_tuple] = field['Data_Value']
                entries[data_tuple] = 1
            else:
                results[data_tuple] += field['Data_Value']
                entries[data_tuple] += 1

    for key in results:
        results[key] /= entries[key]

    with open(f"results/{job_id}", "w") as f:
        f.write(jsonify(results))

    return results
     



def calculate_arithmetic_mean(request_data, results, entries, data):
    for field in data:
        if 2011 <= field['YearStart'] and field['YearEnd'] <= 2022 and field['Question'] == request_data['question']:
            location_desc = field['LocationDesc']
            if location_desc not in results:
                results[location_desc] = field['Data_Value']
                entries[location_desc] = 1
            else:
                results[location_desc] += field['Data_Value']
                entries[location_desc] += 1


class Job:
    def __init__(self, job_id, job_routine: JobRoutine, request_data):
        self.job_id = job_id
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
    

