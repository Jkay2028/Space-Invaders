from datetime import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

SERVICE_KEY_PATH = 'backend/firebase-service-key.json'

cred = credentials.Certificate(SERVICE_KEY_PATH)
firebase_admin.initialize_app(cred)

db = firestore.client()
collection = None


def join_leaderboard(game_id):
    global collection
    collection = db.collection('game_' + game_id)


def save_score(username, score):
    old_score = None
    old_score_doc = collection.document('user_' + username).get()
    if old_score_doc.exists:
        old_score = old_score_doc.to_dict().get('score', None)

    if old_score is not None and score < old_score:
        return

    now = datetime.now()
    collection.document('user_' + username).set({
        'username': username,
        'score': score,
        'when': now.strftime('%m-%d-%Y %I:%M %p')
    }, merge=True)


def get_scores():
    score_docs = collection.stream()
    scores = []

    for doc in score_docs:
        data = doc.to_dict()
        if data.get('score', None):
            scores.append(data)

    return sorted(scores, key=lambda score: score.get('score', 0), reverse=True)
