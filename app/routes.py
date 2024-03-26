import logging
from app import webserver
from flask import request, jsonify
from app.job import Job
import os
import json

# Example endpoint definition
@webserver.route('/api/post_endpoint', methods=['POST'])
def post_endpoint():
    if request.method == 'POST':
        # Assuming the request contains JSON data
        data = request.json
        print(f"got data in post {data}")

        # Process the received data
        # For demonstration purposes, just echoing back the received data
        response = {"message": "Received data successfully", "data": data}

        # Sending back a JSON response
        return jsonify(response)
    else:
        # Method Not Allowed
        return jsonify({"error": "Method not allowed"}), 405

@webserver.route('/api/get_results/<job_id>', methods=['GET'])
def get_response(job_id):
    print(f"JobID is {job_id}")
    # TODO
    # Check if job_id is valid
    if job_id > webserver.job_counter or job_id < 1:
        logging.error(f"Invalid job_id {job_id}")
        return jsonify({"status": "error", "reason": "Invalid job_id"})

    # check if the job_id is still running
    if job_id in webserver.tasks_runner.waiting_jobs:
        logging.info(f"Job {job_id} is still running")
        return jsonify({'status': 'running'})
    
    if job_id in webserver.tasks_runner.job_results:
        logging.info(f"Job {job_id} is done")
        return jsonify({'status': 'done', 'data': webserver.tasks_runner.job_results[job_id]})
    
    logging.error(f"Job {job_id} is not in the queue or results")

    return jsonify({"status": "error", "reason": "Job has valid job_id but is not in the queue or results."})


@webserver.route('/api/states_mean', methods=['POST'])
def states_mean_request():
    # Get request data
    data = request.json
    # TODO
    # Register job. Don't wait for task to finish
    new_job = Job(webserver.job_counter, "states_mean", data)
    webserver.tasks_runner.waiting_jobs.put(new_job)
    # Increment job_id counter
    webserver.job_counter += 1

    logging.info(f"Job {new_job.job_id} was added to the queue")    
    
    # Return associated job_id
    return jsonify({"job_id": new_job.job_id})

@webserver.route('/api/state_mean', methods=['POST'])
def state_mean_request():
    # TODO
    # Get request data
    data = request.json
    # Register job. Don't wait for task to finish
    new_job = Job(webserver.job_counter, "state_mean", data)
    webserver.tasks_runner.waiting_jobs.put(new_job)
    # Increment job_id counter
    webserver.job_counter += 1

    logging.info(f"Job {new_job.job_id} was added to the queue")
    # Return associated job_id
    return jsonify({"job_id": new_job.job_id})


@webserver.route('/api/best5', methods=['POST'])
def best5_request():
    # TODO
    # Get request data
    data = request.json
    # Register job. Don't wait for task to finish
    new_job = Job(webserver.job_counter, "best5", data)
    webserver.tasks_runner.waiting_jobs.put(new_job)
    # Increment job_id counter
    webserver.job_counter += 1
    # Return associated job_id
    return jsonify({"job_id": new_job.job_id})

@webserver.route('/api/worst5', methods=['POST'])
def worst5_request():
    # TODO
    # Get request data
    data = request.json
    # Register job. Don't wait for task to finish
    new_job = Job(webserver.job_counter, "worst5", data)
    webserver.tasks_runner.waiting_jobs.put(new_job)
    # Increment job_id counter
    webserver.job_counter += 1
    # Return associated job_id

    return jsonify({"job_id": new_job.job_id})

@webserver.route('/api/global_mean', methods=['POST'])
def global_mean_request():
    # TODO
    # Get request data
    data = request.json
    # Register job. Don't wait for task to finish
    new_job = Job(webserver.job_counter, "global_mean", data)
    webserver.tasks_runner.waiting_jobs.put(new_job)
    # Increment job_id counter
    webserver.job_counter += 1
    # Return associated job_id

    return jsonify({"job_id": new_job.job_id})

@webserver.route('/api/diff_from_mean', methods=['POST'])
def diff_from_mean_request():
    # TODO
    # Get request data
    data = request.json
    # Register job. Don't wait for task to finish
    new_job = Job(webserver.job_counter, "diff_from_mean", data)
    webserver.tasks_runner.waiting_jobs.put(new_job)
    # Increment job_id counter
    webserver.job_counter += 1
    # Return associated job_id
    
    return jsonify({"job_id": new_job.job_id})

@webserver.route('/api/state_diff_from_mean', methods=['POST'])
def state_diff_from_mean_request():
    # TODO
    # Get request data
    data = request.json
    # Register job. Don't wait for task to finish
    new_job = Job(webserver.job_counter, "state_diff_from_mean", data)
    webserver.tasks_runner.waiting_jobs.put(new_job)
    # Increment job_id counter
    webserver.job_counter += 1
    # Return associated job_id

    return jsonify({"job_id": new_job.job_id})

@webserver.route('/api/mean_by_category', methods=['POST'])
def mean_by_category_request():
    # TODO
    # Get request data
    data = request.json
    # Register job. Don't wait for task to finish
    new_job = Job(webserver.job_counter, "mean_by_category", data)
    # Increment job_id counter
    webserver.job_counter += 1
    # Return associated job_id

    return jsonify({"job_id": new_job.job_id})

@webserver.route('/api/state_mean_by_category', methods=['POST'])
def state_mean_by_category_request():
    # TODO
    # Get request data
    data = request.json
    # Register job. Don't wait for task to finish
    new_job = Job(webserver.job_counter, "state_mean_by_category", data)
    webserver.tasks_runner.waiting_jobs.put(new_job)
    # Increment job_id counter
    webserver.job_counter += 1
    # Return associated job_id

    return jsonify({"job_id": new_job.job_id})

# You can check localhost in your browser to see what this displays
@webserver.route('/')
@webserver.route('/index')
def index():
    routes = get_defined_routes()
    msg = f"Hello, World!\n Interact with the webserver using one of the defined routes:\n"

    # Display each route as a separate HTML <p> tag
    paragraphs = ""
    for route in routes:
        paragraphs += f"<p>{route}</p>"

    msg += paragraphs
    return msg

def get_defined_routes():
    routes = []
    for rule in webserver.url_map.iter_rules():
        methods = ', '.join(rule.methods)
        routes.append(f"Endpoint: \"{rule}\" Methods: \"{methods}\"")
    return routes
