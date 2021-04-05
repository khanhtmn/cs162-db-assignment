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
