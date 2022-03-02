from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.listing_mod import Listings
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
    if 'userId' in session:
        data = {
        'id': session['userId']
        }
        one_user = Users.get_profile(data)
        return render_template('dashboard.html', current_user = one_user)
    else:
        return render_template('login.html', current_user = False, session = 0)

# Process Register, for registration form
@app.route('/process_user', methods=['POST'])
def process_user():
    if not Users.validate_register(request.form):
        return redirect('/register')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'firstName': request.form['firstName'],
        'lastName': request.form['lastName'],
        'email': request.form['email'],
        'password': pw_hash
    }
    userId = Users.save_user(data)
    session['userId'] = userId
    return redirect('/')

# Process Login, for login form
@app.route('/process_login', methods=["POST"])
def user_login():
    if not Users.validate_login(request.form):
        return redirect('/login')
    data = {'email': request.form['email']}
    user_with_email = Users.get_by_email(data)
    userId = user_with_email.id
    if 'userId' in session:
        return redirect(f'/profile/{userId}')
    if user_with_email == False:
        flash("Invalid Email/Password.")
        return redirect('/')
    if not bcrypt.check_password_hash(user_with_email.password, request.form['password']):
        flash("Invalid Email/Password.")
        return redirect('/')
    session['userId'] = user_with_email.id
    return redirect('/')

@app.route('/profile/<int:userId>')
def user_profile(userId):
    if 'userId' not in session:
        return redirect('/')
    user_data = {
        'id': session['userId'],
        'userId': userId
    }
    listing = Users.user_listings(user_data)
    one_user = Users.get_profile(user_data)
    print("***********")
    print(listing.listings)
    if one_user == False:
        return redirect('/login')
    return render_template('profile.html', user_profile = one_user, listings = listing.listings)

# Logout, for logout form/button
@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect('/')