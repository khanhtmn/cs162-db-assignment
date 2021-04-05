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
