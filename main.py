from flask import Flask, request, jsonify
from flask.views import MethodView
from datetime import datetime, timezone
from typing import Optional, List
import pydantic

app = Flask(__name__)