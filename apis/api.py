#API functions

from abc import ABC, abstractmethod
import requests
import json
import configparser

class APIrequester(ABC):
    def __init__(self):
        print("init base APIrequester")

    @abstractmethod
    def request():pass

    @abstractmethod
    def run(self):pass
    
    @abstractmethod
    def stop():pass
        
