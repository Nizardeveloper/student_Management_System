import requests
from app import app
from db_config import mysql
from flask import render_template, request
from datetime import datetime

#routing main page
@app.route('/')
def frontend():
    return render_template('index.html')

#routing to admin login page for viewing student table
@app.route('/admin-login')
def login():
        return render_template('login.html')



#student table
@app.route('/admin')
def admin():
    api_url = requests.get("http://127.0.0.1:5000/users")
    student_data = api_url.json()
    return render_template('admin.html', student=student_data)

#student table
@app.route('/admin/search')
def search():
    searchValue = request.args.get('search', None)
    dictToSend = {'search': searchValue}
    res = requests.post('http://127.0.0.1:5000/search', json=dictToSend)
    dictFromServer = res.json()
    return render_template('admin.html', searched=dictFromServer)

#routing to login page 
@app.route('/admin-login-messages')
def message():
        return render_template('conlog.html')

@app.route('/messages')
def mess():
    #   return print("hello");
      api_url = requests.get('http://127.0.0.1:5000/messages')
      contact = api_url.json()
      return render_template('messages.html', messages=contact)

@app.route('/messages/search')
def search_mess():
    searchValue = request.args.get('search', None)
    dictToSend = {'search': searchValue}
    res = requests.post('http://127.0.0.1:5000/search_mess', json=dictToSend)
    dictFromServer = res.json()
    return render_template('messages.html', search_mess=dictFromServer)



@app.route('/delete-user')
def deluser():
      delUserId = request.args.get('delUserId')
      api_url = requests.delete('http://127.0.0.1:5000/delete/'+ delUserId)
      delUserData = api_url.json()
      return {"Response": delUserData};

if __name__ == "__main__":
    app.run()
    
