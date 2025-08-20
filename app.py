from flask import Flask, request, jsonify, send_from_directory
import requests
import threading
import uuid
import time
import os

app = Flask(__name__, static_folder='static', static_url_path='')

GRAPH_API_URL = "https://graph.facebook.com/v17.0"
tasks = {}  # task_id -> {status, details, tokens, posts}

def react_task(task_id, tokens, post_ids, reaction_type):
    results = []
    print(f"[Task {task_id}] Starting reaction task with {len(tokens)} tokens and {len(post_ids)} posts.")
    for token in tokens:
        token = token.strip()
        print(f"[Task {task_id}] Using token: {token[:10]}...")
        for post_id in post_ids:
            post_id = post_id.strip()
            reaction_url = f"{GRAPH_API_URL}/{post_id}/reactions"
            params = {
                'type': reaction_type.upper(),
                'access_token': token
            }
            try:
                response = requests.post(reaction_url, params=params)
                print(f"[Task {task_id}] POST {reaction_url} with type={reaction_type.upper()}")
                print(f"[Task {task_id}] Response status: {response.status_code}")
                if response.status_code == 200:
                    results.append({'post_id': post_id, 'token': token[:5] + '...', 'status': 'Success'})
                    print(f"[Task {task_id}] Reacted successfully on post {post_id} with token {token[:5]}...")
                else:
                    error_json = response.json()
                    results.append({'post_id': post_id, 'token': token[:5] + '...', 'status': 'Failed', 'error': error_json})
                    print(f"[Task {task_id}] Failed on post {post_id} with token {token[:5]}... Error: {error_json}")
            except Exception as e:
                results.append({'post_id': post_id, 'token': token[:5] + '...', 'status': 'Failed', 'error': str(e)})
                print(f"[Task {task_id}] Exception on post {post_id} with token {token[:5]}... Exception: {e}")
            time.sleep(20)  # Delay between tokens

    tasks[task_id]['status'] = 'complete'
    tasks[task_id]['details'] = results
    print(f"[Task {task_id}] Completed reactions.")

@app.route('/react-multi', methods=['POST'])
def react_to_multiple_posts():
    data = request.form
    reaction_type = data.get('reaction_type')
    post_ids = data.get('post_ids')
    tokens_file = request.files.get('tokens_file')
    access_token = data.get('access_token')  # Single token option

    if not reaction_type or not post_ids:
        return jsonify({'error': 'Reaction type and post IDs required'}), 400

    post_id_list = [pid.strip() for pid in post_ids.replace(',', '\n').splitlines() if pid.strip()]

    token_list = []
    if tokens_file:
        content = tokens_file.read().decode('utf-8')
        token_list = [t.strip() for t in content.splitlines() if t.strip()]
    elif access_token:
        token_list = [access_token.strip()]
    else:
        return jsonify({'error': 'Access token or token file required'}), 400

    print(f"Received react-multi request with tokens: {len(token_list)} and posts: {len(post_id_list)}")

    task_id = str(uuid.uuid4())
    tasks[task_id] = {
        'status': 'running',
        'details': [],
        'tokens': len(token_list),
        'posts': len(post_id_list)
    }

    thread = threading.Thread(target=react_task, args=(task_id, token_list, post_id_list, reaction_type))
    thread.start()

    return jsonify({'task_id': task_id, 'message': 'Reaction task started'})

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

@app.route('/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    if task_id in tasks:
        del tasks[task_id]
        return jsonify({'message': f'Task {task_id} deleted'})
    else:
        return jsonify({'error': 'Task ID not found'}), 404

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=True)
