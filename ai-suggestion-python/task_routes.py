from flask import Blueprint, request, jsonify
from datetime import datetime

task_bp = Blueprint('task_bp', __name__)
TASKS = []

@task_bp.route('', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': TASKS})

@task_bp.route('/add', methods=['POST'])
def add_task():
    data = request.json
    new_task = {
        '_id': len(TASKS) + 1,
        'title': data.get('title', ''),
        'topic': data.get('topic', ''),
        'deadline': data.get('deadline', datetime.now().isoformat())
    }
    TASKS.append(new_task)
    return jsonify({'success': True, 'task': new_task})

@task_bp.route('/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global TASKS
    TASKS = [t for t in TASKS if t['_id'] != task_id]
    return jsonify({'success': True})
