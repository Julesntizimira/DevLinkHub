#!/usr/bin/python3
'''user and profile model'''
from models.basemodel import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey


class Takeaway(BaseModel, Base):
    __tablename__ = 'takeaways'
    text = Column(String(200), nullable=False)
    project_id = Column(String(60), ForeignKey('projects.id'), nullable=False)
 

    def __init__(self, *args, **kwargs):
        """initializes Skill"""
        super().__init__(*args, **kwargs)