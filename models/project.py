#!/usr/bin/python3
'''define Project and Tag model'''
from .basemodel import BaseModel, Base
from sqlalchemy import Column, String, Text, ForeignKey, Integer, Table
from sqlalchemy.orm import relationship


# define Project and Tag many to many relationship
project_tag = Table('project_tag', Base.metadata,
                    Column('project_id', String(60),
                    ForeignKey('projects.id', onupdate='CASCADE', ondelete='CASCADE'),
                    primary_key=True), 
                    Column('tag_id', String(60),
                    ForeignKey('tags.id', onupdate='CASCADE', ondelete='CASCADE'),
                    primary_key=True))


class Project(BaseModel, Base):
    '''Project Model class'''
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
    links = relationship("Link", backref="project", cascade="all, delete-orphan")
    objectives = relationship("Objective", backref="project", cascade="all, delete-orphan")
    takeaways = relationship("Takeaway", backref="project", cascade="all, delete-orphan")
    subtitles = relationship("Subtitle", backref="project", cascade="all, delete-orphan")

    def __init__(self, *args, **kwargs):
        """initializes Project instance"""
        super().__init__(*args, **kwargs)


class Tag (BaseModel, Base):
    '''Tag model class'''
    __tablename__ = 'tags'
    name =  Column(String(200), nullable=False)

    def __init__(self, *args, **kwargs):
        """initializes Tag instance"""
        super().__init__(*args, **kwargs)
    
    @property
    def projects(self):
        '''get projects related to this tag'''
        from models import storage
        projects = []
        for project in storage.all(Project).values():
            if self in project.tags:
                projects.append(project)
        return projects