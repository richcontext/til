import requests

def call_api(params):
    return requests.get('http://httpbin.org/get', params)
