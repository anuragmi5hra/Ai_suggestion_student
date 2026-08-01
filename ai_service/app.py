from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route('/api/suggest', methods=['POST'])
def suggest():
    data = request.json or {}
    title = data.get('title','')
    topic = data.get('topic','')
    deadline = data.get('deadline','')
    # Basic heuristic suggestion generator
    try:
        dl = datetime.fromisoformat(deadline) if deadline else None
    except:
        dl = None
    suggestion = f"Study '{topic or title}' consistently.\n"
    if dl:
        days_left = max(1, (dl - datetime.now()).days)
        suggestion += f"Break material into {min(7, days_left)} chunks and study {max(1, round( (2 if days_left<7 else 1) ))} hour(s) per day.\n"
    suggestion += "Prioritize active recall and spaced repetition.\n" 
    return jsonify({ 'suggestion': suggestion })

if __name__ == '__main__':
    app.run(port=8000)
