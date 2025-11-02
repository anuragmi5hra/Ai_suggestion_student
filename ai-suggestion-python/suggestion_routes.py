from flask import Blueprint, request, jsonify
from datetime import datetime, date
import logging

suggest_bp = Blueprint('suggest_bp', __name__)

@suggest_bp.route('/suggest', methods=['POST'])
def suggest():
    try:
        data = request.json or {}
        title = data.get('title', '')
        topic = data.get('topic', '')
        deadline_str = data.get('deadline', '')

        dl_date = None
        if deadline_str:
            try:
                if len(deadline_str) == 10:
                    dl_date = datetime.strptime(deadline_str, '%Y-%m-%d').date()
                else:
                    dl_date = datetime.fromisoformat(deadline_str).date()
            except ValueError as e:
                logging.error(f"Failed to parse deadline '{deadline_str}': {e}")
                dl_date = None

        suggestion = f"📚 Study Plan for '{topic or title}':\n\n"
        suggestion += f"➡ Focus on '{topic or 'your topic'}' using active recall.\n"

        if dl_date:
            today = date.today()
            days_left = max(1, (dl_date - today).days)
            study_chunks = min(7, days_left)
            hours_per_day = max(1, round(days_left / study_chunks))
            suggestion += f"🗓 You have {days_left} days. Study {hours_per_day}h/day for {study_chunks} sessions.\n"

        suggestion += "\n💡 Use spaced repetition and short reviews every 2–3 days!"
        return jsonify({'suggestion': suggestion})

    except Exception as e:
        logging.error(f"Unhandled exception in /api/suggest: {e}")
        return jsonify({'error': 'Internal Server Error during suggestion generation'}), 500
