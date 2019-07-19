#!/usr/bin/python

import sys
from json import dumps
import time
from requests.sessions import Session
from simplejson import loads
from pprint import pprint

webservice = "http://192.168.2.178:1237/"
web_username = "system"
web_password = "sys"
_session = None

DEFAULT_HEADERS = {
    "Content-type": "application/json",
    "Accept": "application/json",
    "User-Agent": "ibs-jsonrpc",
    "Accept-Charset": "utf-8",
    "Cache-Control": "no-cache",
}


def _get_session():
    global _session
    if _session is None:
        _session = Session()
        _session.headers.update(DEFAULT_HEADERS)
    return _session

def send_request(handler, method, parameters):

    session = _get_session()
    method_to_call = ".".join((handler, method,))
    response_object = session.post(url=webservice, data=dumps(dict(method=method_to_call, params=parameters)))
    return loads(response_object.text)


def login():
    method = "login"
    handler = "login"
    params = {
        "auth_remoteaddr": "127.0.0.1",
        "auth_type": "ANONYMOUS",
        "auth_name": "ANONYMOUS",
        "auth_pass": "ANONYMOUS",
        "login_auth_pass": web_password,
        "create_session": True,
        "login_auth_name": web_username,
        "login_auth_type": "ADMIN"
    }

    resp = send_request(handler, method, params)
    return resp

def getUserInfo(session_id,user_id):
    handler = "user"
    method = "getUserInfo"
    params = {
        "auth_remoteaddr": "127.0.0.1",
        "auth_session": session_id,
        "auth_name": web_username,
        "auth_type": "ADMIN",
        "user_id" : user_id
    }

    response = send_request(handler,method,params)
    return response

if __name__ == "__main__":
    session_id = login()
    if session_id['error']:
        print(session_id['error'])
        exit
    user_id = '14'
    user_information = getUserInfo(session_id['result'],user_id)
    if user_information['error'] is None:
        pprint(user_information['result'])
    else:
        print user_information['error']