"""
Every month the following reports need to be run:

Find the top 5 offices with the most sales for that month.
Find the top 5 estate agents who have sold the most (include their contact details and their sales details so that it is easy contact them and congratulate them).
Calculate the commission that each estate agent must receive and store the results in a separate table.
For all houses that were sold that month, calculate the average number of days that the house was on the market.
For all houses that were sold that month, calculate the average selling price
Find the zip codes with the top 5 average sales prices
"""

import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
# from datetime import datetime
# from create import Office, OfficeArea, AreaEnum, House, Seller, Buyer, Agent, AgentOffice, Listing, Sale, StatusEnum,Float
# from services import calc_commission

engine = create_engine('sqlite:///database.db', echo=True)
conn = engine.connect()
conn

Session = sessionmaker(bind=engine, echo=True)
session = Session()

# Find the top 5 offices with the most sales for that month
"""
SELECT office_id, SUM(selling_price) FROM listings
JOIN sales on listings.listing_id = sales.listing_id
GROUP BY office_id
ORDER BY selling_price
WHERE selling_date >= 2020-12-01

SELECT l.office_id, SUM(s.selling_price) from listings l
JOIN sales s on l.listing_id = s.listing_id
GROUP BY l.office_id
ORDER BY SUM(s.selling_price)
WHERE s.selling_date >= 2020-12-01
LIMIT 5
"""
stmt = text("SELECT l.office_id, SUM(s.selling_price) from listings l"
            "JOIN sales s on l.listing_id = s.listing_id"
            "GROUP BY l.office_id"
            "ORDER BY SUM(s.selling_price)"
            "WHERE s.selling_date >= 2020-12-01"
            "LIMIT 5")

result = conn.execute(stmt)
>>> stmt = text("SELECT users.id, addresses.id, users.id, "
...     "users.name, addresses.email_address AS email "
...     "FROM users JOIN addresses ON users.id=addresses.user_id "
...     "WHERE users.id = 1").columns(
...        users.c.id,
...        addresses.c.id,
...        addresses.c.user_id,
...        users.c.name,
...        addresses.c.email_address
...     )
>>> result = conn.execute(stmt)


# session.query(User).all()
# session.query(Insurance).filter_by(claim_id = 1).all()
# https://stackoverflow.com/questions/24508070/convert-sql-to-sql-alchemy
status_counts = db.session.query(BarBaz.status, db.func.count(BarBaz.id).label('count_id')
).filter(db.not_(db.or_(BarBaz.name == 'Foo', BarBaz.name == 'Bar'))
).group_by(BarBaz.status
).all()

select (select COUNT(id) FROM instance where not name = 'erf' and not tiername = 'wer' and type='app')
as app, (select COUNT(1) FROM instance_2 where not name = 'visq' and not name = 'werf' and type='adc')
as adc from dual;

# Find the top 5 estate agents who have sold the most
# (include their contact details and their sales details so that it is easy
# contact them and congratulate them).
"""
SELECT a.agent_id, a.first_name, a.last_name, a.email, a.phone_number, COUNT(l.listing_id) as number_listing FROM agents a
JOIN listings l on a.agent_id = l.agent_id
JOIN sales s on l.listing_id = s.listing_id
GROUP BY agent_id
ORDER BY number_listing
LIMIT 5
"""

# Calculate the commission that each estate agent must receive
# and store the results in a separate table.
"""
SELECT l.agent_id, SUM(s.commission) FROM sales s
JOIN listings l on s.listing_id = l.listing_id
GROUP BY agent_id
"""

# For all houses that were sold that month, calculate the average
# number of days that the house was on the market.


# For all houses that were sold that month, calculate the average selling price


# Find the zip codes with the top 5 average sales prices
"""
SELECT h.zipcode, AVG(s.selling_price) FROM houses h
JOIN listings l on h.house_id = l.house_id
JOIN sales s on l.listing_id = s.listing_id
GROUP BY h.zipcode
ORDER BY AVG(s.selling_price) DESC
LIMIT 5
"""