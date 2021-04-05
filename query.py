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
