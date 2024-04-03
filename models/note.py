#!/usr/bin/python3
''' define Note model '''
from models.basemodel import BaseModel, Base
from sqlalchemy import Column, String, Text, ForeignKey


class Note(BaseModel, Base):
    '''Note model class'''
    __tablename__ = 'notes'
    project_id = Column(String(60), ForeignKey('projects.id', ondelete='CASCADE'), nullable=False)
    profile_id = Column(String(60), ForeignKey('profiles.id', ondelete='SET NULL'), nullable=True)
    text = Column(Text, nullable=True)

    def __init__(self, *args, **kwargs):
        """initializes Note instance"""
        super().__init__(*args, **kwargs)
