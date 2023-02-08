import functions
from datetime import date
from datetime import datetime,timezone
from dateutil.relativedelta import relativedelta
import json
from alibabacloud_bssopenapi20171214.client import Client as BssOpenApi20171214Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_bssopenapi20171214 import models as bss_open_api_20171214_models
from aliyunsdkbssopenapi.request.v20171214.QueryBillOverviewRequest import QueryBillOverviewRequest
from aliyunsdkcore.client import AcsClient

with open('credentials.json') as f:
    config = json.load(f)



class AliyunRQ:
    def __init__(self):
        self.name = "Aliyun"

    def hourly(self):
        env_lst = []
        total_sum = 0
        for cred in config["aliyun_cred"][0]:
            client = AcsClient(cred["user"], cred["token"], "ap-southeast-1")
            request = QueryBillOverviewRequest()
            request.add_query_param('BillingCycle', datetime.now(timezone.utc).strftime("%Y-%m"))
            request.set_accept_format('json')

            # Decode the responses object_dict to string
            try:
                response = client.do_action_with_exception(request).decode("utf-8")
                readable = json.loads(response)["Data"]
            except Exception as e:
                print("Error while working on " + self.name + " Provider " + cred["env"] + " enviroment")
                print("Error Exception: ")
                print(e)
            for i in readable["Items"]["Item"]:
                total_sum += i["AfterTaxAmount"]
            try:
                env_lst.append(functions.to_dict(provider=self.name, department=cred["department"], enviroment=cred["env"], bill=total_sum))
            except Exception as e:
                print("Error while working on " + self.name + " Provider " + cred["env"] + " enviroment")
                print("Error Exception: ")
                print(e)
        return env_lst

    def monthly(self):
        env_lst = []
        total_sum = 0
        compute_sum = 0
        storage_sum = 0
        marketplace_sum = 0

        for cred in config["aliyun_cred"][0]:
            client = AcsClient(cred["user"], cred["token"], "ap-southeast-1")
            request = QueryBillOverviewRequest()
            request.add_query_param('BillingCycle', functions.last_month.strftime("%Y-%m"))
            request.set_accept_format('json')

            # Decode the responsed object_dict to string
            try:
                response = client.do_action_with_exception(request).decode("utf-8")
                readable = json.loads(response)["Data"]
            except Exception as e:
                print("Error while working on " + self.name + " Provider " + cred["env"] + " enviroment")
                print("Error Exception: ")
                print(e)

            for i in readable["Items"]["Item"]:
                total_sum += i["AfterTaxAmount"]
                if "Storage" in i["ProductName"]:
                    storage_sum += i["AfterTaxAmount"]
                elif "support" in i["ProductName"]:
                    marketplace_sum += i["AfterTaxAmount"]
                else:
                    compute_sum += i["AfterTaxAmount"]

            if int(total_sum) != 0:
                env_lst.append(functions.to_dict(provider=self.name, department=cred["department"], enviroment=cred["env"], bill=total_sum,
                                                        year=functions.last_month.strftime("%Y"), month=functions.last_month.strftime("%m"),
                                                        storage=storage_sum, compute=compute_sum, marketplace=marketplace_sum))
        return env_lst

    def hourly_print(self):
        print(json.dumps(self.hourly(),indent=4))

    def monthly_print(self):
        print(json.dumps(self.monthly(),indent=4))