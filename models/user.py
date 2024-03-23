#!/usr/bin/python3
'''user and profile model'''
from models.basemodel import BaseModel, Base
from sqlalchemy import Column, String, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from .skill import Skill
from .rate import Rate
from .comment import Comment
from .project import Project
from flask_login import UserMixin


class Profile(BaseModel, Base):
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


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class User(BaseModel, Base, UserMixin):
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
        """initializes User"""
        super().__init__(*args, **kwargs)
        if kwargs:
            if kwargs.get('profile', None) is None:
                self.profile = Profile(
                    username=self.username,
                    email=self.email,
                    user_id=self.id,
                    name=self.name,
                    )
        else:
            self.profile = Profile(
                username=self.username,
                email=self.email,
                user_id=self.id,
                name=self.name,
                )


