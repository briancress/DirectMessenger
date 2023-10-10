"""Module for protocol for communicating with dsu server"""
# ds_protocol.py

import json
from collections import namedtuple

# Namedtuple to hold the values retrieved from json messages.
DataTuple = namedtuple('DataTuple', ['response', 'token'])


def extract_json(json_msg: str) -> DataTuple:
    '''
    Call the json.loads function on a json string and convert it to a DataTuple object

    TODO: replace the pseudo placeholder keys with actual DSP protocol keys
    '''
    try:
        json_obj = json.loads(json_msg)
        response = json_obj['response']
        token = json_obj['response']['token']
    except json.JSONDecodeError:
        print("Json cannot be decoded.")
        return False
    except KeyError:
        print('There was an error communicating with the server')
        return False
    except UnboundLocalError:
        print('There was an error')
        return False

    return DataTuple(response, token)


def extract_dm(json_msg: str):
    """Extracts json message"""
    try:
        json_obj = json.loads(json_msg)
        response = json_obj['response']

    except json.JSONDecodeError:
        print("Json cannot be decoded.")
        return False
    except KeyError:
        print('There was an error communicating with the server')
        return False
    except AttributeError:
        print('Error')
        return False

    return response


def join(username, password):
    """creates json format for username and password"""
    username = '"' + username + '"'
    password = '"' + password + '"'
    j_temp = '{"join": {"username": {username},"password": {password},"token":""}}'
    j_temp = j_temp.replace('{username}', username)
    j_temp = j_temp.replace('{password}', password)

    return j_temp


def dm_send(message, recipient, token, timestamp):
    """ Send a directmessage to another DS user (in the example bellow, ohhimark)"""
    d_m = '{"token":"{user_token}", "directmessage": {"entry": "{message}","recipient":"{recipient}", "timestamp": "{timestamp}"}}'
    d_m = d_m.replace('{user_token}', token)
    d_m = d_m.replace('{message}', message)
    d_m = d_m.replace('{recipient}', recipient)
    d_m = d_m.replace('{timestamp}', timestamp)
    return d_m


def unread(token):
    """Request unread messages from the DS server"""
    d_m = '{"token":"{token}", "directmessage": "new"}'
    d_m = d_m.replace('{token}', token)
    return d_m


def unread_all(token):
    """Request all messages from the DS server"""
    d_m = '{"token":"{token}", "directmessage": "all"}'
    d_m = d_m.replace('{token}', token)
    return d_m
