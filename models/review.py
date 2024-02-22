#!/usr/bin/python3
""" Review module for the HBNB project """
from models.base_model import BaseModel, Base
from models.user import User
from models.place import Place
from sqlalchemy import Column, String, ForeignKey, Integer, Float


class Review(BaseModel, Base):
    """ Review classto store review information """
    __tablename__ = "reviews"

    place_id = Column(String(60), ForeignKey(Place.id), nullable=False)
    user_id = Column(String(60), ForeignKey(User.id), nullable=False)
    text = Column(String(1024), nullable=False)
