"""
    This contains the API endpoints that will be used to interact with the webserver.
"""
import os
import json
import logging
from flask import request, jsonify
from app.job import Job, states_mean, state_mean, best5, worst5, global_mean
from app.job import diff_from_mean, state_diff_from_mean, mean_by_category, state_mean_by_category
from app import webserver

# Example endpoint definition
@webserver.route('/api/post_endpoint', methods=['POST'])
def post_endpoint():
    logging.info("Received POST request at /api/post_endpoint")

    if request.method == 'POST':
        data = request.json
        # Process the received data
        # For demonstration purposes, just echoing back the received data
        response = {"message": "Received data successfully", "data": data}

        # Sending back a JSON response
        return jsonify(response)

    return jsonify({"error": "Method not allowed"}), 405

@webserver.route('/api/get_results/<job_id>', methods=['GET'])
def get_response(job_id):
    logging.info("Received GET request at /api/get_results/%s", job_id)

    # Check if job_id is valid
    if int(job_id) > int(webserver.job_counter) or int(job_id) < 1:
        logging.error("Invalid job_id: %s", job_id)
        return {"status": "error", "reason": "Invalid job_id"}

    # Check if the job_id is in waiting queue
    is_in_waiting_queue = False
    waiting_queue = webserver.tasks_runner.get_waiting_jobs()
    for job in waiting_queue.queue:
        if job.job_id == int(job_id):
            is_in_waiting_queue = True
            break

    # Check if the job_id is still running
    if is_in_waiting_queue:
        logging.info("Job %s is still running", job_id)
        return {"status": "running"}

    # Look in results dir to see if the job_id is there. if yes, return the results
    if os.path.exists(f"results/{job_id}"):
        with open(f"results/{job_id}", "r") as f:
            results = f.read()
            logging.info("Job %s is done and results are (first 100 chars): %s",
                job_id, results[:100])

            if results == '':
                return {"status": "done", "data": {}}

            return {"status": "done", "data": json.loads(results)}

    logging.error("Job %s is not in the queue or results", job_id)

    return {"status": "error", "reason": "Job has valid job_id but is not in the queue or results."}

@webserver.route('/api/jobs', methods=['GET'])
def get_jobs_info():
    logging.info("Received GET request at /api/jobs")
    result = {}

    waiting_jobs = webserver.tasks_runner.get_waiting_jobs()
    for job in waiting_jobs.queue:
        result[job.job_id] = "waiting"

    # Look in results dir to see jobs that are done
    for file in os.listdir("results"):
        job_id = file
        if job_id not in result:
            result[job_id] = "done"

    return jsonify(result)

@webserver.route('/api/num_jobs', methods=['GET'])
def get_num_jobs():
    logging.info("Received GET request at /api/num_jobs")

    if webserver.tasks_runner.is_shutdown():
        return jsonify({"num_jobs": 0})

    waiting_jobs = webserver.tasks_runner.get_waiting_jobs()
    num_jobs = len(waiting_jobs.queue)

    return jsonify({"num_jobs": num_jobs})

@webserver.route('/api/states_mean', methods=['POST'])
def states_mean_request():
    logging.info("Received POST request at /api/states_mean")
    data = request.json

    new_job = Job(webserver.job_counter, states_mean, data)
    webserver.tasks_runner.waiting_jobs.put(new_job)
    logging.info("Job %s was added to the queue", new_job.job_id)

    webserver.job_counter += 1

    return jsonify({"job_id": new_job.job_id})

@webserver.route('/api/state_mean', methods=['POST'])
def state_mean_request():
    logging.info("Received POST request at /api/state_mean")
    data = request.json

    new_job = Job(webserver.job_counter, state_mean, data)
    webserver.tasks_runner.waiting_jobs.put(new_job)
    logging.info("Job %s was added to the queue", new_job.job_id)

    webserver.job_counter += 1

    return jsonify({"job_id": new_job.job_id})

@webserver.route('/api/best5', methods=['POST'])
def best5_request():
    logging.info("Received POST request at /api/best5")
    data = request.json

    new_job = Job(webserver.job_counter, best5, data)
    webserver.tasks_runner.waiting_jobs.put(new_job)
    logging.info("Job %s was added to the queue", new_job.job_id)

    webserver.job_counter += 1

    return jsonify({"job_id": new_job.job_id})

@webserver.route('/api/worst5', methods=['POST'])
def worst5_request():
    logging.info("Received POST request at /api/worst5")
    data = request.json

    new_job = Job(webserver.job_counter, worst5, data)
    webserver.tasks_runner.waiting_jobs.put(new_job)
    logging.info("Job %s was added to the queue", new_job.job_id)

    webserver.job_counter += 1

    return jsonify({"job_id": new_job.job_id})

@webserver.route('/api/global_mean', methods=['POST'])
def global_mean_request():
    logging.info("Received POST request at /api/global_mean")
    data = request.json

    new_job = Job(webserver.job_counter, global_mean, data)
    webserver.tasks_runner.waiting_jobs.put(new_job)
    logging.info("Job %s was added to the queue", new_job.job_id)

    webserver.job_counter += 1

    return jsonify({"job_id": new_job.job_id})

@webserver.route('/api/diff_from_mean', methods=['POST'])
def diff_from_mean_request():
    logging.info("Received POST request at /api/diff_from_mean")
    data = request.json

    new_job = Job(webserver.job_counter, diff_from_mean, data)
    webserver.tasks_runner.waiting_jobs.put(new_job)
    logging.info("Job %s was added to the queue", new_job.job_id)

    webserver.job_counter += 1

    return jsonify({"job_id": new_job.job_id})

@webserver.route('/api/state_diff_from_mean', methods=['POST'])
def state_diff_from_mean_request():
    logging.info("Received POST request at /api/state_diff_from_mean")
    data = request.json

    new_job = Job(webserver.job_counter, state_diff_from_mean, data)
    webserver.tasks_runner.waiting_jobs.put(new_job)
    logging.info("Job %s was added to the queue", new_job.job_id)
    webserver.job_counter += 1

    return jsonify({"job_id": new_job.job_id})

@webserver.route('/api/mean_by_category', methods=['POST'])
def mean_by_category_request():
    logging.info("Received POST request at /api/mean_by_category")
    data = request.json

    new_job = Job(webserver.job_counter, mean_by_category, data)
    webserver.tasks_runner.waiting_jobs.put(new_job)
    logging.info("Job %s was added to the queue", new_job.job_id)

    webserver.job_counter += 1

    return jsonify({"job_id": new_job.job_id})

@webserver.route('/api/state_mean_by_category', methods=['POST'])
def state_mean_by_category_request():
    logging.info("Received POST request at /api/state_mean_by_category")
    data = request.json

    new_job = Job(webserver.job_counter, state_mean_by_category, data)
    webserver.tasks_runner.waiting_jobs.put(new_job)
    logging.info("Job %s was added to the queue", new_job.job_id)

    webserver.job_counter += 1

    return jsonify({"job_id": new_job.job_id})

# You can check localhost in your browser to see what this displays
@webserver.route('/')
@webserver.route('/index')
def index():
    logging.info("Received GET request at / or /index")

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

@webserver.route('/api/graceful_shutdown', methods=['GET'])
def handle_shutdown():
    logging.info("Received GET request at /api/graceful_shutdown")

    if webserver.tasks_runner is not None:
        webserver.tasks_runner.set_shutdown_event()
        return jsonify({"status": "shutting down"}), 200

    return jsonify({"error": "ThreadPool not active"}), 400
