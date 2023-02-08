import json
import requests
from datetime import datetime, timezone
import functions

with open('credentials.json') as f:
    config = json.load(f)


class DigitalRQ:
    def __init__(self):
        self.name = "Digital Ocean"
        self.hourly_url = "https://api.digitalocean.com/v2/customers/my/balance"
        self.monthly_url = "https://api.digitalocean.com/v2/customers/my/invoices"

    def fetch_data(self, url, call):
        logger = functions.setup_logger(logger_name=self.name)
        env_lst = []
        for cred in config["digital_cred"][0]:
            headers = {"Authorization": "Bearer {}".format(cred["encoded"]),
                       "Content-Type": "application/json"}
            try:
                billing_response = requests.get(url, headers=headers).json()
                if call == "hourly":
                    env_lst.append(
                        functions.to_dict(provider=self.name, department=cred["department"], enviroment=cred["env"],
                                          bill=billing_response['month_to_date_balance']))
                else:
                    obj = billing_response["invoices"][0]
                    env_lst.append(
                        functions.to_dict(provider=self.name, department=cred["department"], enviroment=cred["env"],
                                          bill=obj["amount"],
                                          year=obj["invoice_period"].split("-")[0],
                                          month=obj["invoice_period"].split("-")[1]))
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
