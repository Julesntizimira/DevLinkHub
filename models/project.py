#!/usr/bin/python3
'''user and profile model'''
from .basemodel import BaseModel, Base
from sqlalchemy import Column, String, Boolean, Text, ForeignKey, Integer, Table
from sqlalchemy.orm import relationship
from .comment import Comment
from .rate import Rate


project_tag = Table('project_tag', Base.metadata,
                    Column('project_id', String(60),
                    ForeignKey('projects.id', onupdate='CASCADE', ondelete='CASCADE'),
                    primary_key=True), 
                    Column('tag_id', String(60),
                    ForeignKey('tags.id', onupdate='CASCADE', ondelete='CASCADE'),
                    primary_key=True))


class Project(BaseModel, Base):
    __tablename__ = 'projects'
    user_id = Column(String(60), ForeignKey('users.id'), nullable=True)
    title = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)
    demo_link = Column(String(2000), nullable=True)
    source_link = Column(Text, nullable=True)
    vote_ratio = Column(Integer, nullable=True)
    vote_count = Column(Integer, nullable=True)
    image_url = Column(String(2000), default='images/default.jpg')
    tags = relationship("Tag", secondary=project_tag, viewonly=False)
    comments = relationship("Comment", backref="project", cascade="all, delete-orphan")
    rates = relationship("Rate", backref="project", cascade="all, delete-orphan")

    def __init__(self, *args, **kwargs):
        """initializes project"""
        super().__init__(*args, **kwargs)


class Tag (BaseModel, Base):
    __tablename__ = 'tags'
    name =  Column(String(200), nullable=False)

    def __init__(self, *args, **kwargs):
        """initializes Tag"""
        super().__init__(*args, **kwargs)