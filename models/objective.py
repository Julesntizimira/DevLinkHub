#!/usr/bin/python3
'''define Objective model'''
from .basemodel import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey


class Objective(BaseModel, Base):
    '''objective Model'''
    __tablename__ = 'objectives'
    text = Column(String(2000), nullable=False)
    project_id = Column(String(60), ForeignKey('projects.id'), nullable=False)
    subtitle_id = Column(String(60), ForeignKey('subtitles.id'), nullable=True)

    def __init__(self, *args, **kwargs):
        """initializes Objective instance"""
        super().__init__(*args, **kwargs)