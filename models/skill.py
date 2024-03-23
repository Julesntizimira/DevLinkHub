#!/usr/bin/python3
'''user and profile model'''
from models.basemodel import BaseModel, Base
from sqlalchemy import Column, String, Text, ForeignKey


class Skill(BaseModel, Base):
    __tablename__ = 'skills'
    profile_id = Column(String(60), ForeignKey('profiles.id'), nullable=True)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)

    def __init__(self, *args, **kwargs):
        """initializes Skill"""
        super().__init__(*args, **kwargs)