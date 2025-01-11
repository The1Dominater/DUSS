### rGPC client ###
import grpc
import rental_app_pb2
import rental_app_pb2_grpc

### Database ###
from sqlalchemy import create_engine, Column, Integer, String, SmallInteger, BigInteger, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Define the database connection string (replace with your own credentials)
DATABASE_URI = 'postgresql://admin:GoofyAdmin@localhost/dussdb'
#DATABASE_URI = os.getenv("DATABASE_URL")

# Set up SQLAlchemy
Model = declarative_base()

class Reservation(Model):
    __tablename__ = "reservations"
    reservation_num = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("customer_accounts.id"))
    eq_type = Column(String(16))
    lease_type = Column(SmallInteger) # 1=seasonal 2=daily
    pkg_type = Column(SmallInteger) # 1=demo 2=premium 3=basic 4=junior
    hint = Column(String(1000))
    telephone = Column(BigInteger)

class CustomerAccount(Model):
    __tablename__ = "customer_accounts"
    id = Column(Integer, primary_key=True)
    email = Column(String(150), unique=True)
    password = Column(String(150))
    firstName = Column(String(150))
    lastName = Column(String(150))
    reservations = relationship('Reservation')
    #workrequests = relationship('WorkRequest')

class AdjustmentInfo(Model):
    __tablename__ = "adjustment_info"
    user_id = Column(Integer, ForeignKey("customer_accounts.id"), primary_key=True)
    height = Column(Integer)
    h_unit = Column(SmallInteger) # 1=cm 2=in
    weight = Column(Integer)
    w_unit = Column(SmallInteger) # 1=kg 2=lbs
    skier_type = Column(SmallInteger)
    l_offset = Column(SmallInteger)
    r_offset = Column(SmallInteger)
    riding_style = Column(SmallInteger) # 1=Regular(left) 2=Goofy(right)
    birthday = Column(Integer)

# Create a database engine
engine = create_engine(DATABASE_URI)

# Create tables if they don't exist
Model.metadata.create_all(engine)

# Set up session maker
Session = sessionmaker(bind=engine)
session = Session()

class Caclulator:
    def __init__(self, user_id:int):
        self.user_id = 1

    def calculate_age(self):

        print("The customer's age is:")
        # Add your function logic here

    def calculate_din(self):
        print("You selected Option Two.")
        # Add your function logic here

    def calculate_total(self):
        print("You selected Option Three.")
        # Add your function logic here

def display_menu(actions):
    print("\nMain Menu:")
    i = 1
    for action in actions:
        display_action = f"{i}. {action}"
        print(display_action)
        i += 1

def get_age(birthday,channel,debug=False):
    # Create the stub object
    stub = rental_app_pb2_grpc.ageStub(channel)
    # Create the addMsg object to be sent
    age_msg = rental_app_pb2.birthdayMsg(birthday=birthday)
    # Get response
    determined_age = stub.age(age_msg)
        
    if debug:
        # decode response
        print("Response is:", determined_age.age)
    
    return determined_age.age

def get_din(age,height,h_unit,weight,w_unit,skier_type,channel,debug=False):
    # Create the stub object
    stub = rental_app_pb2_grpc.dinStub(channel)
    # Create the addMsg object to be sent
    din_msg = rental_app_pb2.dinMsg(age=age,
                                    height=height,
                                    h_unit=h_unit,
                                    weight=weight,
                                    w_unit=w_unit,
                                    skier_type=skier_type)
    # Get response
    calculated_din = stub.din(din_msg)
        
    if debug:
        # decode response
        print("Response is:", calculated_din.din)
    
    return calculated_din.din

def get_total(eq_type,lease_type,pkg_type,channel,debug=False):
    stub = rental_app_pb2_grpc.totalStub(channel)
    if eq_type == 'ski':
        eq_type = 1
    elif eq_type == 'snowboard':
        eq_type = 2
    else:
        eq_type = 3
    
    total_msg = rental_app_pb2.totalMsg(eq_type=eq_type,
                                     lease_type=lease_type,
                                     pkg_type=pkg_type)
    calculated_total = stub.total(total_msg)
        
    if debug:
        # decode response
        print("Response is:", calculated_total.total)
    
    return calculated_total.total

def main():
    # Define a variable to store the current customer
    global customer_id
    customer_id=None
    actions = ['Find Reservation', 'Find Customer', 'Clear Customer', 'Calculate Age', 'Calculate DIN', 'Calculate Total', 'Exit']

    # Set up a channel for gRPC
    host = 'localhost'
    port = '50051'
    addr = f'{host}:{port}/rental-server'
    channel = grpc.insecure_channel(addr)

    while True:
        display_menu(actions)
        choice = input("Enter your choice: ")
        if choice == str(len(actions)):
            print("Exiting the program. Goodbye!")
            break
        elif choice == '1':
            telephone = input("Please input telephone number: ")
            reservation = session.query(Reservation).filter_by(telephone=telephone).first()
            if reservation:
                customer_id = reservation.user_id
                account = session.query(CustomerAccount).filter_by(id=customer_id).first()
                first_name = account.firstName
                last_name = account.lastName
                print(f"{telephone}-->{first_name} {last_name}")
            else:
                print(f"Nothing found for the given telephone number: {telephone}")
        elif choice == '2':
            email = input("Please input email: ")
            account = session.query(CustomerAccount).filter_by(email=email).first()
            if account:
                customer_id = account.id
                first_name = account.firstName
                last_name = account.lastName
                print(f"{email}-->{first_name} {last_name} ")
            else:
                print(f"Nothing found for the given email:{email}")
        elif choice == '3':
            customer_id = None
            print()
            print("### Cleared customer ###")
        elif choice == '4':
            if customer_id:
                # Grab birthday info from the database
                adjinfo = session.query(AdjustmentInfo).filter_by(user_id=customer_id).first()
                birthday = adjinfo.birthday
                if birthday is None:
                    print("No birthday on file!")
                    birthday = input("Please input birthday in MMDDYYYY format: ")
                age = get_age(birthday,channel)
                print(f"Customer's age: {age}")
            else:
                print("Please first select a reservation or customer using options 1 & 2!")
        elif choice == '5':
            if customer_id:
                # Grab height, weight, h_unit, w_unit, skier_type, and age from database
                adjinfo = session.query(AdjustmentInfo).filter_by(user_id=customer_id).first()
                age = get_age(adjinfo.birthday,channel)
                height = adjinfo.height
                h_unit = adjinfo.h_unit
                weight = adjinfo.weight
                w_unit = adjinfo.w_unit
                skier_type = adjinfo.skier_type

                din = get_din(age, height, h_unit, weight, w_unit, skier_type, channel)
                print(f"Customer's DIN is: {din}")
            else:
                print("Please first select a reservation or customer using options 1 & 2!")
        elif choice == '6':
            if customer_id:
                reservation = session.query(Reservation).filter_by(user_id=customer_id).first()
                eq_type = reservation.eq_type
                lease_type = reservation.lease_type
                pkg_type = reservation.pkg_type

                total_cost = get_total(eq_type, lease_type, pkg_type, channel)
                print("################################## Total #######################################")
                print(f"{eq_type} {lease_type} {pkg_type} ........................ ${total_cost:.2f}")
            else:
                print("Please first select a reservation or customer using options 1 & 2!")
        else:
           print()
           print("Please enter a valid option!") 
                

if __name__ == "__main__":
    main()
