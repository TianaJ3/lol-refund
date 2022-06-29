import base64
import psutil
import os
import sys
import requests
import psutil
from urllib3 import disable_warnings
import configparser

disable_warnings()

def get_process_by_name(process_name):
    while True:
        for proc in psutil.process_iter():
            try:
                if process_name in proc.name():
                    return proc
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

class LeagueOfLegendsClientAPI(object):
    
    STORE_FRONTS = { # https://github.com/jesus-figueroa/lol-account-checker/blob/main/lolchecker.py
        "br": "br",
        "eune": "eun",
        "euw": "euw",
        "jp": "jp",
        "kr": "kr",
        "lan": "la1",
        "las": "la2",
        "na": "na",
        "oce": "oc",
        "ru": "ru",
        "tr": "tr",
    }
    
    def __init__(self):
        print('Waiting league client...')
        self.process = get_process_by_name("LeagueClientUx")

        self.lockfile = open(os.path.join(self.process.cwd(), "lockfile"), 'r').read()

        split = self.lockfile.split(":")

        self.process_name = split[0]
        self.process_id = split[1]
        self.port = split[2]
        self.password = str(base64.b64encode(("riot:" + split[3]).encode("utf-8")), "utf-8")
        self.protocol = split[4]
        self.region = requests.get(
            self.protocol + "://127.0.0.1:" + self.port + "/riotclient/get_region_locale",
            verify=False,
            headers={"Authorization": "Basic " + self.password}).json()
        self.session = requests.get(
            self.protocol + "://127.0.0.1:" + self.port + "/lol-login/v1/session",
            verify=False,
            headers={"Authorization": "Basic " + self.password}).json()
        
    def get(self, path):
        return requests.get(
            self.protocol + "://127.0.0.1:" + self.port + path,
            verify=False,
            headers={"Authorization": "Basic " + self.password}
        )
    
    def get_token(self, path):
        token = self.session["idToken"]
        region = LeagueOfLegendsClientAPI.STORE_FRONTS[self.region["webRegion"]]
        
        return requests.get("https://" + region + ".store.leagueoflegends.com" + path,
            verify=False,
            headers={"Authorization": "Bearer " + token}
        )
    
    def postRefund(self, path, json=None):
        token = self.session["idToken"]
        region = LeagueOfLegendsClientAPI.STORE_FRONTS[self.region["webRegion"]]
        
        return requests.post(
            self.protocol + "://" + region + ".store.leagueoflegends.com" + path,
            verify=False,
            headers={"Authorization": "Bearer " + token},
            json=json
        )
