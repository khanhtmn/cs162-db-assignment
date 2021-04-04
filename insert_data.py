import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import datetime
from create import Office, OfficeArea, AreaEnum, House, Seller, Buyer, Agent, AgentOffice, Listing, Sale, StatusEnum,Float

from services import calc_commission

engine = create_engine('sqlite:///database.db', echo=True)
engine.connect()

# Insert data
Session = sessionmaker(bind=engine)
session = Session()

try:
    session.add(Office(office_id = 1, office_name = "Magical Land 01", office_area = AreaEnum.east))
    session.add(Office(office_id = 2, office_name = "Magical Land 02", office_area = AreaEnum.east))

    session.commit()
except:
    session.rollback()
    # raise
finally:
    session.close()

try:
    session.add(OfficeArea(office_id = 1, zipcode = 11010))
    session.add(OfficeArea(office_id = 1, zipcode = 11011))
    session.add(OfficeArea(office_id = 1, zipcode = 11012))
    session.add(OfficeArea(office_id = 2, zipcode = 22020))
    session.add(OfficeArea(office_id = 2, zipcode = 22021))

    session.commit()
except:
    session.rollback()
    # raise
finally:
    session.close()

try:
    session.add(House(house_id = 1, bedrooms = 1, bathrooms = 1, zipcode = 11010))
    session.add(House(house_id = 2, bedrooms = 2, bathrooms = 1, zipcode = 11010))
    session.add(House(house_id = 3, bedrooms = 2, bathrooms = 2, zipcode = 11010))
    session.add(House(house_id = 4, bedrooms = 1, bathrooms = 1.5, zipcode = 22020))

    session.commit()
except:
    session.rollback()
    # raise
finally:
    session.close()

try:
    session.add(Seller(seller_id = 1, first_name = "Jessica", last_name = "Jung", email = "jess@jessisme.com", phone_number = "010-700-009"))
    session.add(Seller(seller_id = 2, first_name = "Timmothy", last_name = "Frank", email = "timmy007@mail.com", phone_number = "151-720-151"))
    session.add(Seller(seller_id = 3, first_name = "Khanh", last_name = "Tran", email = "hello@khanh.com", phone_number = "413-456-789"))

    session.commit()
except:
    session.rollback()
    # raise
finally:
    session.close()

try:
    session.add(Buyer(buyer_id = 1, first_name = "Ivy", last_name = "Chen", email = "poisonous_ivy@mail.com", phone_number = "222-111-009"))
    session.add(Buyer(buyer_id = 2, first_name = "Edward", last_name = "Choi", email = "eddiechoi@mail.com", phone_number ="444-111-189"))
    session.add(Buyer(buyer_id = 3, first_name = "David", last_name = "Park", email = "davidpark89@mail.com", phone_number = "435-157-079"))

    session.commit()
except:
    session.rollback()
    # raise
finally:
    session.close()

# Insert Agent data
try:
    session.add(Agent(agent_id = 1, first_name = "Michelle", last_name = "Brown", email = "michelle@magicalland.com", phone_number = "345-134-659"))
    session.add(Agent(agent_id = 2, first_name = "Rachel", last_name = "Lee", email = "rachel@magicalland.com", phone_number = "204-157-013"))
    session.add(Agent(agent_id = 3, first_name = "Jason", last_name = "Xu", email = "jason@magicalland.com", phone_number = "583-121-923"))

    session.commit()
except:
    session.rollback()
    # raise
finally:
    session.close()

# Insert AgentOffice data
try:
    session.add(AgentOffice(agent_id = 1, office_id = 1))
    session.add(AgentOffice(agent_id = 1, office_id = 2))
    session.add(AgentOffice(agent_id = 2, office_id = 1))
    session.add(AgentOffice(agent_id = 3, office_id = 2))

    session.commit()
except:
    session.rollback()
    # raise
finally:
    session.close()

# Insert Listing data
try:
    session.add(Listing(listing_id = 1, house_id = 1, seller_id = 1, agent_id = 1, office_id = 1, listing_price = 100000,
                        listing_date = datetime(2020,11, 1, 10, 0, 0), status = StatusEnum.available))
    session.add(Listing(listing_id = 2, house_id = 2, seller_id = 2, agent_id = 1, office_id = 1, listing_price = 200000,
                        listing_date = datetime(2020,11, 15, 10, 0, 0), status = StatusEnum.available))
    session.add(Listing(listing_id = 3, house_id = 3, seller_id = 3, agent_id = 1, office_id = 2, listing_price = 150000,
                        listing_date = datetime(2020,12, 1, 10, 0, 0), status = StatusEnum.available))

    session.commit()
except:
    session.rollback()
    # raise
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
        # raise
    finally:
        session.close()

update_sale(sale_id = 1, listing_id = 1, buyer_id = 1, selling_price = 95000, selling_date = datetime(2020,12, 15, 10, 0, 0))
update_sale(sale_id = 2, listing_id = 3, buyer_id = 2, selling_price = 145000, selling_date = datetime(2020,12, 30, 10, 0, 0))

# print("-------OFFICE---------")
# print(session.query(Office).all())
# print("-------OFFICE---------")

# print("-------OFFICE-AREA---------")
# print(session.query(OfficeArea).all())
# print("-------OFFICE-AREA---------")

# print("-------HOUSE---------")
# print(session.query(House).all())
# print("-------HOUSE---------")

# print("-------SELLER---------")
# print(session.query(Seller).all())
# print("-------SELLER---------")

# print("-------BUYER---------")
# print(session.query(Buyer).all())
# print("-------BUYER---------")

# print("-------AGENT---------")
# print(session.query(Agent).all())
# print("-------AGENT---------")

# print("-------AGENT-OFFICE---------")
# print(session.query(AgentOffice).all())
# print("-------AGENT-OFFICE---------")

# print("-------LISTING---------")
# print(session.query(Listing).all())
# print("-------LISTING---------")

# print("-------SALE---------")
# print(session.query(Sale).all())
# print("-------SALE---------")
