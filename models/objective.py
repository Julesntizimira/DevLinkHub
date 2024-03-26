#!/usr/bin/python3
'''user and profile model'''
from .basemodel import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey


class Objective(BaseModel, Base):
    '''objectives'''
    __tablename__ = 'objectives'
    text = Column(String(2000), nullable=False)
    project_id = Column(String(60), ForeignKey('projects.id'), nullable=False)
    subtitle_id = Column(String(60), ForeignKey('subtitles.id'), nullable=True)

    def __init__(self, *args, **kwargs):
        """initializes objective"""
        super().__init__(*args, **kwargs)