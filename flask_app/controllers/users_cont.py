from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user_mod import Users
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# Current_user = False, session = 0 
# is for showing/hiding the login/registration buttons. 
# If have a better solution feel free to use it, this was 
# easiest for me in the past but im open for suggestions.

# Home Page
@app.route('/')
def home():
    if 'user_id' in session:
        data = {
        'id': session['user_id']
        }
        one_user = Users.get_profile(data)
        return render_template('home.html', current_user = one_user)
    else:
        return render_template('home.html', current_user = False, session = 0)

# Register Page
@app.route('/register')
def create_user():
    if 'user_id' in session:
        data = {
        'id': session['user_id']
        }
        one_user = Users.get_profile(data)
        return render_template('register.html', current_user = one_user)
    else:
        return render_template('register.html', current_user = False, session = 0)

# Process Register, for registration form
@app.route('/process_user', methods=['POST'])
def process_user():
    if not Users.validate_register(request.form):
        return redirect('/register')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': pw_hash
    }
    user_id = Users.save_user(data)
    session['user_id'] = user_id
    return redirect('/')

# Login Page
@app.route('/login')
def login_page():
    if 'user_id' in session:
        data = {
        'id': session['user_id']
        }
        one_user = Users.get_profile(data)
        return render_template('home.html', current_user = one_user)
    else:
        return render_template('login.html', current_user = False, session = 0)

# Process Login, for login form
@app.route('/process_login', methods=["POST"])
def user_login():
    if not Users.validate_login(request.form):
        return redirect('/login')
    data = {'email': request.form['email']}
    user_with_email = Users.get_by_email(data)
    user_id = user_with_email.id
    if 'user_id' in session:
        return redirect(f'/profile/{user_id}')
    if user_with_email == False:
        flash("Invalid Email/Password.")
        return redirect('/')
    if not bcrypt.check_password_hash(user_with_email.password, request.form['password']):
        flash("Invalid Email/Password.")
        return redirect('/')
    session['user_id'] = user_with_email.id
    return redirect('/')

# Logout, for logout form/button
@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect('/')