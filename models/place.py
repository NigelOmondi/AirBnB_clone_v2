#!/usr/bin/python3
""" Place Module for HBNB project """
import models
from models.base_model import BaseModel, Base
from models.amenity import Amenity
from models.review import Review
from sqlalchemy import String, Integer, Float, ForeignKey, Column, Table
from sqlalchemy.orm import relationship
from os import getenv

place_amenity = Table("place_amenity", Base.metadata,
                      Column("place_id", String(60),
                             ForeignKey("places.id"),
                             primary_key=True, nullable=False),
                      Column("amenity_id", String(60),
                             ForeignKey("amenities.id"),
                             primary_key=True, nullable=False))


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
    amenities = relationship("Amenity", secondary=place_amenity,
                             viewonly=False, backref="place_amenities")
    amenity_ids = []

    if getenv("HBNB_TYPE_STORAGE", None) != "db":
        @property
        def reviews(self):
            """Return a list of review instances"""
            review_values = models.storage.all(Review).values()
            review_list = []
            for review in review_values:
                if review.place_id == self.id:
                    review_list.append(review)
            return review_list

        @property
        def amenities(self):
            """Get/set linked Amenities."""
            amenityList = []
            for amenity in list(models.storage.all(Amenity).values()):
                if amenity.id in self.amenity_ids:
                    amenityList.append(amenity)
            return amenityList

        @amenities.setter
        def amenities(self, value):
            if type(value) is Amenity:
                self.amenity_ids.append(value.id)
