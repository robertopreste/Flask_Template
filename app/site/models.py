#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Created by Roberto Preste
from datetime import datetime
from threading import Thread
from app import db, login, mail, app
from flask import render_template
from flask_login import UserMixin
from flask_mail import Message
from werkzeug.security import generate_password_hash, check_password_hash
from config import ADMINS


class User(UserMixin, db.Model):
    __tablename__ = "User"

    id = db.Column(db.Integer, nullable=False, autoincrement=True, primary_key=True)
    username = db.Column(db.String, index=True, unique=True, nullable=False)
    email = db.Column(db.String, index=True, unique=True, nullable=False)
    first_name = db.Column(db.String, nullable=True, default=None)
    last_name = db.Column(db.String, nullable=True, default=None)
    password_hash = db.Column(db.String)
    registr_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_access = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    approved = db.Column(db.Boolean, default=False)
    downloads = db.relationship("Downloads", backref="User", lazy="dynamic")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_approval(self):
        self.approved = True
        db.session.commit()

    def unset_approval(self):
        self.approved = False
        db.session.commit()

    def update_last_access(self):
        self.last_access = datetime.utcnow()
        db.session.commit()

    def __repr__(self):
        return """User(id: {self.id}, username: {self.username})""".format(self=self)


class Downloads(db.Model):
    __tablename__ = "Downloads"

    id = db.Column(db.Integer, nullable=False, autoincrement=True, primary_key=True)
    dataset = db.Column(db.String, nullable=False)
    dl_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("User.id"), nullable=False)

    def __repr__(self):
        return """Downloads(id: {self.id}, dataset: {self.dataset}, dl_date: {self.dl_date}, user_id: {self.user_id})""".format(self=self)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
