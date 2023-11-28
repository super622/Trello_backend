
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Card(Base):
    __tablename__ = 'tbl_card'

    id = Column(Integer, primary_key=True, index=True)
    # listId = Column(Integer, ForeignKey('tbl_list.id'))
    parentId = Column(Integer)
    title = Column(String)

class Comment(Base):
    __tablename__ = 'tbl_comments'

    id = Column(Integer, primary_key=True, index=True)
    comment = Column(String)
    cardId = Column(Integer, ForeignKey('tbl_card.id'))

class Description(Base):
    __tablename__ = 'tbl_descriptions'

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    cardId = Column(Integer, ForeignKey('tbl_card.id'))

class List(Base):
    __tablename__ = 'tbl_list'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
