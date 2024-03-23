#!/usr/bin/python3
'''comment model'''
from models.basemodel import BaseModel, Base
from sqlalchemy import Column, String, Text, ForeignKey


class Comment(BaseModel, Base):
    __tablename__ = 'comments'
    project_id = Column(String(60), ForeignKey('projects.id', ondelete='CASCADE'), nullable=False)
    profile_id = Column(String(60), ForeignKey('profiles.id', ondelete='SET NULL'), nullable=True)
    text = Column(Text, nullable=True)

    def __init__(self, *args, **kwargs):
        """initializes Comment"""
        super().__init__(*args, **kwargs)