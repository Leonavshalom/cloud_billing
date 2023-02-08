import json
import requests
from datetime import datetime, timezone
import time
import functions
import datetime as dt
from datetime import date

today = date.today()
first_day_this_month = dt.datetime(int(date.today().strftime("%Y")), int(date.today().strftime("%m")), 1, 0)
with open('credentials.json') as f:
    config = json.load(f)

class Tb100RQ:
    def __init__(self):
        self.name = "100tb"
        self.url = "https://api.ingenuitycloudservices.com/rest-api/billing/invoices"

    def hourly(self):
        return []

    def monthly(self):
        env_lst = []
        for cred in config["tb100_cred"][0]:
            try:
                billing_response = requests.get(self.url,
                                                headers={'Accept': 'application/json',
                                                         'X-Api-Token': '{}'.format(cred["encoded"])},
                                                params=cred["params"])
            except Exception as e:
                print("Error while working on " + self.name + " Provider " + cred["env"] + " enviroment")
                print("Error Exception: ")
                print(e)
            billing_lst = billing_response.json()["data"][-1]
            bill = billing_lst["amount"]
            year = billing_lst["datepaid"].split("-")[0]
            month = billing_lst["datepaid"].split("-")[1]
            given_date = datetime.strptime(year+"-"+month, "%Y-%m")
            try:
                env_lst.append(functions.to_dict(self.name, department=cred["department"], enviroment=cred["env"],
                                                                bill=bill, year=given_date.strftime("%Y"), month=given_date.strftime("%m")))
            except Exception as e:
                print("Error while working on " + self.name + " Provider " + cred["env"] + " enviroment")
                print("Error Exception: ")
                print(e)
        return env_lst

    def hourly_print(self):
        print(json.dumps(self.hourly(), indent=4))

    def monthly_print(self):
        print(json.dumps(self.monthly(), indent=4))

