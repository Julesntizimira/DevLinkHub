#!/usr/bin/python3
'''define rate Model'''
from .basemodel import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, CheckConstraint, Boolean


class Rate(BaseModel, Base):
    '''class Rate Model'''
    __tablename__ = 'rates'
    profile_id = Column(String(60), ForeignKey('profiles.id', ondelete='SET NULL'), nullable=True)
    project_id = Column(String(60), ForeignKey('projects.id', ondelete='CASCADE'), nullable=False)
    is_upvote = Column(Boolean, nullable=False, default=False)
    __table_args__ = (
        CheckConstraint(is_upvote.in_([True, False]), name='valid_is_upvote'),
    )

    def __init__(self, *args, **kwargs):
        """initializes Rate instance"""
        super().__init__(*args, **kwargs)