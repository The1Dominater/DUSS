from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class StoreItem(db.Model):
    __tablename__ = "store_items"
    sku = db.Column(db.Integer, primary_key=True, unique=True)
    model = db.Column(db.String(100))
    brand = db.Column(db.String(100))
    display_name = db.Column(db.String(100))
    price = db.Column(db.Float)
    quantity = db.Column(db.Integer)
    serial_number = db.Column(db.Integer,unique=True)
    description = db.Column(db.String(10000))
    image_path = db.Column(db.String(256))

class WorkRequest(db.Model):
    __tablename__ = "work_request"
    user_id = db.Column(db.Integer, db.ForeignKey("customer_accounts.id"))
    order = db.Column(db.Integer, primary_key=True)
    date_made = db.Column(db.DateTime(timezone=True), default=func.now())
    date_completed = db.Column(db.DateTime(timezone=True))
    model = db.Column(db.String(100))
    brand = db.Column(db.String(100))
    description = db.Column(db.String(10000))
    
class Reservation(db.Model):
    __tablename__ = "reservations"
    reservation_num = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("customer_accounts.id"))
    eq_type = db.Column(db.String(16))
    lease_type = db.Column(db.SmallInteger) # 1=seasonal 2=daily
    pkg_type = db.Column(db.SmallInteger) # 1=demo 2=premium 3=basic 4=junior
    hint = db.Column(db.String(1000))
    telephone = db.Column(db.BigInteger)
    
# class ReservationGroup(db.Model):
#    date_made = db.Column(db.DateTime(timezone=True), default=func.now())
#     persons = all people in the group

class CustomerAccount(db.Model, UserMixin):
    __tablename__ = "customer_accounts"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    firstName = db.Column(db.String(150))
    lastName = db.Column(db.String(150))
    reservations = db.relationship('Reservation')
    workrequests = db.relationship('WorkRequest')

class AdjustmentInfo(db.Model):
    __tablename__ = "adjustment_info"
    user_id = db.Column(db.Integer, db.ForeignKey("customer_accounts.id"), primary_key=True)
    height = db.Column(db.Integer)
    h_unit = db.Column(db.SmallInteger) # 1=cm 2=in
    weight = db.Column(db.Integer)
    w_unit = db.Column(db.SmallInteger) # 1=kg 2=lbs
    skier_type = db.Column(db.SmallInteger)
    l_offset = db.Column(db.SmallInteger)
    r_offset = db.Column(db.SmallInteger)
    riding_style = db.Column(db.SmallInteger) # 1=Regular(left) 2=Goofy(right)
    birthday = db.Column(db.Integer)