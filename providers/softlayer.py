import SoftLayer
import functions
from datetime import date
from dateutil.relativedelta import relativedelta
import json

with open('credentials.json') as f:
    data = json.load(f)


class SoftlayerRQ:
    def __init__(self):
        self.name = "Softlayer"

    def hourly(self):
        env_lst = []
        for cred in data["softlayer_cred"][0]:
            try:
                client = SoftLayer.create_client_from_env(username=cred["user"], api_key=cred["token"])
                output = functions.to_dict(provider=self.name, department=cred["department"], enviroment=cred["env"],
                                           bill=client['SoftLayer_Account'].getNextInvoiceTotalAmount())
            except Exception as e:
                print("Error while working on " + self.name + " Provider " + cred["env"] + " enviroment")
                print("Error Exception: ")
                print(e)
            env_lst.append(output)
        return env_lst

    def monthly(self):
        env_lst = []
        last_month = date.today() - relativedelta(months=1)
        objectMask = "mask[id, createDate, statusCode]"
        orderBy = {"invoices": {'createDate': {'operation': 'betweenDate', 'options': [
            {'name': 'startDate', 'value': ["{}/01/{} 0:0:0".format(date.today().strftime("%m"), date.today().strftime("%Y"))]},
            {'name': 'endDate', 'value': ["{}/01/{} 23:59:59".format(date.today().strftime("%m"), date.today().strftime("%Y"))]}],
                                               'typeCode': {
                                                   'operation': 'in',
                                                   'options': [
                                                       {'name': 'data', 'value': ['RECURRING']}
                                                   ]
                                               }, }}}
        for cred in data["softlayer_cred"][0]:
            client = SoftLayer.create_client_from_env(username=cred["user"], api_key=cred["token"])
            try:
                for invoice in client.iter_call("SoftLayer_Account", "getInvoices", filter=orderBy, mask=objectMask):
                    invoice_detail = client.call("SoftLayer_Billing_Invoice", "getInvoiceTotalAmount",
                                                      id=invoice.get('id'))
                    if float(invoice_detail) > 0:
                        output = functions.to_dict(self.name, department=cred["department"], enviroment=cred["env"],
                                                                    bill=invoice_detail, year=last_month.strftime("%Y"), month=last_month.strftime("%m"))
                        break
            except Exception as e:
                print("Error while working on "+self.name+" Provider "+cred["env"]+" enviroment")
                print("Error Exception: ")
                print(e)
            env_lst.append(output)
        return env_lst

    def hourly_print(self):
        print(json.dumps(self.hourly(),indent=4))

    def monthly_print(self):
        print(json.dumps(self.monthly(),indent=4))