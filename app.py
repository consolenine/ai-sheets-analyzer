from flask import Flask, render_template, request, redirect, url_for, jsonify
import requests
from dotenv import load_dotenv
import os, base64

from asrplus import process_lang

load_dotenv()

app = Flask(__name__)

# Dummy admin credentials (replace with actual authentication mechanism)
admin_username = 'admin'
admin_password = 'password'

data = {
    'title': 'Welcome to My Website',
    'content': 'This is some dynamic content!',
}

# Route for the main webpage
@app.route('/')
def index():
    return render_template('index.html', data=data)

# Route for the admin login page
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == admin_username and password == admin_password:
            # Dummy authentication (replace with actual authentication mechanism)
            return redirect(url_for('admin_dashboard'))
        else:
            return 'Invalid credentials. Please try again.'
    return render_template('admin_login.html')

# Route for the admin dashboard (requires authentication)
@app.route('/admin/dashboard')
def admin_dashboard():
    # Dummy data for the admin dashboard (replace with actual admin data)
    admin_data = {
        'username': admin_username,
        'total_users': 100,
        'total_orders': 500,
    }
    return render_template('admin_dashboard.html', admin_data=admin_data)

@app.route('/process_input', methods=['POST'])
def process_input():
    response = process_lang(request)
    return jsonify(response)
    

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
