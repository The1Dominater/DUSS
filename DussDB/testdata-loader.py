import csv, random
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define the database connection string (replace with your own credentials)
DATABASE_URI = 'postgresql://admin:GoofyAdmin@localhost/dussdb'

# Set up SQLAlchemy
Base = declarative_base()

class StoreItem(Base):
    __tablename__ = "store_items"
    sku = Column(Integer, primary_key=True, unique=True)
    model = Column(String(100))
    brand = Column(String(100))
    display_name = Column(String(100))
    price = Column(Float)
    quantity = Column(Integer)
    serial_number=Column(Integer,unique=True)
    description = Column(String(10000))
    image_path = Column(String(256))

class CustomerAccount(Base):
    __tablename__ = "customer_accounts"
    id = Column(Integer, primary_key=True)
    email = Column(String(150), unique=True)
    password = Column(String(150))
    firstName = Column(String(150))
    lastName = Column(String(150))

# Create a database engine
engine = create_engine(DATABASE_URI)

# Create tables if they don't exist
Base.metadata.create_all(engine)

# Set up session maker
Session = sessionmaker(bind=engine)
session = Session()

# Function to read CSV and insert into the database
def insert_items_from_csv(file):
    # Read the CSV file into a Pandas DataFrame
    with open(file, newline='', encoding='utf-8') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            new_item = StoreItem(
                model=row['model'],
                brand=row['brand'],
                display_name=row['display_name'],
                description=row['description'],
                price=row['price'],
                serial_number=random.randint(1000000,9999999),
                quantity=random.randint(1,100)
            )
            # Add to the session
            session.add(new_item)
        session.commit()

# Function to read CSV and insert into the database
def insert_customers_from_csv(file):
    # Read the CSV file into a Pandas DataFrame
    with open(file, newline='', encoding='utf-8') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            new_customer = CustomerAccount(
                email=row['email'],
                password=row['password'],
                firstName=row['firstname'],
                lastName=row['lastname']
            )
            # Add to the session
            session.add(new_customer)
        session.commit()

# To load the test data use:
#  $ kubectl port-forward svc/postgres-svc 5432:5432
# Then you can run the test-loader.py and it should load the data
if __name__ == "__main__":
    # Path to CSV file
    csv_file_path = 'test_store_items.csv'
    insert_items_from_csv(csv_file_path)
    csv_file_path = 'test_customers.csv'
    insert_customers_from_csv(csv_file_path)

    session.close()
