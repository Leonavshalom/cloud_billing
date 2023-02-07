from datetime import date
from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta
import requests
import functions
import json

last_month = date.today() - relativedelta(months=1)
today = date.today()
with open('credentials.json') as f:
    config = json.load(f)


class UpcloudRQ:
    def __init__(self):
        self.name = "Upcloud"
        self.hourly_url  = "https://api.upcloud.com/1.3/account/billing_summary/{}-{}".format(
            today.strftime("%Y"),
            today.strftime("%m"))
        self.monthly_url = "https://api.upcloud.com/1.3/account/billing_summary/{}".format(last_month.strftime("%Y-%m"))

    def hourly(self):
        env_lst = []
        for cred in config["upcloud_cred"]:
            headers = {"Authorization": "Basic {}".format(cred["encoded"]),
                       "Content-Type": "application/json"}
            try:
                billing_response = requests.get(self.hourly_url, headers=headers).json()
                bill = billing_response['billing']['total_amount']
                env_lst.append(
                    functions.to_dict(provider=self.name, department=cred["department"], enviroment=cred["env"],
                                            bill=bill))
            except Exception as e:
                print("Error while working on " + self.name + " Provider " + cred["env"] + " enviroment")
                print("Error Exception: ")
                print(e)
        return env_lst

    def monthly(self):
        env_lst = []
        for cred in config["upcloud_cred"]:
            headers = {"Authorization": "Basic {}".format(cred["encoded"]),
                       "Content-Type": "application/json"}
            try:
                billing_response = requests.get(self.monthly_url, headers=headers).json()['billing']
                # print(json.dumps(billing_response, indent=4))
                env_lst.append(
                    functions.to_dict(provider=self.name, department=cred["department"], enviroment=cred["env"],
                                             bill=round(billing_response["total_amount"], 2),
                                             year=last_month.strftime("%Y"), month=last_month.strftime("%m"),
                                             compute=billing_response["servers"]["total_amount"],
                                             storage=billing_response["storages"]["total_amount"]))
            except Exception as e:
                print("Error while working on " + self.name + " Provider " + cred["env"] + " enviroment")
                print("Error Exception: ")
                print(e)
        return env_lst

    def hourly_print(self):
        print(json.dumps(self.hourly(), indent=4))

    def monthly_print(self):
        print(json.dumps(self.monthly(), indent=4))