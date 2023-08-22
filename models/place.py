#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from models.city import City
from models.review import Review
from models.user import User
from os import getenv
from sqlalchemy import String, Integer, Float, ForeignKey, Column
from sqlalchemy.orm import relationship


class Place(BaseModel, Base):
    """The class Place"""

    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, default=0, nullable=False)
    number_bathrooms = Column(Integer, default=0, nullable=False)
    max_guest = Column(Integer, default=0, nullable=False)
    price_by_night = Column(Integer, default=0, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    amenity_ids = []
    reviews = relationship("Review", backref="place", cascade="delete")

    @property
	def reviews(self):
      """Return a list of review instances"""
        review_values = models.storage.all("Review").values()
        review_list = []
		for review in review_values:
            if review.place_id == self.id:
                review_list.append(review)
        return review_list
