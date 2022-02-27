from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.listing_mod import Listings
from flask_app.models.user_mod import Users

# Add template for "new listing"
@app.route('/new_listing/<int:userID>')
def create_listing(userID):
    if 'userID' not in session:
        return redirect('/')
    
    userID = session['userID']
    return render_template('new_listing.html', current_user = userID)

@app.route('/process_listing/<int:userID>', methods=['POST'])
def process_listing(userID):
    userID = session['userID']
    if not Listings.validate_listing(request.form):
        # Add template for "new listing"
        return redirect(f'/new_listing/{userID}') 
    
    data = {
        'title': request.form['name'],
        'description': request.form['description'],
        'listPrice': request.form['listPrice'],
        'userID': session['userID']
    }
    Listings.save_listing(data)
    # Add template for "profile" page
    return redirect(f'/profile/{userID}')

@app.route('/listings/<int:listingID>')
def all_listings(listingID):
    if 'userID' in session:
        user_data = {
            'id': session['userID']
        }
        list_data = {
            'listingID': listingID
        }
        one_user = Users.get_profile(user_data)
        all_listings = Listings.get_listings(list_data)
        return render_template('listings.html', current_user = one_user, listings = all_listings)
    else:
        list_data = {
            'listingID': listingID
        }
        all_listings = Listings.get_listings(list_data)
        return render_template('listings.html', current_user = False, session = 0, listings = all_listings)

@app.route('/edit_listing/<int:userID>/<listingID>')
def edit_listing(userID, listingID):
    userID = session['userID']
    data = {
        'id': listingID
    }
    one_listing = Listings.get_listings(data)
    return render_template('edit_listing.html', current_user = userID, listing = one_listing)

@app.route('/update_listing/<int:userID>/<listingID>', methods=['POST'])
def update_listing(userID, listingID):
    userID = session['userID']
    if 'userID' not in session:
        return redirect('/')
    if not Listings.validate_edit(request.form):
        return redirect(f'/edit_listing/{userID}/{listingID}')
    data = {
        'id': listingID,
        'title': request.form['title'],
        'description': request.form['description'],
        'listPrice': request.form['listPrice'],
        'userID': session['userID']
    }
    Listings.update_listing(data)
    return redirect(f'/profile/{userID}')

@app.route('/delete_listing/<int:userID>/<listingID>', methods=['POST'])
def delete_listing(userID, listingID):
    userID = session['userID']
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': listingID
    }
    Listings.delete_listing(data)
    return redirect(f'/profile/{userID}')

@app.route('/like_listing/<int:userID>/<listingID>')
def like_listing(userID, listingID):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'userID': userID,
        'listingID' : listingID
    }

    Listings.like_listing(data)

    return redirect(f'/listings/{listingID}')




