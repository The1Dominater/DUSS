from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from .models import CustomerAccount
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint("auth", __name__)

@auth.route('/login', methods=["GET","POST"])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = CustomerAccount.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in successfully", category='success')
                login_user(user, remember=True)
                
                # If the user was trying to access a page that requires login
                # then send them to that page after login
                next_page = request.args.get('next')
                if next_page:
                    return redirect(next_page)
                
                # If not return to the home page
                return redirect(url_for('views.home'))
            else:
                flash("Email or password not recognized", category='error')
        else:
            flash("Email address not associated with any existing users!", category='error')
    
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    flash("Logged out successfully", category='success')
    logout_user()
    return redirect(url_for('views.home'))

@auth.route('/sign-up', methods=["GET","POST"])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        password = request.form.get('password') 
        confirm_password = request.form.get('confirm_password')

        user = CustomerAccount.query.filter_by(email=email).first()
        if user:
            flash("Account associated with the email already exists!",category='error')
        elif len(email) < 5:
            flash("Email must be greater than 4 characters.", category='error')
        elif len(firstName) < 2:
            flash("First name must be greater than 1 character.", category='error')
        elif len(lastName) < 2:
            flash("Last name must be greater than 1 character.", category='error')
        elif len(password) < 12:
            flash("Password must be 12 or more characters.", category='error')
        elif confirm_password != password:
            flash("Passwords do not match!", category='error')
        else:
            # Add user to database
            hashed_pass = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
            new_user = CustomerAccount(email=email, firstName=firstName,lastName=lastName,password=hashed_pass)
            db.session.add(new_user)
            db.session.commit()

            # Inform the user the account has been created
            flash("Account created!", category='success')

            # Automatically log user in once account is created
            login_user(new_user, remember=True)

            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)
