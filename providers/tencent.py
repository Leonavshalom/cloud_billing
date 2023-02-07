from tencentcloud.billing.v20180709 import billing_client, models
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
import json
from datetime import datetime,timezone
from datetime import date
from dateutil.relativedelta import relativedelta
import functions

httpProfile = HttpProfile()
httpProfile.endpoint = "billing.tencentcloudapi.com"
clientProfile = ClientProfile()
clientProfile.httpProfile = httpProfile
req = models.DescribeBillSummaryByPayModeRequest()
last_month = date.today() - relativedelta(months=1)
with open('credentials.json') as f:
    config = json.load(f)


class TencentRQ:
    def __init__(self):
        self.name = "Tencent"

    def hourly(self):
        env_lst = []
        for cred in config["tencent_cred"]:
            creds = credential.Credential(cred["user"], cred["token"])
            client = billing_client.BillingClient(creds, "", clientProfile)
            params = {
                "BeginTime": "{}".format(date.today().strftime("%Y-%m")),
                "EndTime": "{}".format(date.today().strftime("%Y-%m"))
            }
            try:
                req.from_json_string(json.dumps(params))
                resp = client.DescribeBillSummaryByPayMode(req)
            except Exception as e:
                print("Error while working on " + self.name + " Provider " + cred["env"] + " enviroment")
                print("Error Exception: ")
                print(e)
            bill = resp.__dict__['SummaryOverview'][1].__dict__['RealTotalCost']
            env_lst.append(functions.to_dict(provider=self.name, department=cred["department"], enviroment=cred["env"], bill=bill))
        return env_lst

    def monthly(self):
        env_lst = []
        for cred in config["tencent_cred"]:
            creds = credential.Credential(cred["user"], cred["token"])
            client = billing_client.BillingClient(creds, "", clientProfile)
            params = {
                "BeginTime": "{}".format(last_month.strftime("%Y-%m")),
                "EndTime": "{}".format(last_month.strftime("%Y-%m"))
            }
            try:
                req.from_json_string(json.dumps(params))
                resp = client.DescribeBillSummaryByPayMode(req)
            except Exception as e:
                print("Error while working on " + self.name + " Provider " + cred["env"] + " enviroment")
                print("Error Exception: ")
                print(e)
            bill = resp.__dict__['SummaryOverview'][1].__dict__['RealTotalCost']
            if float(bill) > 10:
                env_lst.append(functions.to_dict(provider=self.name, department=cred["department"], enviroment=cred["env"], bill=bill,year=last_month.strftime("%Y"), month=last_month.strftime("%m")))
        return env_lst

    def hourly_print(self):
        print(json.dumps(self.hourly(),indent=4))

    def monthly_print(self):
        print(json.dumps(self.monthly(),indent=4))

