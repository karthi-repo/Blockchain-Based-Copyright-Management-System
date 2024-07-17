#!/usr/bin/env python
import os
import hashlib
from flask import Flask, request, render_template, jsonify, redirect, send_from_directory, make_response
from blockchain import Blockchain
import pickle
import requests

from pymongo import MongoClient

UPLOAD_FOLDER = 'uploads'
TMP_FOLDER = 'tmp'

app =  Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['TMP_FOLDER'] = TMP_FOLDER

# the node's copy of blockchain

blockchain = Blockchain()

if os.path.exists('./blockchain/chain.pkl'):
	with open('./blockchain/chain.pkl', 'rb') as input:
		blockchain.chain = pickle.load(input)

if not os.path.exists('./blockchain'):
	os.mkdir('blockchain')
if not os.path.exists('./uploads'):
	os.mkdir('uploads')
if not os.path.exists('./tmp'):
	os.mkdir('tmp')

# Connect to MongoDB
# client = MongoClient('mongodb://localhost:27017/')
# db = client['major']
# collection = db['project_01']

@app.route('/')
def index():
    return render_template('./login.html')
	# return render_template('./index.html')

@app.route('/upfile')
def upfile():
    return render_template('./index.html')

@app.route('/blockchain')
def blockchain_page():
    return render_template('./blockchain.html')

@app.route('/about')
def about_page():
    return render_template('./aboutus.html')

@app.route('/faq')
def faq_page():
    return render_template('./faq.html')

@app.route('/uploads/<path:filename>')
def custom_static(filename):
    print(filename)
    temp = filename.split('.')
    if len(temp) > 1:
        response = make_response(send_from_directory('./uploads/', temp[0]))
        response.headers['Content-Type'] = 'text/html'
        return response
    else:
        return send_from_directory('./uploads/', temp[0])

@app.route('/mine', methods=['GET'])
def mine_unconfirmed_transactions():
	result = blockchain.mine()
	response = {'block': result.__dict__}

	return jsonify(response), 200

@app.route('/chain', methods=['GET'])
def get_chain():
	chain_data = []
	for block in blockchain.chain:
		chain_data.append(block.__dict__)

	response = {'chain': chain_data}
	return jsonify(response), 200

@app.route('/upload', methods=['POST'])
def upload():
	global blockchain

	print(request)
	if 'contentFile' not in request.files:
		response = {'ok': False}
		return jsonify(response), 500
	file = request.files['contentFile']
	
	filename = hashlib.sha256(file.read()).hexdigest()
	file.seek(0) #reset read pointer

	action = request.form['action']

	if action == "lookup":
		#TODO search for exact and partial matches
		print('TODO lookup')
		file.save(os.path.join(app.config['TMP_FOLDER'], filename))
		lookup_media = {
            'genre': request.form['genre'],
            'media': filename,
        }
		result = blockchain.lookup(lookup_media)
		os.remove(os.path.join(app.config['TMP_FOLDER'], filename)) #remove uploaded file

		if result is None:
			response = {'unique': True}
			return jsonify(response), 200

		response = {'unique': False, 'block': result.__dict__, 'message': 'Similar Object Detected'}
		
		return jsonify(response), 200
	elif action == "publish":
		if os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
			print("Duplicate Detected")
			response = {'unique': False, 'message':'Duplicate Detected'}
		else:
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			#Create a new transaction
			filepath = 'uploads/' + filename

			author = request.form['author']
			title = request.form['title']
			pubkey = blockchain.upload_to_ipfs(filepath)
			ownerprivatekey = request.form['pubkey']
			genre = request.form['genre']
			original_filename = file.filename
			blockchain.new_transaction(title, original_filename, author, pubkey, genre, filename)
			
			result = blockchain.mine(ownerprivatekey, pubkey)
			print(f"result is:{result}")
			if result == None:
				print("FALSE")
				os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename)) #remove uploaded file
				response = {'unique': False, 'message':'Similar Object Detected, Input File Rejected'}
			else:
				print("TEST")
				# print(result)
				# print(blockchain.store_cid_on_ethereum(ownerprivatekey, pubkey))
				# blockchain.upload_to_ipfs(filepath)
				response = {'unique': True, 'block': result.__dict__}

		return jsonify(response), 200

# @app.route('/logindetails', methods=['POST'])
# def login():
# 	email_user = request.form['email_user']
# 	private_key_user = request.form['privatekey_user']

# 	document = collection.find_one({'email': email_user, 'prikey': private_key_user})

# 	if document is not None:
# 		return render_template('./index.html')
# 	else:
# 		error_message = "Incorrect credentials. Please try again."
# 		return render_template('./login.html', error_message=error_message)

@app.route('/logindetails', methods=['POST'])
def login():
	return render_template('./index.html')

@app.route('/signup_details', methods=['POST'])
def signup():
    # signup_name = request.form['signup_name']
    # signup_email = request.form['signup_email']
    # signup_pubkey = request.form['signup_pubkey']
    # signup_prikey = request.form['signup_prikey']
    # document = {
    #     'name': signup_name,
    #     'email': signup_email,
    #     'pubkey': signup_pubkey,
    #     'prikey': signup_prikey
    # }

    # collection.insert_one(document)

    return render_template('./index.html')  


app.run(debug=True, port=5008)
