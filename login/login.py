from flask import Blueprint, render_template, request, redirect, flash, session
import mysql.connector
import bcrypt

login_app = Blueprint('login', __name__)

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "agrimart"
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

def validate_credentials(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    sql_query= "SELECT BuyerID, Password FROM Buyer WHERE Username = %s"
    cursor.execute(sql_query, (username,))
    user_data=cursor.fetchone()

    if user_data:
        user_id, hashed_password = user_data
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
            return user_id, 'buyer'
        
    sql_query = "SELECT SellerID, Password FROM Seller WHERE Username = %s"
    cursor.execute(sql_query, (username,))
    user_data = cursor.fetchone()

    cursor.close()
    conn.close()

    if user_data:
        user_id, hashed_password = user_data
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
            return user_id, 'seller'

    return None

@login_app.route('/login', methods=['GET', 'POST'])
def login():
    error_message = "" 
    if request.method=='POST':
        username = request.form['Username']
        password = request.form['Password']

        user_data = validate_credentials(username, password)
    
        if user_data:
            user_id, user_type = user_data
            session['user_id'] = user_id
            session['user_type']= user_type

            if user_type == 'buyer':
                return redirect('/homepage_buyer')
            elif user_type == 'seller':
                return redirect('/homepage_seller')
            else:
                error_message = "Invalid user type"

        error_message = "Invalid username or password. Please try again or sign up first."

    return render_template('login.html', error_message=error_message)

@login_app.route('/', methods=['POST'])
def index():
    return render_template('index.html')