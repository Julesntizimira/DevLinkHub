#!/usr/bin/python3
'''base model to be inherited form by other bases'''
from sqlalchemy.orm import DeclarativeBase
from uuid import uuid4
from sqlalchemy import Column, String, DateTime
from datetime import datetime



time = "%B %d, %Y, %I:%M %p"

class Base(DeclarativeBase):
    pass


class BaseModel():
    id = Column(String(60), primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        '''constructor'''
        if kwargs:
            for attr, val in kwargs.items():
                if attr != '__class__':
                    setattr(self, attr, val)
            if kwargs.get('id', None) is None:
                self.id = str(uuid4())
            if kwargs.get('created_at', None) and type(self.created_at) is str:
                self.created_at = datetime.strptime(kwargs['created_at'], time)
            else:
                self.created_at = datetime.utcnow()
            if kwargs.get('updated_at', None) and type(self.updated_at) is str:
                self.updated_at = datetime.strptime(kwargs['updated_at'], time)
            else:
                self.updated_at = datetime.utcnow()
        else:
            self.id = str(uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = self.created_at
    

    def save(self):
        '''save newly or updated obj'''
        from . import storage
        self.updated_at = datetime.utcnow()
        if self.__class__.__name__ == 'User':
            self.profile.save()
        storage.new(self)
        storage.save()
    
    def to_dict(self):
        '''convert an object into a dictionary'''
        new_dict = {attr: val for attr, val in self.__dict__.copy().items() if not isinstance(val, BaseModel) }
        if "created_at" in new_dict:
            new_dict["created_at"] = new_dict["created_at"].strftime(time)
        if "updated_at" in new_dict:
            new_dict["updated_at"] = new_dict["updated_at"].strftime(time)
        new_dict["__class__"] = self.__class__.__name__
        if "_sa_instance_state" in new_dict:
            del new_dict["_sa_instance_state"]
        return new_dict
    
    def __str__(self):
        dict_to_list = [f'{attr}: {val}' for attr, val in self.to_dict().items()]
        list_to_str = ", ".join(dict_to_list)
        return f'[{self.__class__.__name__}.{self.id}] ({list_to_str})'
    
    def delete(self):
        from . import storage
        if self.__class__.__name__ == 'Profile':
            user = self.user
            storage.delete(user)
        else:
            storage.delete(self)