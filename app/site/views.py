#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Created by Roberto Preste
import requests
import json
from flask import Blueprint, render_template, flash, redirect, session, url_for, request, g, jsonify, send_file
from werkzeug.urls import url_parse

www = Blueprint("site", __name__)

from sqlalchemy import or_, and_
from app import app, db
from config import ADMINS
from flask_login import current_user, login_user, logout_user, login_required
from .forms import LoginForm, RegistrationForm
from .models import User
from app.static import dbdata


# Home Page
@www.route("/index", methods=["GET"])
@www.route("/home", methods=["GET"])
@www.route("/", methods=["GET"])
def index():
    return render_template("index.html",
                           title="My Database",
                           latest_update=dbdata.latest_update)


@www.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if request.method == "GET":

        # expl: if user is already logged in, return to the home page
        if current_user.is_authenticated:
            return redirect(url_for("site.index"))

        return render_template("login.html", title="Log In", form=form)

    elif request.method == "POST":

        if form.validate_on_submit():
            user = User.query.filter(User.username == form.username.data).first()

            if not user.approved:
                flash("User not confirmed yet. Please wait for the approval email.")
                return redirect(url_for("site.index"))

            # expl: if user does not exist or the entered password is wrong
            if user is None or not user.check_password(form.password.data):
                flash("Invalid username or password!")
                return redirect(url_for("site.login"))

            login_user(user)
            user.update_last_access()
            next_page = request.args.get("next")

            # expl: check that the url sent is relative, to avoid external urls
            if not next_page or url_parse(next_page).netloc != "":
                next_page = "index"

            return redirect(url_for("site." + next_page.lstrip("/").lstrip("%252F")))


@www.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("site.index"))


@www.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()

    if request.method == "GET":

        if current_user.is_authenticated:
            return redirect(url_for("site.index"))

        return render_template("register.html", title="Registration", form=form)

    elif request.method == "POST":

        # expl: a series of checks, since the internal ones don't seem to work properly
        if User.query.filter(User.email == form.email.data).first():
            flash("Email address already used. Please choose a different email address.")
            return redirect(url_for("site.register"))

        if User.query.filter(User.username == form.username.data).first():
            flash("Username existing. Please choose a different username.")
            return redirect(url_for("site.register"))

        if form.password.data != form.password2.data:
            flash("Passwords must match. Please check again. ")
            return redirect(url_for("site.register"))

        if form.validate_on_submit():

            user = User(username=form.username.data, email=form.email.data,
                        first_name=form.first_name.data, last_name=form.last_name.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            send_email("[My Database]User {} registered.".format(form.username.data),
                       ADMINS[0],
                       [form.email.data, ADMINS[0]],
                       render_template("registr_request.txt",
                                       first_name=form.first_name.data,
                                       username=form.username.data,
                                       email=form.email.data))
            flash("Registration complete! You will be notified when your request is approved.")

            # expl: if the following lines are commented, approval is needed, using approve_user.py
            user.set_approval()
            send_email("[My Database] User {} approved".format(form.username.data),
                       ADMINS[0],
                       [form.email.data, ADMINS[0]],
                       render_template("registr_confirm.txt",
                                       first_name=form.first_name.data,
                                       username=form.username.data,
                                       email=form.email.data))

            return redirect(url_for("site.index"))


@www.errorhandler(404)
def page_not_found(e):
    return render_template("404.html", title="Error 404"), 404


@www.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html", title="Error 500"), 500

