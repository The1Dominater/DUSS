from flask import Blueprint, render_template, request, flash, redirect, session
from flask_login import login_required, current_user
from website.models import *
from . import db
from datetime import datetime, timedelta

views = Blueprint("views", __name__)

RESERVATIONS_ON=True #TODO Add a admin switch to turn these on or off

@views.route('/')
def home():
    return render_template('home.html', user=current_user)

@views.route('/store', methods=['GET','POST'])
def store():
    items = StoreItem.query.all() #TODO build a better store scrolling page
    return render_template('store.html', user=current_user, items=items)

def verify_guest(guest):
    ### Verify the guest's information
    # Output: False if any of the inputs fail, True otherwise

    first_name = guest['first_name']
    last_name = guest['last_name']
    birthday = guest['birthday']

    # Check if first and last name are appropriate lengths
    if len(first_name) < 1:
        flash(f"The provided first name is too short! Name given: {first_name}", category='error')
        return False
    elif len(first_name) > 150:
        flash(f"The provided first name is too long! Name given: {first_name}", category='error')
        return False
    if len(last_name) < 1:
        flash(f"The provided last name is too short! Name given: {first_name}", category='error')
        return False
    elif len(last_name) > 150:
        flash(f"The provided last name is too long! Name given: {first_name}", category='error')
        return False
    if not all(character.isalpha() or character.isspace() for character in first_name):
        flash(f"The provided first name contains not alphabetic characters! Name given: {first_name}", category='error')
        return False
    if not all(character.isalpha() or character.isspace() for character in last_name):
        flash(f"The provided last name contains not alphabetic characters! Name given: {last_name}", category='error')
        return False
    
    # Check if the birthday is a valid date
    try:
        today = datetime.now()
        birthday_strp=datetime.strptime(birthday, "%Y-%m-%d")
        if birthday_strp >= today:
            flash(f"The provided birthday of {birthday} for {last_name},{first_name} has not occurred yet!", category='error')
            return False
        elif (today - timedelta(days=150 * 365.25)) >= birthday_strp:
            flash(f"The provided birthday of {birthday} for {last_name},{first_name} is too old!", category='error')
            return False
        else:
            return True
    except:
        flash(f"The provided birthday of {birthday} for {last_name},{first_name} is not a valid date! ", category='error')
        return False

def verify_party_leader(guest):
    ### Verify the party leader's information
    # Output: False if any of the inputs fail, True otherwise

    first_name = guest['first_name']
    last_name = guest['last_name']
    birthday = guest['birthday']
    telephone = guest['telephone']

    # Make sure the party leader is 18+ to make reservation
    try:
        min_age = datetime.now() - timedelta(days=18 * 365.25)
        birthday_strp=datetime.strptime(birthday, "%Y-%m-%d")
        if birthday_strp >= min_age:
            flash(f"The party leader must be 18+ but the provided birthday({birthday}) is to young!", category='error')
            return False
        else:
            return verify_telephone(telephone)
    except:
        flash(f"The provided birthday of {birthday} for {last_name},{first_name} is not a valid date! ", category='error')
        return False

def verify_telephone(telephone:str):
    ### Verify the party leader's phone number
    # - telephone is a phone number from anywhere
    # Output: False if the phone number is invalid, True otherwise
    # Import phonenumbers package to verify all numbers
    import phonenumbers

    # Strip all unnecessary characters(including '+','(',')','-', and ' ')
    telephone_wo_chars = ''.join([char for char in telephone if char.isdigit()])
    # Assume 10 digit numbers are from USA; append country code 1 
    if len(telephone_wo_chars) == 10:
        telephone_wo_chars = "1" + telephone_wo_chars
    # Add/Re-add '+' so parser can interpret country code
    telephone_number = "+" + telephone_wo_chars

    try:
        # Parse the phone number
        parsed_number = phonenumbers.parse(telephone_number)
        
        # Check if the phone number is valid
        if not phonenumbers.is_valid_number(parsed_number):
            flash(f"Invalid phone number provided: {telephone}", category='error')
            return False
    except phonenumbers.phonenumberutil.NumberParseException:
        flash(f"Invalid phone number format: {telephone}", category='error')
        return False
    
    # If all conditions are meet return True
    return True

@views.route("/reservation", methods=['GET','POST'])
@login_required
def reservation():
    # Grab todays date so it can be passed to HTML 
    today=datetime.now()

    if request.method == 'POST':
        # Initailize a list of guests
        guests = []

        # Grab guest information from the form and verify it on the backend
        guest_validation = True
        for key in request.form.keys():
            index = key.split('_')[-1]
            if index.isdigit():
                print(key)

                guest = {
                    'first_name': request.form.get(f'first_name_{index}'),
                    'last_name': request.form.get(f'last_name_{index}'),
                    'birthday': request.form.get(f'birthday_{index}'),
                    'eq_type': request.form.get(f'eq_type_{index}'),
                 }
                
                if verify_guest(guest):
                    if index == 0:
                        guest['telephone'] = request.form.get(f'telephone')
                        if not verify_party_leader(guest):
                            guest_validation = False
                            break
                    
                    guests.append(guest)
                else:
                   guest_validation = False 
        
        # If inputs were valid store information in db
        if guest_validation:
            
            return render_template('/reservations/reservation_success.html', user=current_user)
        # If inputs were invalid return the form with all the information contained in it    
        else:
            print("Invalid info provided")
            customer = CustomerAccount.query.filter_by(id=current_user.id).first()
            
            return render_template('/reservations/reservation_all_error.html', 
                                user=current_user, 
                                first_name=customer.firstName,
                                last_name=customer.lastName,
                                today=today.strftime('%Y-%m-%d'),
                                min_pl_age=(today - timedelta(days=18 * 365.25)).strftime('%Y-%m-%d'),
                                max_age=(today - timedelta(days=130 * 365.25)).strftime('%Y-%m-%d'),
                                max_pickup=(today - timedelta(days=30)).strftime('%Y-%m-%d'),
                                max_return=30)
    else:
        # If reservations are on show the form
        if RESERVATIONS_ON:
            customer = CustomerAccount.query.filter_by(id=current_user.id).first()

            # Automatically fill in user information as party leader info
            return render_template('/reservations/reservation_all.html', 
                                user=current_user, 
                                first_name=customer.firstName,
                                last_name=customer.lastName,
                                today=today.strftime('%Y-%m-%d'),
                                min_pl_age=(today - timedelta(days=18 * 365.25)).strftime('%Y-%m-%d'),
                                max_age=(today - timedelta(days=130 * 365.25)).strftime('%Y-%m-%d'),
                                max_pickup=(today - timedelta(days=30)).strftime('%Y-%m-%d'),
                                max_return=30)
        # Else display msg about reservations being unavailable
        else:
            return render_template('/reservations/reservation_off.html', user=current_user)

@views.route("/workshop", methods=['GET','POST'])
@login_required
def workshop():
    #print("Workshop", flush=True)
    return render_template('workshop.html', user=current_user)

@views.route("/checkout")
@login_required
def checkout():
    return render_template('checkout.html', user=current_user)

@views.route("/terms")
@views.route("/privacy")
def terms_and_privacy():
    return render_template('terms_and_privacy.html', user=current_user)

@views.route("/contact", methods=['GET','POST'])
def contact():
    if request.method == 'POST':
        # TODO
        pass

    return render_template('contact_us.html', user=current_user)

@views.errorhandler(404)
@views.errorhandler(405)
def page_missing():
    return render_template('page_missing.html', user=current_user)
