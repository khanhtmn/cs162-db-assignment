The repo for this assignment is available here: [https://github.com/khanhtmn/cs162-db-assignment](https://github.com/khanhtmn/cs162-db-assignment)

# How to run the file

```
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip3 install -r requirements.txt
$ python3 create.py
$ python3 insert_data.py
$ python3 query_data.py
```

As part of your assignment, your must highlight places where you have appropriately used data normalization, indices, and transactions. Please draw attention to any areas of your assignment where you have exceeded the requirements of this assignment.

# Data normalization
## First normal form
Here are the conditions for the first normal form and how my submission fulfills them:
1. __Each row is uniquely defined (primary key)__: Each table has either a primary key or a composite primary key (table `OfficeArea` and `AgentOffice`) to define the uniqueness of each row.
1. __No groups in each column__: Because each agent can belong to multiple offices, I could have created a column in table `Agent` to with a list of offices. However, to fulfill this condition, I create a table `AgentOffice` to map the agents with their respective offices. Same logic applies to table `OfficeArea` because each office is in charge of multiple zipcodes.
1. __Each column has the same type of data__: Each column has the same type of data in each table.
  
## Second normal form
Here are the conditions for the second normal form and how my submission fulfills them:
1. __The database needs to be in first normal form__: This is already proved by above.
1. __All non-key columns depend on the primary key__: At first I store the information of the agents and offices in all 1 table. The primary key was the Office ID. However, because the agent information, such as their names and contact information, is not dependent on the primary key `office_id`, so I split the table into `Office` and `Agent` tables. Same logic was applied to table `House`, `Listing`, and `Sale`. I could have put all information into 1 table, but I assume the company may want to keep track of the information of each house in case it was listed and sold multiple times, so I create the table `House` just to keep track of the information of the house.

## Third normal form
Here are the conditions for the third normal form and how my submission fulfills them:
1. __The database needs to be in second normal form__: This is already proved by above
1. __All fields can be determined only by the key in the table and no other column__: Originally I had the contact details of the agents in each listing because that's how the buyer can contact them. However, I realize that if I know the `agent_id`, I can look up in the `Agent` table and find the rest of the contact details there too. Therefore, I removed the contact details of the `Agent` in the `Listing` table and only left the `agent_id` there. Same logic was applied for the `buyer_id` and buyer details in the `Sale` table.

# Indices
I'm still not sure how robust each field in the table is, but based on the query of the monthly report, I see that we need to filter by date and do a lot of joins on the `listing_id`. Therefore, I created the index for `listing_date`, `selling_date`, and `listing_id` in table `Listing` and table `Sale`. 

# Transaction
I use transaction in inserting the data in `insert.py`, line 58 to line 68. Each row adding to the database is a transaction and if there's any error, the `session` will rollback and not commit the changes to the database.

# Code

### `requirements.txt`
```
SQLAlchemy==1.4.5
pandas==1.2.3
```
### `services.py`
```
# Helper function to calculate the commission
def calc_commission(sale_price):
    if sale_price < 100000:
        commission = 0.1*sale_price
    elif 100000 <= sale_price < 200000:
        commission = 0.075*sale_price
    elif 200000 <= sale_price < 500000:
        commission = 0.06*sale_price
    elif 500000 <= sale_price < 1000000:
        commission = 0.05*sale_price
    elif sale_price >= 1000000:
        commission = 0.04*sale_price
    return commission
```

### `create.py`
```
import sqlalchemy
from sqlalchemy import create_engine, Column, Text, Integer, ForeignKey, String, Numeric, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import Enum
from datetime import datetime
from services import calc_commission

engine = create_engine('sqlite:///database.db')
engine.connect()

Base = declarative_base()

class AreaEnum(Enum):
    east = "east"
    west = "west"
    north = "north"
    south = "south"

class Office(Base):
	__tablename__ = 'offices'
	office_id = Column(Integer, primary_key = True) # Insert auto increment
	office_name = Column(String)
	office_area = Column(Enum("east", "west", "north", "south", name="AreaEnum"))

	def __repr__(self):
		return "<Office(office_id={0}, office_name={1}, office_area={2})>".format(self.office_id, self.office_name, self.office_area)

class OfficeArea(Base):
	__tablename__ = 'office_areas'
	office_id = Column(Integer, ForeignKey('offices.office_id'), primary_key = True)
	zipcode = Column(Integer, primary_key = True)
	offices = relationship(Office)

	def __repr__(self):
		return "<OfficeArea(office_id={0}, zipcode={1}>".format(self.office_id, self.zipcode)

class House(Base):
	__tablename__ = 'houses'
	house_id = Column(Integer, primary_key = True) # Insert auto increment
	bedrooms = Column(Integer)
	bathrooms = Column(Float(1))
	zipcode = Column(Integer)

	def __repr__(self):
		return "<House(house_id={0}, bedrooms={1}, bathrooms={2}, zipcode={3}>".format(
            self.house_id, self.bedrooms, self.bathrooms, self.zipcode)

class Seller(Base):
	__tablename__ = 'sellers'
	seller_id = Column(Integer, primary_key = True)
	first_name = Column(String)
	last_name = Column(String)
	email = Column(String)
	phone_number = Column(String)

	def __repr__(self):
		return "<Seller(seller_id={0}, first_name={1}, last_name={2}, email={3}, \
                phone_number={4}>".format(self.seller_id, self.first_name, self.last_name,
                                          self.email, self.phone_number)

class Buyer(Base):
	__tablename__ = 'buyers'
	buyer_id = Column(Integer, primary_key = True)
	first_name = Column(String)
	last_name = Column(String)
	email = Column(String)
	phone_number = Column(String)

	def __repr__(self):
		return "<Buyer(buyer_id={0}, first_name={1}, last_name={2}, email={3}, \
                phone_number={4}>".format(self.buyer_id, self.first_name, self.last_name,
                                          self.email, self.phone_number)

class Agent(Base):
	__tablename__ = 'agents'
	agent_id = Column(Integer, primary_key = True)
	first_name = Column(String)
	last_name = Column(String)
	email = Column(String)
	phone_number = Column(String)

	def __repr__(self):
		return "<Agent(agent_id={0}, first_name={1}, last_name={2}, email={3}, \
                phone_number={4}>".format(self.agent_id, self.first_name, self.last_name,
                                          self.email, self.phone_number)

class AgentOffice(Base):
	__tablename__ = 'agent_offices'
	agent_id = Column(Integer, ForeignKey('agents.agent_id'), primary_key = True)
	office_id = Column(Integer, ForeignKey('offices.office_id'), primary_key = True)
	agents = relationship(Agent)
	offices = relationship(Office)

	def __repr__(self):
		return "<AgentOffice(agent_id={0}, office_id={1}>".format(self.agent_id, self.office_id)

class StatusEnum(Enum):
    available = "available"
    sold = "sold"

class Listing(Base):
	__tablename__ = 'listings'
	listing_id = Column(Integer, primary_key = True, index=True)
	house_id = Column(Integer, ForeignKey('houses.house_id'))
	seller_id = Column(Integer, ForeignKey('sellers.seller_id'))
	agent_id = Column(Integer, ForeignKey('agents.agent_id'))
	office_id = Column(Integer, ForeignKey('offices.office_id'))
	listing_price = Column(Float(2))
	listing_date = Column(DateTime, index=True)
	status = Column(Enum("available", "sold", name="StatusEnum"), default="available") # Available or Sold - Enum
	houses = relationship(House)
	sellers = relationship(Seller)
	agents = relationship(Agent)
	offices = relationship(Office)

	def __repr__(self):
		return "<Listing(listing_id={0}, house_id={1}, seller_id={2}, \
                agent_id={3}, office_id={4}, listing_price={5}, listing_date={6}, status={7} \
                >".format(self.listing_id, self.house_id, self.seller_id, self.agent_id,
                          self.office_id, self.listing_price, self.listing_date, self.status)

class Sale(Base):
	__tablename__ = 'sales'
	sale_id = Column(Integer, primary_key = True)
	listing_id = Column(Integer, ForeignKey('listings.listing_id'), index=True)
	buyer_id = Column(Integer, ForeignKey('buyers.buyer_id'))
	selling_price = Column(Float(2))
	selling_date = Column(DateTime, index=True)
	commission = Column(Float(2))
	listings = relationship(Listing)
	buyers = relationship(Buyer)

	def __repr__(self):
		return "<Sale(sale_id={0}, listing_id={1}, buyer_id={2}, selling_price={3}, selling_date={4} \
                commission={5}>".format(self.sale_id, self.listing_id, self.buyer_id, self.selling_price,
                self.selling_date, self.commission)

Base.metadata.create_all(bind=engine)
```

### `insert.py`
```
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import datetime
from create import Office, OfficeArea, AreaEnum, House, Seller, Buyer, Agent, AgentOffice, Listing, Sale, StatusEnum
from services import calc_commission

engine = create_engine('sqlite:///database.db', echo=True)
engine.connect()

Session = sessionmaker(bind=engine)
session = Session()

# Data
offices_to_add = [{'office_id': 1, 'office_name': "Magical Land 01", 'office_area': AreaEnum.east},
                  {'office_id': 2, 'office_name': "Magical Land 02", 'office_area': AreaEnum.east}]

office_areas_to_add = [{'office_id': 1, 'zipcode': 11010},
                       {'office_id': 1, 'zipcode': 11011},
                       {'office_id': 1, 'zipcode': 11012},
                       {'office_id': 2, 'zipcode': 22020},
                       {'office_id': 2, 'zipcode': 22021}]

houses_to_add = [{'house_id': 1, 'bedrooms': 1, 'bathrooms': 1, 'zipcode': 11010},
                 {'house_id': 2, 'bedrooms': 2, 'bathrooms': 1, 'zipcode': 11010},
                 {'house_id': 3, 'bedrooms': 2, 'bathrooms': 2, 'zipcode': 11010},
                 {'house_id': 4, 'bedrooms': 1, 'bathrooms': 1.5, 'zipcode': 22020}]

sellers_to_add = [{'seller_id': 1, 'first_name': "Jessica", 'last_name': "Jung", 'email': "jess@jessisme.com", 'phone_number': "010-700-009"},
                   {'seller_id': 2, 'first_name': "Timmothy", 'last_name': "Frank", 'email': "timmy007@mail.com", 'phone_number': "151-720-151"},
                   {'seller_id': 3, 'first_name': "Khanh", 'last_name': "Tran", 'email': "hello@khanh.com", 'phone_number': "413-456-789"}]

buyers_to_add = [{'buyer_id': 1, 'first_name': "Ivy", 'last_name': "Chen", 'email': "poisonous_ivy@mail.com", 'phone_number': "222-111-009"},
                   {'buyer_id': 2, 'first_name': "Edward", 'last_name': "Choi", 'email': "eddiechoi@mail.com", 'phone_number': "444-111-189"},
                   {'buyer_id': 3, 'first_name': "David", 'last_name': "Park", 'email': "davidpark89@mail.com", 'phone_number': "435-157-079"}]

agents_to_add = [{'agent_id': 1, 'first_name': "Michelle", 'last_name': "Brown", 'email': "michelle@magicalland.com", 'phone_number': "345-134-659"},
                   {'agent_id': 2, 'first_name': "Rachel", 'last_name': "Lee", 'email': "rachel@magicalland.com", 'phone_number': "204-157-013"},
                   {'agent_id': 3, 'first_name': "Jason", 'last_name': "Xu", 'email': "jason@magicalland.com", 'phone_number': "583-121-923"}]

agent_offices_to_add = [{'agent_id': 1, 'office_id': 1},
                        {'agent_id': 1, 'office_id': 2},
                        {'agent_id': 2, 'office_id': 1},
                        {'agent_id': 3, 'office_id': 2}]

listings_to_add = [{'listing_id': 1, 'house_id': 1, 'seller_id': 1, 'agent_id': 2, 'office_id': 2, 'listing_price': 100000,
                    'listing_date': datetime(2020,11, 1, 10, 0, 0), 'status': StatusEnum.available},
                    {'listing_id': 2, 'house_id': 4, 'seller_id': 2, 'agent_id': 2, 'office_id': 2, 'listing_price': 200000,
                    'listing_date': datetime(2020,11, 1, 10, 0, 0), 'status': StatusEnum.available},
                    {'listing_id': 3, 'house_id': 2, 'seller_id': 3, 'agent_id': 1, 'office_id': 1, 'listing_price': 150000,
                    'listing_date': datetime(2020,11, 1, 10, 0, 0), 'status': StatusEnum.available}]

# Insert Office, OfficeArea, House, Seller, Buyer, Agent, AgentOffice, Listing data
keys = [(offices_to_add, Office), (office_areas_to_add, OfficeArea), (houses_to_add, House),
        (sellers_to_add, Seller), (buyers_to_add, Buyer), (agents_to_add, Agent),
        (agent_offices_to_add, AgentOffice), (listings_to_add, Listing)]

for dict_to_add, table in keys:
    for dict_row in dict_to_add:
        try:
            stmt = table(**dict_row)
            session.add(stmt)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

# Insert Sale data
def update_sale(sale_id, listing_id, buyer_id, selling_price, selling_date):
    commission = calc_commission(selling_price)

    try:
        session.add(Sale(sale_id=sale_id, listing_id=listing_id, buyer_id=buyer_id,
                    selling_price=selling_price, selling_date=selling_date, commission=commission))
        session.query(Listing).filter_by(listing_id=listing_id).update({"status":StatusEnum.sold})
        session.commit()

    except:
        session.rollback()
        raise
    finally:
        session.close()

update_sale(sale_id = 1, listing_id = 1, buyer_id = 1, selling_price = 95000, selling_date = datetime(2020,12, 15, 10, 0, 0))
update_sale(sale_id = 2, listing_id = 3, buyer_id = 2, selling_price = 145000, selling_date = datetime(2020,12, 30, 10, 0, 0))
update_sale(sale_id = 3, listing_id = 2, buyer_id = 3, selling_price = 200000, selling_date = datetime(2020,12, 30, 10, 0, 0))
```

### `query.py`
```
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, text
import pandas as pd

engine = create_engine('sqlite:///database.db')
conn = engine.connect()
conn

Session = sessionmaker(bind=engine)
session = Session()

# 1. Find the top 5 offices with the most sales for that month
month = 12
year = 2020
stmt = text(f"""SELECT o.office_id, SUM(s.selling_price) FROM offices o
            JOIN listings l on o.office_id = l.office_id
            JOIN sales s on l.listing_id = s.listing_id
            WHERE s.selling_date >= '{year}-{month}-01 00:00:00'
            GROUP BY l.office_id
            ORDER BY SUM(s.selling_price) DESC
            LIMIT 5""")
results = conn.execute(stmt).fetchall()
df = pd.DataFrame(results, columns=['Office ID','Total sales'])
print(f'1. Top 5 offices with the most sales for month {month} and year {year}')
print(df.to_string(index=False))
print("-----------------------------------------------------------------")

# 2. Find the top 5 estate agents who have sold the most
# (include their contact details and their sales details so that it is easy
# contact them and congratulate them).
stmt = text("""SELECT a.agent_id, a.first_name, a.last_name, a.email, a.phone_number,  COUNT(l.listing_id)
            FROM agents a
            JOIN listings l on a.agent_id = l.agent_id
            GROUP BY a.agent_id
            HAVING l.status = "sold"
            ORDER BY COUNT(l.listing_id) DESC
            LIMIT 5""")
results = conn.execute(stmt).fetchall()
df = pd.DataFrame(results, columns=['Agent ID','First name', 'Last name', 'Email', 'Phone number', 'Number of sales'])
print(f'2. Top 5 estate agents who have sold the most and their contact details')
print(df.to_string(index=False))
print("-----------------------------------------------------------------")

# 3. Calculate the commission that each estate agent must receive
# and store the results in a separate table.
stmt = text("""SELECT l.agent_id, SUM(s.commission) FROM sales s \
                JOIN listings l on s.listing_id = l.listing_id \
                GROUP BY l.agent_id""")
results = conn.execute(stmt).fetchall()
df = pd.DataFrame(results, columns=['Agent ID','Total commission'])
print(f'3. The commission that each estate agent must receive')
print(df.to_string(index=False))
print("-----------------------------------------------------------------")

# 4. For all houses that were sold that month, calculate the average
# number of days that the house was on the market.
stmt = text("""
            SELECT AVG(julianday(s.selling_date)-julianday(l.listing_date)) FROM sales s
            JOIN listings l on s.listing_id = l.listing_id
            WHERE s.selling_date >= '2020-12-01 00:00:00'
            """)
results = conn.execute(stmt).fetchall()
df = pd.DataFrame(results, columns=['Average number of days'])
print(f'4. The average number of days that the house was on the market')
print(df.to_string(index=False))
print("-----------------------------------------------------------------")

# 5. For all houses that were sold that month, calculate the average selling price
month = 12
year = 2020
stmt = text(f"""SELECT ROUND(AVG(s.selling_price), 2) FROM sales s
            WHERE s.selling_date >= '{year}-{month}-01 00:00:00'
            """)
results = conn.execute(stmt)
df = pd.DataFrame(results, columns=['Average selling price'])
print(f'5. Average selling price of house sold in month {month} of year {year}')
print(df.to_string(index=False))
print("-----------------------------------------------------------------")

# 6. Find the zip codes with the top 5 average sales prices
stmt = text("""SELECT h.zipcode, AVG(s.selling_price) FROM houses h
                JOIN listings l on h.house_id = l.house_id
                JOIN sales s on l.listing_id = s.listing_id
                GROUP BY h.zipcode
                ORDER BY AVG(s.selling_price) DESC
                LIMIT 5""")
results = conn.execute(stmt).fetchall()
df = pd.DataFrame(results, columns=['Zipcode','Average selling price'])
print(f'6. The zip codes with the top 5 average sales prices')
print(df.to_string(index=False))
print("-----------------------------------------------------------------")
```
