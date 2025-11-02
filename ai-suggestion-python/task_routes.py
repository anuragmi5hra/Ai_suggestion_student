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

@task_bp.route('/<int:task_id>/progress', methods=['PATCH'])
def update_progress(task_id):
    for task in TASKS:
        if task['_id'] == task_id:
            task['progress'] = task.get('progress', 0) + 10
            if task['progress'] > 100:
                task['progress'] = 100
            return jsonify({'success': True, 'task': task})
    return jsonify({'success': False, 'message': 'Task not found'}), 404


@task_bp.route('/<int:task_id>/done', methods=['PATCH'])
def mark_done(task_id):
    for task in TASKS:
        if task['_id'] == task_id:
            task['progress'] = 100
            return jsonify({'success': True, 'task': task})
    return jsonify({'success': False, 'message': 'Task not found'}), 404
