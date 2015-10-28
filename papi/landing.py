#!/usr/bin/python
#
from flask import render_template
from papi import api

@api.route('/')
def index():
    user = "Anonymous"
    return render_template('index.html',
                           title='Lander',
                           user=user)

# @dogstore.route('/api')
