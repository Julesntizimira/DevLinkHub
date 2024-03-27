#!/usr/bin/python3
'''subtitle model'''
from models.basemodel import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class Subtitle(BaseModel, Base):
    '''Subtitle model class'''
    __tablename__ = 'subtitles'
    text = Column(String(200), nullable=False)
    project_id = Column(String(60), ForeignKey('projects.id'), nullable=False)
    objectives = relationship("Objective", backref="subtitle", cascade="all, delete-orphan")

    def __init__(self, *args, **kwargs):
        """initializes Subtitle instance"""
        super().__init__(*args, **kwargs)