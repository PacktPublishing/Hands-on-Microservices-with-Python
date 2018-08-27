from flask import abort
import requests


def get_request(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.HTTPError as err_http:
        print ("HTTP error: ", err_http)
        abort(404)
    except requests.exceptions.ConnectionError as err_connection:
        print ("Cannot connect: ", err_connection)
        abort(404)
    except requests.exceptions.Timeout as err_timeout:
        print ("Timeout: ", err_timeout)
        abort(404)
    except requests.exceptions.RequestException as err_request:
        print ("Error with request: ", err_request)
        abort(404)
