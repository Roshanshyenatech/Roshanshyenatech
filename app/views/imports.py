from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.core.exceptions import ValidationError
import django.dispatch
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from django.utils import timezone
from django.core.mail import send_mail
import random
import requests
# imports .
import uuid
# from .signals import *
# from .decorators import *

from app.encode import encode_auth_token
from app.decode import decode_auth_token
# from api_app.views.serializer import *
# from api_app.views.helping_function import *

# from .password_decode import decode_password_token
# from .password_encode import encode_password_token

import datetime
# from project.settings import EMAIL_HOST_USER
import json
import time
#tmodels
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status

from app.models.customer import *
from app.models.roles import *
from django.core.mail import send_mail
