import json
import pymysql
from app import app#importing  flask from app.py
from db_config import mysql#importing our db connection from db_config.py
from flask import jsonify
from flask import flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

#inserting the student data		
@app.route('/insert', methods=['POST'])
def add_user():
	try:
		_json = request.json
		# return _json;
		_firstname = _json['firstname']
		_lastname = _json['lastname']
		_regno = _json['regno']
		_batch_from = _json['batch_from']
		_batch_to = _json['batch_to']
		_email =  _json['mail_id']
		_contact = _json['phonenumber']
		_created_at = str(datetime.now())
		_updated_at = str(datetime.now())
		
		
		# validate the received values
		if _firstname and _lastname and _regno and _batch_from and _batch_to and  _email and _contact and  request.method == 'POST':
			# save edits
			sql = "INSERT INTO users(firstname, lastname, regno, batch_from, batch_to, mail_id, contact, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"		
			data = (_firstname, _lastname, _regno, _batch_from,_batch_to, _email, _contact, _created_at, _updated_at)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()
			resp = 'Student added successfully!'
			statusCode = 200
			return json.dumps({'success':True, 'message': resp, 'statusCode': statusCode}), statusCode, {'ContentType':'application/json'}
		else:
			return not_found()
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

#admin login
@app.route('/admin', methods= ['POST'])
def login():
	try:
		_json = request.json
		_username = _json['username']
		_password = _json['password']
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute('SELECT * FROM admin WHERE user_name= %s AND pass_word= %s',(_username, _password))
		data = cursor.fetchone()

		if data is None:
			# return 'Incorrect Username / Password'
			resp = 'Bad Request - invalid Username or Password'
			statusCode = 400
			return json.dumps({'success':True, 'message': resp, 'statusCode': statusCode}), statusCode, {'ContentType':'application/json'}
		else:
			return json.dumps({'success':True}), 200, {'ContentType':'application/json'}
	
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()


#Getting all datas as a dict format		
@app.route('/users')
def users():
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM users")#selecting all datas from db
		rows = cursor.fetchall()
		resp = jsonify(rows)
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

#Getting specific data from db	
@app.route('/user/<int:id>')
def user(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM users WHERE id=%s", id)
		row = cursor.fetchone()
		resp = jsonify(row)
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

#Viewing the created at and updated at
@app.route('/view')
def view_times(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT created_at, updated_at FROM users WHERE id=%s", id)
		rows = cursor.fetchone()
		resp = jsonify(rows)
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()


#updating a student details using his id
@app.route('/update', methods=['POST'])
def update_user():
	try:
		_json = request.json
		_id = _json['id']
		_firstname = _json['firstname']
		_lastname = _json['lastname']
		_regno = _json['regno']
		_batch_from = _json['batch_from']
		_batch_to = _json['batch_to']	
		_email = _json['mail_id']
		_contact = _json['phonenumber']
		_updated_at = str(datetime.now())
		# validate the received values
		if _firstname and _lastname and _regno and _batch_from and _batch_to and  _email and _contact and _id and request.method == 'POST':

			# save edits
			sql = "UPDATE users SET firstname=%s, lastname=%s, regno=%s, batch_from=%s, batch_to=%s, mail_id=%s, contact=%s, updated_at=%s WHERE id=%s"
			data = (_firstname, _lastname, _regno, _batch_from,_batch_to, _email, _contact, _updated_at, _id)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()
			resp = 'User updated successfully!'
			statusCode = 200
			return json.dumps({'success':True, 'message': resp, 'statusCode': statusCode}), statusCode, {'ContentType':'application/json'}
		else:
			return not_found()
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()



#deleting the data of specific student by his id.		
@app.route('/delete/<int:id>',methods= ['DELETE'])
def delete_user(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM users WHERE id=%s", (id,))
		conn.commit()
		resp = 'User deleted successfully!'
		statusCode = 200
		return json.dumps({'success':True, 'message': resp, 'statusCode': statusCode}), statusCode, {'ContentType':'application/json'}
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

#seach api for admin
@app.route('/search', methods= ['POST'])
def search():
	try:
		_json = request.json
		_search = _json['search']
		cursor = mysql.connect().cursor(pymysql.cursors.DictCursor)
		cursor.execute('SELECT * FROM users WHERE(id LIKE %s or firstname LIKE %s or lastname LIKE %s or regno LIKE %s )',(_search, _search, _search, _search))
		rows = cursor.fetchall()
		resp = jsonify(rows)
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close()

@app.route('/search_mess', methods= ['POST'])
def mess():
	try:
		_json = request.json
		_search_mess = _json['search']
		cursor = mysql.connect().cursor(pymysql.cursors.DictCursor)
		cursor.execute('SELECT * FROM contact WHERE(id LIKE %s or name LIKE %s)',(_search_mess, _search_mess))
		rows = cursor.fetchall()
		resp = jsonify(rows)
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close()




#contact page
@app.route('/contact', methods=['POST'])
def contact():
	try:
		_json = request.json
		name = _json['name']
		mail_id = _json['mail_id']
		message = _json['message']
		recieved_at = str(datetime.now())
		
		# validate the received values
		if name and mail_id and message and request.method == 'POST':
			# save edits
			sql = "INSERT INTO contact(name, mail_id, message, recieved_at) VALUES (%s, %s, %s, %s)"		
			data = (name, mail_id, message, recieved_at)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()
			resp = 'Thanks for your response!'
			statusCode = 200
			return json.dumps({'success':True, 'message': resp, 'statusCode': statusCode}), statusCode, {'ContentType':'application/json'}
		else:
			return not_found()
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
	
@app.route('/messages')
def message():
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM contact")#selecting all datas from db
		rows = cursor.fetchall()
		resp = jsonify(rows)
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()


		
@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp
		
if __name__ == "__main__":
    app.run()
 
       