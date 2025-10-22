from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, date, timedelta
import logging

# Set up basic logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
CORS(app) # Ensures CORS is handled for all routes

@app.route('/api/suggest', methods=['POST'])
def suggest():
    try:
        data = request.json or {}
        title = data.get('title', '')
        topic = data.get('topic', '')
        deadline_str = data.get('deadline', '')
        
        # --- DEBUGGING AND FIX FOR DEADLINE PARSING ---
        dl_date = None
        if deadline_str:
            try:
                # Flask request payload often sends dates in 'YYYY-MM-DD' format from forms/JSON
                # datetime.fromisoformat is robust but we'll try to handle common formats
                
                # Check if the string contains only the date part
                if len(deadline_str) == 10:
                    dl_date = datetime.strptime(deadline_str, '%Y-%m-%d').date()
                else:
                    # Try to parse the full ISO format with time/timezone if available
                    dl_date = datetime.fromisoformat(deadline_str).date()
            except ValueError as e:
                # Log the error to the console (important for debugging 500 errors)
                logging.error(f"Failed to parse deadline '{deadline_str}': {e}")
                # We can choose to return an error or continue with dl_date = None
                # Let's proceed with None for robustness
                dl_date = None

        suggestion = f"Study '{topic or title}' consistently.\n"
        
        if dl_date:
            # Calculate days left using date objects to avoid time/timezone issues
            today = date.today()
            days_left = max(1, (dl_date - today).days) 
            
            # Heuristic logic improved slightly
            study_chunks = min(7, days_left)
            hours_per_day = max(1, round(days_left / study_chunks))
            
            suggestion += f"Break material into {study_chunks} chunks and study {hours_per_day} hour(s) per day.\n"
        
        suggestion += "Prioritize active recall and spaced repetition.\n" 
        return jsonify({ 'suggestion': suggestion })
        
    except Exception as e:
        # Catch any other unexpected exceptions and log them
        logging.error(f"Unhandled exception in /api/suggest: {e}")
        # Return a JSON error response instead of an HTML 500 page
        return jsonify({'error': 'Internal Server Error during suggestion generation'}), 500

if __name__ == '__main__':
    # Setting use_reloader=False prevents the app from running twice if it's imported
    app.run(port=8000, debug=False, use_reloader=False)