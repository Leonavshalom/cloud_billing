from datetime import date
import datetime as dt
import calendar
from datetime import datetime, timezone
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import logging
import base64


now_utc = datetime.now(timezone.utc)
dateandtime = now_utc.strftime("%Y-%m-%dT%H:%M:%S.%f%Z")
index = "yearly_invoice_test"
now_utc = datetime.now(timezone.utc)
today = date.today()
today2 = datetime.today()
now = dt.datetime.now()
hour = now.hour
todayedate = today.strftime("%d/%m/%y")  # hour
year = int(today.strftime("%Y"))
month = int(today.strftime("%m"))
yandm = now_utc.strftime("%Y-%m")
num_days = calendar.monthrange(year, month)[1]
days = [day for day in range(1, num_days + 1)]
items = list(range(0, 57))
l = len(items)
last_month = today - relativedelta(months=1)


def setup_logger(logger_name, log_file="/tmp/billing.log", level=logging.INFO):
    # create a logger
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)
    
    # create a file handler
    handler = logging.FileHandler(log_file)
    handler.setLevel(level)
    
    # create a logging format
    formatter = logging.Formatter('%(asctime)s | [%(levelname)s] | %(message)s',
                                  datefmt='%b %d %H:%M:%S')
    handler.setFormatter(formatter)
    
    # add the handlers to the logger
    logger.addHandler(handler)
    
    return logger


def upcloud_encoded_cred_convertor():
    user = input("Please enter the username: ")
    password = input("Please enter password: ")
    print(base64.b64encode("{}:{}".format(user,password)).encode().decode())
    

def to_dict(provider, department, enviroment, bill, year=None, month=None, storage=None, compute=None, traffic=None, marketplace=None):
    dateandtime = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    dikt = {
        "time": dateandtime,
        "provider": provider,
        "department": department,
        "enviroment": enviroment,
        "invoice_bill": round(float(bill), 2),
        "invoice_year": year,
        "invoice_month": month,
        "storage": storage,
        "compute": compute,
        "traffic": traffic,
        "marketplace": marketplace
    }
    return dikt

def count(lst):
    total = 0.0
    for dikt in lst:
        total += float(dikt["amount"])
    return total


def last_month_bydate(given_date):
    last_month = given_date - relativedelta(months=1)
    return last_month
