import json
import string
import random
import re
from flask import jsonify
from functools import wraps
from flask import session
from datetime import datetime


def return_error(error="SOMETHING_WENT_WRONG", message="Error", data={}, code=200):
    return jsonify({"success": False, "error": error, "message": message, "data": data})


def return_success(data={}, status="SUCCESS", code=200):
    if isinstance(data, (dict, list)):
        if isinstance(data, (list)):
            l_data = {}
            l_data['status'] = status
            l_data['data'] = data
            return jsonify({"success": True, "data": l_data})
        if data.get('status', False):
            return jsonify({"success": True, "data": data})
        else:
            data['status'] = status
            return jsonify({"success": True, "data": data})
    else:
        raise Exception(f'data obj must be list or dict but got {type(data)}')


def logged_in(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        email = session.get("email", None)
        if email:
            return f(*args, **kwargs)
        else:
            return return_error('LOGIN_REQUIRED', "Session not found login again")

    return decorated_func


def generate_random_string(N=7):
    res = ''.join(random.choices(
        string.ascii_lowercase + string.ascii_uppercase + string.digits + str(datetime.now().timestamp()).split('.')[0],
        k=N))
    return res



def month_id_to_datetime(month_id):
    # Extract month and year components from the string
    month = int(month_id[:2])
    year = int(month_id[2:])

    # Create a new datetime object with the 1st day of the month
    first_day_of_month = datetime(year, month, 1)
    return first_day_of_month

def datetime_to_month_id(dt_obj):
  

    return dt_obj.strftime("%B %Y")

   


def month_year(input_string):
    date_obj = datetime.strptime(input_string, "%Y-%m-%d")
    formatted_date = date_obj.strftime("%Y-%b")
    return formatted_date


regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'


def valid_email(email):
    try:
        if (re.fullmatch(regex, email)):
            return True
        else:
            return False
    except:
        return False

