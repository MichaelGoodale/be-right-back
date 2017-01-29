#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, request
from random import randint
import model_interface
# A constant referring to the dictionary to use.
get_sentence = model_interface.get_reply

# Initialize the Flask app.
application = Flask(__name__)

# The main and only route.
@application.route("/")
def main():
	sentence = request.args.get("sentence")
	return get_sentence(sentence)

