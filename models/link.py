#!/usr/bin/python3
'''user and profile model'''
from .basemodel import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey


class Link(BaseModel, Base):
    '''Link model'''
    __tablename__ = 'links'
    name = Column(String(200), nullable=False)
    url = Column(String(2000), nullable=False)
    project_id = Column(String(60), ForeignKey('projects.id'), nullable=False)

    def __init__(self, *args, **kwargs):
        """initializes Link instance"""
        super().__init__(*args, **kwargs)