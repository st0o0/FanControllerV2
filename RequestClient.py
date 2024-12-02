#!/usr/bin/python
import requests

class RequestClient:
    __url: str
    __name: str

    def __init__(self, url: str, name: str):
            self.__url = url
            self.__name = name

    def send(self, temp: float):
            json_object = {
                "name": self.__name,
                "temp": temp
            }
            try:
                result =  requests.post(self.__url, data=json_object, json=json_object, timeout=5)
            except Exception as e:
                print(e.args)
                return None
            return result