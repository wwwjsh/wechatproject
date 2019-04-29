# coding: utf-8
from sqlalchemy import CHAR, Column, DateTime, Enum, ForeignKey, String, TIMESTAMP, Time, text
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.INTEGER(5), primary_key=True)
    nickname = db.Column(db.String(30))
    openid = db.Column(db.CHAR(128))
    unionid = db.Column(db.CHAR(128))
    session_key = db.Column(db.CHAR(128))
    address = db.Column(db.String(60))
    phone = db.Column(db.CHAR(11))


class Item(Base):
    __tablename__ = 'items'

    item_id = db.Column(db.INTEGER(5), primary_key=True)
    pass_id = db.Column(db.CHAR(10), nullable=False, unique=True)
    lau_usId = db.Column(db.ForeignKey('users.id'), index=True)
    item_type = db.Column(db.Enum('1', '2'), nullable=False)
    contacts = db.Column(db.String(20), nullable=False)
    start_time = db.Column(db.TIMESTAMP, nullable=False)
    end_time = db.Column(db.TIMESTAMP, nullable=False)
    item_address = db.Column(db.String(60))
    text_info = db.Column(db.String(150))
    img_info = db.Column(db.String(100))
    lau_time = db.Column(db.TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))

    user = relationship('User')


class OrdObject(Base):
    __tablename__ = 'ord_objects'

    obj_id = db.Column(db.INTEGER(5), primary_key=True)
    itemId = db.Column(db.ForeignKey('items.item_id'), index=True)
    obj_num = db.Column(db.INTEGER(3))
    obj_name = db.Column(db.String(15), nullable=False)
    minOrd_time = db.Column(db.Time)
    startOrd_time = db.Column(db.DateTime, nullable=False)
    Ordable_sum = db.Column(db.INTEGER(3), nullable=False)
    residue = db.Column(db.INTEGER(3), nullable=False)
    logic_del = db.Column(db.INTEGER(1), server_default=text("'1'"))

    item = db.relationship('Item')


class Order(Base):
    __tablename__ = 'orders'

    ord_id = db.Column(db.INTEGER(8), primary_key=True)
    ord_num = db.Column(db.INTEGER(5), nullable=False)
    objId = db.Column(db.ForeignKey('ord_objects.obj_id'), index=True)
    ord_usId = db.Column(db.ForeignKey('users.id'), index=True)
    queue_num = db.Column(db.INTEGER(3), server_default=text("'-1'"))
    place_time = db.Column(db.TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))

    ord_object = db.relationship('OrdObject')
    user = db.relationship('User')
