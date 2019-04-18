# coding: utf-8
from sqlalchemy import CHAR, Column, DateTime, Enum, ForeignKey, String, TIMESTAMP, Time, text
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class User(Base):
    __tablename__ = 'users'

    id = Column(INTEGER(5), primary_key=True)
    nickname = Column(String(30))
    openid = Column(CHAR(128))
    unionid = Column(CHAR(128))
    session_key = Column(CHAR(128))
    address = Column(String(60))
    phone = Column(CHAR(11))


class Item(Base):
    __tablename__ = 'items'

    item_id = Column(INTEGER(5), primary_key=True)
    pass_id = Column(CHAR(10), nullable=False, unique=True)
    lau_usId = Column(ForeignKey('users.id'), index=True)
    item_type = Column(Enum('1', '2'), nullable=False)
    contacts = Column(String(20), nullable=False)
    start_time = Column(TIMESTAMP, nullable=False)
    end_time = Column(TIMESTAMP, nullable=False)
    item_address = Column(String(60))
    text_info = Column(String(150))
    img_info = Column(String(100))
    lau_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))

    user = relationship('User')


class OrdObject(Base):
    __tablename__ = 'ord_objects'

    obj_id = Column(INTEGER(5), primary_key=True)
    itemId = Column(ForeignKey('items.item_id'), index=True)
    obj_num = Column(INTEGER(3))
    obj_name = Column(String(15))
    minOrd_time = Column(Time)
    startOrd_time = Column(DateTime, nullable=False)
    Ordable_sum = Column(INTEGER(3), nullable=False)
    residue = Column(INTEGER(3), nullable=False)
    logic_del = Column(INTEGER(1), server_default=text("'1'"))

    item = relationship('Item')


class Order(Base):
    __tablename__ = 'orders'

    ord_id = Column(INTEGER(8), primary_key=True)
    ord_num = Column(INTEGER(5), nullable=False)
    objId = Column(ForeignKey('ord_objects.obj_id'), index=True)
    ord_usId = Column(ForeignKey('users.id'), index=True)
    queue_num = Column(INTEGER(3), server_default=text("'-1'"))
    place_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))

    ord_object = relationship('OrdObject')
    user = relationship('User')
