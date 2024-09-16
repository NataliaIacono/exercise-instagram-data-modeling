import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Enum
from enum import Enum as PyEnum
from datetime import datetime
from enums import MediaTypeEnum 

from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er
# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy

# models = Flask(__name__)
# models.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/test.db"
# db = SQLAlchemy(models)

Base = declarative_base()

class Usuario(Base):
    __tablename__="usuario"
    id = Column(Integer, primary_key=True)
    nombre=Column(String, nullable=False)
    nombre_usuario=Column(String, nullable=False)
    apellido=Column(String, nullable=False)
    email=Column(String, nullable=False)
    relacion_post=relationship("Post", backref="usuario")
    relacion_follower=relationship("Follower", backref="usuario")
    relacion_comment=relationship("Comment", backref="usuario")
    
class Post(Base):
    __tablename__="post"
    id = Column(Integer, primary_key=True)  
    user_id= Column(Integer, ForeignKey("usuario.id"))
    relacion_media=relationship("Media", backref="Post")
    relacion_comment=relationship("Comment", backref="Post")
    
 
class Follower(Base):
    __tablename__ = "follower"
    user_from_id = Column(Integer, ForeignKey("usuario.id"), primary_key=True)
    user_to_id = Column(Integer, ForeignKey("usuario.id"), primary_key=True)

    
class Media(Base):
    __tablename__="media"
    id=Column(Integer, primary_key=True)
    type = Column(Enum(MediaTypeEnum, name="media_type_enum"), nullable=False)
    url=Column(String)
    post_id= Column(Integer, ForeignKey("post.id"))
   

class Comment(Base):
    __tablename__="comment"
    id = Column(Integer, primary_key=True)
    comment_text=Column(String)
    author_id = Column(Integer, ForeignKey("usuario.id"))
    post_id= Column(Integer, ForeignKey("post.id"))
   

    #usuario = relationship(Usuario) establece que cada comentario está asociado a un usuario que lo ha escrito.
    #post = relationship(Post) indica que cada comentario está asociado a un post específico.



    # def to_dict(self):
    #     return {}

   # Configura tu motor de base de datos aquí
engine = create_engine('sqlite:///:memory:')
Base.metadata.create_all(engine) 


## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
