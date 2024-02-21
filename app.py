from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
import secrets


app = Flask(__name__)
app.config['SECRET_KEY'] = 'hgh'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'HGH'


app.secret_key = 'c9a1f05b79f72bc1a7cee3a97bcdd1eb'

mysql = MySQL(app)
bcrypt = Bcrypt(app)



@app.route('/', methods=['GET', 'POST'])
def main():
     return render_template('index.html')

@app.route('/farmer_signup', methods=['GET', 'POST'])
def farmer_signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        phone_number = request.form['Phone_number']
        email = request.form['email']

        if len(password)<8:
            flash('password must be 8 character long!')
        elif password != confirm_password:
            flash('password must match confirm password!')
        else:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

            cursor = mysql.connection.cursor()
            cursor.execute("INSERT INTO seller (username, password, phone_number, email) VALUES (%s, %s, %s, %s)",
                           (username, hashed_password, phone_number, email))
            mysql.connection.commit()
            cursor.close()

            flash('Account created successfully!', 'success')
            return redirect(url_for('farmer_login'))

    return render_template('farmer_signup.html')

 
@app.route('/farmer_login', methods=['GET', 'POST'])
def farmer_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM seller WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()

        if user and bcrypt.check_password_hash(user['password'], password):
            
            flash('Login successful!', 'success')
            # session variable
            return 'FARMER_HOME'
        else:
            flash('Login failed. Check your username and password.', 'danger')

    return render_template('farmer_login.html')


@app.route('/buyer_signup', methods=['GET', 'POST'])
def buyer_signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['confirm_password']
        phone_number = request.form['phone']
        email = request.form['email']

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO consumers (username, password, phone_number, email) VALUES (%s, %s, %s, %s)",
                       (username, hashed_password, phone_number, email))
        mysql.connection.commit()
        cursor.close()

        flash('Account created successfully!', 'success')
        return redirect(url_for('buyer_login'))

    return render_template('buyer_signup.html')

@app.route('/buyer_login', methods=['GET', 'POST'])
def buyer_login():
    if request.method == 'POST':
        username = request.form['buyer_username']
        password = request.form['password']

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM consumers WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()

        if user and bcrypt.check_password_hash(user[2], password):

            session['username'] = username
            
            flash('Login successful!', 'success')
            # session variable
            return redirect(url_for('buyer_home'))
        else:
            flash('Login failed. Check your username and password.', 'danger')


    return render_template('buyer_login.html')


@app.route('/buyer_home')
def buyer_home():

    if 'username' in session:
        return render_template('buyer_home.html')

    else:
        return redirect(url_for('buyer_login'))



if __name__ == '__main__':
	app.run(debug=True)