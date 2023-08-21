#!/usr/bin/python3
""" State Module for HBNB project """
import models
from models.base_model import BaseModel, Base
from sqlalchemy import String, Column
from models.city import City
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
	""" State class """
	__tablename__ = "states"
	name = Column(String(128, nullable=False))
	cities = relationship("City", backref="state", cascade="delete")

	@property
	def cities(self):
		"""Returns the list of City instances
		with state_id equals to the current. """

		allCities = models.storage.all(City)

		return [city for city in allCities.values() if city.state_id == self.id]
