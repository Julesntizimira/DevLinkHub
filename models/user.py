#!/usr/bin/python3
'''defines user and profile model'''
from models.basemodel import BaseModel, Base
from sqlalchemy import Column, String, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from flask_login import UserMixin


class Profile(BaseModel, Base):
    '''Profile model class'''
    __tablename__ = 'profiles'
    user_id = Column(String(60), ForeignKey('users.id'))
    user = relationship("User", back_populates="profile")
    username = Column(String(150), nullable=False, unique=True)
    email = Column(String(150), nullable=False)
    name = Column(String(150), nullable=False)
    bio = Column(Text, nullable=True)
    location = Column(String(150), nullable=True)
    headline = Column(String(250), nullable=True)
    profile_image_url = Column(String(2000), default='images/profiles/user-default.png')
    social_github = Column(String(200), nullable=True)
    social_linkdin = Column(String(200), nullable=True)
    social_youtube = Column(String(200), nullable=True)
    social_twitter = Column(String(200), nullable=True)
    skills = relationship("Skill", backref="profile",
                          cascade="all, delete, delete-orphan")
    comments = relationship("Comment", backref="profile", cascade="all, delete-orphan")
    rates = relationship("Rate", backref="profile", cascade="all, delete-orphan")
    notes = relationship("Note", backref="profile", cascade="all, delete-orphan")


    def __init__(self, *args, **kwargs):
        '''initialise Profile instance'''
        super().__init__(*args, **kwargs)


class User(BaseModel, Base, UserMixin):
    '''User Model class'''
    __tablename__ = 'users'
    username = Column(String(150), nullable=False, unique=True)
    password = Column(String(150), nullable=False)
    email = Column(String(150), nullable=False)
    name = Column(String(150), nullable=False)
    is_staff = Column(Boolean, default=False)
    projects = relationship('Project', backref='user', cascade="all, delete-orphan")
    profile = relationship("Profile", uselist=False,
                           back_populates="user",
                           cascade="all, delete-orphan",
                           )
    
    def __init__(self, *args, **kwargs):
        """initializes User instance"""
        super().__init__(*args, **kwargs)
        if kwargs:
            if kwargs.get('profile', None) is None:
                self.profile = Profile(user_id=self.id)
        else:
            self.profile = Profile(user_id=self.id)
    
    @property
    def unread(self):
        '''return unread messages'''
        messages = sorted(self.received_messages, key=lambda x: x.created_at, reverse=True)
        unread = sum(1 for message in messages if not message.is_read)
        return unread

