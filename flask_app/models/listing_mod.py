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
        self.createDate = data['created_at']
        self.updatedDate = data['updated_at']
        self.useriD = data['updated_at']
        self.likes = []

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
        query = "INSERT INTO listings (title, description, listPrice, createdDate, updatedDate, userID) VALUES (%(title)s, %(description)s, %(listPrice)s, NOW(), NOW(), %(userID)s);"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results

# Get all home listings, for public listing page
    @classmethod
    def get_listings(cls):
        query = "SELECT * FROM listings;"
        results = connectToMySQL(cls.db_name).query_db(query)
        if not results:
            return False
        
        all_listings = []

        for row in results:
            row['likes'] = Listings.get_listing_likes(row)
            all_listings.append(row)
        
        return all_listings

# Get all home listings, for public listing page
    @classmethod
    def get_one_listing(cls, data):
        query = "SELECT * FROM listings WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if not results:
            return False
        return cls(results[0])

# Edit home listing
    @classmethod
    def update_listing(cls, data):
        query = "UPDATE listings SET name=%(name)s, prod_desc=%(description)s, price=%(listPrice)s, updatedDate=NOW() WHERE id = %(id)s"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results

# Delete home listing
    @classmethod
    def delete_listing(cls, data):
        query = "DELETE FROM listings WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

# Like a listing
    @classmethod
    def like_listing(cls, data):
        query = "INSERT INTO likes (userID, listingID) VALUES (%(userID)s, %(listingID)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results       

    @classmethod
    def get_listing_likes(cls, data):
        query = "SELECT DISTINCT userID FROM likes WHERE listingID = %(listingID)s"
        result = connectToMySQL(cls.db_name).query_db(query, data)

        liked_users = []

        for row in result: 
            liked_users.append(row)

        return liked_users
