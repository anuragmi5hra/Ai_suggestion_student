from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, date, timedelta
import logging
import os

# Set up basic logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
CORS(app)  # Ensures CORS is handled for all routes


@app.route('/api/suggest', methods=['POST'])
def suggest():
    try:
        data = request.json or {}
        title = data.get('title', '')
        topic = data.get('topic', '')
        deadline_str = data.get('deadline', '')
        
        dl_date = None
        if deadline_str:
            try:
                # Handle both YYYY-MM-DD and full ISO formats
                if len(deadline_str) == 10:
                    dl_date = datetime.strptime(deadline_str, '%Y-%m-%d').date()
                else:
                    dl_date = datetime.fromisoformat(deadline_str).date()
            except ValueError as e:
                logging.error(f"Failed to parse deadline '{deadline_str}': {e}")
                dl_date = None

        suggestion = f"Study '{topic or title}' consistently.\n"
        
        if dl_date:
            today = date.today()
            days_left = max(1, (dl_date - today).days)
            study_chunks = min(7, days_left)
            hours_per_day = max(1, round(days_left / study_chunks))
            suggestion += f"Break material into {study_chunks} parts and study {hours_per_day} hour(s) per day.\n"
        
        suggestion += "Prioritize active recall and spaced repetition.\n"
        return jsonify({'suggestion': suggestion})

    except Exception as e:
        logging.error(f"Unhandled exception in /api/suggest: {e}")
        return jsonify({'error': 'Internal Server Error during suggestion generation'}), 500


# ✅ This must be at the root indentation level, not inside another function!
@app.route('/')
def home():
    return "✅ AI Suggestion API is running successfully on Render!"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
