# venv\Scripts\activate
from flask import Flask, request

from pymongo import MongoClient
import certifi

from bson.json_util import dumps
from bson.objectid import ObjectId

app = Flask(__name__)

CONN_STRING = 'mongodb+srv://QWERTY:QWERTY@cluster0.usc1l.mongodb.net/rbs?retryWrites=true&w=majority'

client = MongoClient(CONN_STRING, tlsCAFile=certifi.where())

db = client['rbs']

tests_collection = db['test']

'''
Route       	Method  	Description
/tests 			GET    		Get all tests
/tests 			POST   		Create a test
/tests/id 		GET    		Get test of specific id
/tests/id   	PUT    		Update test of specific id
/tests/id   	DELETE 		Delete test of a specific id
'''

@app.route('/tests', methods = ['GET','POST'])
def tests():
	method = request.method
	if(method=='GET'):
		tests = tests_collection.find()
		return dumps(list(tests))
	else:
		test_data = request.get_json(force=True)
		tests_collection.insert_one(test_data)
		return dumps({"status":"Document Created"})


@app.route('/tests/<test_id>', methods = ['GET','PUT',"DELETE"])
def test(test_id):
	method = request.method
	test = tests_collection.find_one({'_id':ObjectId(test_id)})
	# test = tests_collection.find_one({'status':400})
	if(method=='GET'):
		return dumps(test)
	elif(method=="PUT"):
		new_data = request.get_json(force=True)
		tests_collection.update_one(test,{'$set':new_data})
		return dumps({"status":"Document Updated"})
	else:
		tests_collection.delete_one(test)
		return dumps({"status":"Document Deleted"})

if __name__ == "__main__":
	app.run(debug=True)