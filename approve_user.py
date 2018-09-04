#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Created by Roberto Preste
from app import db, app
import argparse
from flask import render_template
from flask_mail import Message
from config import ADMINS
from app import app, mail
from app.site.models import User
# from app.site.scripts import send_email

## Usage: python approve_user.py <username>


parser = argparse.ArgumentParser("""Approve a specific user.""")
parser.add_argument("user", help="Username of the user to approve. ")
args = parser.parse_args()

u = User.query.filter(User.username == args.user).first()
u.set_approval()

msg = Message(subject="[My Database] User %s approved" % u.username,
              sender=ADMINS[0],
              recipients=[u.email, ADMINS[0]])

with app.app_context():
    msg.body = render_template("registr_confirm.txt",
                               first_name=u.first_name,
                               username=u.username)
    mail.send(msg)

print("User %s approved. " % args.user)