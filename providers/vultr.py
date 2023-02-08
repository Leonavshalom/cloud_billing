import json
from datetime import date
from dateutil.relativedelta import relativedelta
import requests
import logging
import functions

last_month = date.today() - relativedelta(months=1)
with open('credentials.json') as f:
    config = json.load(f)


class VultrRQ:
    def __init__(self):
        self.name = "Vultr"
        self.monthly_url = "https://api.vultr.com/v2/billing/history"
        self.hourly_url = "https://api.vultr.com/v2/account"
        self.headers = {"Content-Type": "application/json"}

    def fetch_data(self, url, call):
        logger = functions.setup_logger(logger_name=self.name)
        env_lst = []
        for cred in config["vultr_cred"][0]:
            self.headers["Authorization"] = "Bearer {}".format(cred["key"])
            try:
                response = requests.get(url, headers=self.headers).json()
                if call == "monthly":
                    env_lst.append(
                        functions.to_dict(provider=self.name, department=cred["department"], enviroment=cred["env"],
                                          bill=abs(response["billing_history"][0]["amount"]),
                                          year=last_month.strftime("%Y"),
                                          month=last_month.strftime("%m")))
                else:
                    env_lst.append(
                        functions.to_dict(provider=self.name, department=cred["department"], enviroment=cred["env"],
                                          bill=response["account"]["pending_charges"]))
                logger.info({
                    "message": "Successfully fetched data from " + self.name + " Provider " + cred["env"] + " enviroment"
                })
            except Exception as e:
                logger.error({
                    "message": "Error while working on " + self.name + " Provider " + cred["env"] + " enviroment",
                    "error": e
                })
        return env_lst

    def hourly(self):
        return self.fetch_data(self.hourly_url, "hourly")

    def monthly(self):
        return self.fetch_data(self.monthly_url, "monthly")

    def print_data(self, data):
        print(json.dumps(data, indent=4))

    def hourly_print(self):
        self.print_data(self.hourly())

    def monthly_print(self):
        self.print_data(self.monthly())
