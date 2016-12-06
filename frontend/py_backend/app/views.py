from app import app
from flask import jsonify, request
import json as simplejson
from Classifier import Classifier
from MessageDAO import MessageDAO

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

_CLASSIFIER = None

def classifier():
    global _CLASSIFIER
    if not _CLASSIFIER:
	_CLASSIFIER = Classifier()
    return _CLASSIFIER

def _helper(term):
    results = []
    c = classifier()
    message_dao = MessageDAO()
    messages = message_dao.retrieve_testing_messages(term)
    for message, sentiment in messages:
        tweet_classification = {'sentiment' : c.classify(message),'tweet' : message}
        results.append(tweet_classification)
    return results

@app.route('/api/search/<data>', methods=['GET'])
def get_sentiment(data):
    try:

	data = data.encode('ascii', 'ignore')
	data.replace('-', ' ')
	res = _helper(data)
	return jsonify(res)
    except Exception as e:
        raise
