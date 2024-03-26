#!/usr/bin/python3
'''user and profile model'''
from models.basemodel import BaseModel, Base
from sqlalchemy import Column, String, Text, ForeignKey, Boolean, Table
from sqlalchemy.orm import relationship
from .user import User

class Message(BaseModel, Base):
    __tablename__ = 'messages'
    message = Column(Text, nullable=True)
    subject = Column(String(200), nullable=True)
    is_read = Column(Boolean, default=False)

    # Define sender relationship
    sender_id = Column(String(60), ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    sender = relationship('User', foreign_keys=[sender_id], backref='sent_messages')

    # Define receiver relationship
    receiver_id = Column(String(60), ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    receiver = relationship('User', foreign_keys=[receiver_id], backref='received_messages')


    def __init__(self, *args, **kwargs):
        """initializes Message"""
        super().__init__(*args, **kwargs)
    
        