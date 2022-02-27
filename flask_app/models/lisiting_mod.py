from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user_mod

class Listings:
    db_name = "Home_Listing_Project_ERD"
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.listPrice = data['listPrice']
        self.imgURL = data['imgURL']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = []

# Confirm fields are filled out
    @staticmethod
    def validate_listing(listing):
        is_valid = True
        if len(listing['title']) < 1:
            flash("Please provide a title for this listing.")
            is_valid = False
        if len(listing['description']) < 20:
            flash("PLease provide a description longer than 20 characters.")
            is_valid = False
        if len(listing['listPrice']) < 0.01:
            flash("Please provide a price for this listing.")
            is_valid = False
        return is_valid

# Confirm edit fields are still filled out
    @staticmethod
    def validate_edit(listing):
        is_valid = True
        if len(listing['title']) < 1:
            flash("Please provide a title for this listing.")
            is_valid = False
        if len(listing['description']) < 20:
            flash("PLease provide a description longer than 20 characters.")
            is_valid = False
        if len(listing['listPrice']) < 0.01:
            flash("Please provide a price for this listing.")
            is_valid = False
        return is_valid

# Save new home listing
    @classmethod
    def save_listing(cls, data):
        query = "INSERT INTO listings (title, description, listPrice, created_at, updated_at, userID) VALUES (%(title)s, %(description)s, %(listPrice)s, NOW(), NOW(), %(userID)s);"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results

# View all home listings associated with user_id
    @classmethod
    def user_listings(cls):
        query = "SELECT * FROM users LEFT JOIN listings ON userID = users.id;"
        results = connectToMySQL(cls.db_name).query_db(query)
        all_listings = []
        for db_row in results:
            listing_data = {
                'id': db_row['listings.id'],
                'title': db_row['title'],
                'description': db_row['description'],
                'listPrice': db_row['listPrice'],
                'created_at': db_row['created_at'],
                'updated_at': db_row['updated_at']
            }
            one_listing = cls(listing_data)
            user_data = {
                'id': db_row['id'],
                'first_name': db_row['first_name'],
                'last_name': db_row['last_name'],
                'email': db_row['email'],
                'password': db_row['password'],
                'created_at': db_row['created_at'],
                'updated_at': db_row['updated_at']
            }
            one_user = user_mod.Users(user_data)
            one_listing.user = one_user
            all_listings.append(one_listing)
        return all_listings

# Get all home listings, for public listing page
    @classmethod
    def get_listings(cls, data):
        query = "SELECT * FROM listings WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if not results:
            return False
        return cls(results[0])

# Edit home listing
    @classmethod
    def update_listing(cls, data):
        query = "UPDATE listings SET name=%(name)s, prod_desc=%(description)s, price=%(listPrice)s, updated_at=NOW() WHERE id = %(id)s"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results

# Delete home listing
    @classmethod
    def delete_listing(cls, data):
        query = "DELETE FROM listings WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)