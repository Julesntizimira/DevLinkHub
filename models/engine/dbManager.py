#!/usr/bin/python3
'''Manage db storage system'''
from models.basemodel import Base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine
from models.user import User, Profile
from models.rate import Rate
from models.skill import Skill
from models.project import Project, Tag
from models.comment import Comment


classes = {
    'User': User,
    'Profile': Profile,
    'Rate': Rate,
    'Skill': Skill,
    'Tag': Tag,
    'Project': Project,
    'Comment': Comment
}


class DbManager():
    '''handle all Db management'''
    __engine = None
    __session = None

    def __init__(self, *args, **kwargs):
        '''constructor method'''
        self.__engine = create_engine('sqlite:///devdb.db')
    
    def new(self, obj):
        '''add new object to the database'''
        self.__session.add(obj)
    
    def save(self):
        '''save changes to the database'''
        self.__session.commit()
    
    def delete(self, obj):
        '''delete an object from the database'''
        if obj:
            self.__session.delete(obj)
            self.__session.commit()


    def reload(self):
        '''create database session'''
        Base.metadata.create_all(bind=self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(session_factory)
    
    def all(self, cls=None):
        """query on the current database session"""
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return (new_dict)
    
    def get(self, cls, id):
        '''get a class instance using id'''
        for obj in self.all(cls).values():
            if id == obj.id:
                return obj
    
    def count(self, cls):
        '''count the number of specific object in database'''
        new_dict =  self.all(cls)
        return len(new_dict)
    
    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()
