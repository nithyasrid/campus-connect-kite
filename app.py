from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_mysqldb import MySQL
from config import Config  # Import Config class
import MySQLdb.cursors
import bcrypt

app = Flask(__name__,static_folder='static')
app.config.from_object(Config) 
app.secret_key = 'your_secret_key'
 
# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'campus_connect'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

# 1. Signup Route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        user = cursor.fetchone()

        if user:
            flash('User already exists!', 'danger')
            return redirect(url_for('signup'))

        cursor.execute('INSERT INTO users (name, email, password) VALUES (%s, %s, %s)', (name, email, password))
        mysql.connection.commit()
        flash('Signup successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('signup.html')

# 2. Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'].encode('utf-8')

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        user = cursor.fetchone()

        if user and bcrypt.checkpw(password, user['password'].encode('utf-8')):
            session['loggedin'] = True
            session['user_id'] = user['id']
            session['name'] = user['name']
            return redirect(url_for('home'))
        else:
            flash('Incorrect login details', 'danger')

    return render_template('login.html')

# 3. Home Route
@app.route('/')
def home():
    if 'loggedin' in session:
        return render_template('index.html', name=session['name'])
    return redirect(url_for('login'))

# 4. Profile Route
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'loggedin' in session:
        if request.method == 'POST':
            bio = request.form['bio']
            profile_pic = request.form['profile_pic']
            
            cursor = mysql.connection.cursor()
            cursor.execute('INSERT INTO profiles (user_id, profile_pic, bio) VALUES (%s, %s, %s)',
                           (session['user_id'], profile_pic, bio))
            mysql.connection.commit()
            flash('Profile updated!', 'success')

        return render_template('profile.html')
    return redirect(url_for('login'))

# 5. Explore (Search and Follow Users)
@app.route('/explore', methods=['GET'])
def explore():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id != %s", (session['user_id'],))
        users = cursor.fetchall()
        return render_template('explore.html', users=users)
    return redirect(url_for('login'))

@app.route('/follow/<int:user_id>')
def follow(user_id):
    if 'loggedin' in session:
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO follows (follower_id, following_id) VALUES (%s, %s)',
                       (session['user_id'], user_id))
        mysql.connection.commit()
        return redirect(url_for('explore'))
    return redirect(url_for('login'))

# 6. Messages
@app.route('/chats', methods=['GET','POST'])
def chat():
    if 'loggedin' in session:
         if request.method == 'POST':
            receiver_id = request.form['receiver_id']
            message = request.form['message']
        
            cursor = mysql.connection.cursor()
            cursor.execute("INSERT INTO messages (sender_id, receiver_id, message) VALUES (%s, %s, %s)",
                        (session['user_id'], receiver_id, message))
            mysql.connection.commit()
            
            return jsonify({'status': 'Message sent'})
    return render_template('chats.html')  # Ensure chats.html exists in /templates
    return redirect(url_for('login'))

# 7. Anonymous Messages
@app.route('/anonymous', methods=['POST'])
def anonymous():
    if request.method == 'POST':
        message = request.form['message']
        
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO anonymous_messages (message) VALUES (%s)", (message,))
        mysql.connection.commit()
        return jsonify({'status': 'Message sent'})

# 8. Achievements
@app.route('/achievements', methods=['POST'])
def achievements():
    if 'loggedin' in session:
        certificate = request.form['certificate']
        skill = request.form['skill']
        
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO achievements (user_id, certificate, skill) VALUES (%s, %s, %s)",
                       (session['user_id'], certificate, skill))
        mysql.connection.commit()
        flash('Achievement added!', 'success')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, port=5500)
