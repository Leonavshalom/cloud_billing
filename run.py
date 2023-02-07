import datetime
import sys
import json
from elasticsearch import Elasticsearch
import time
import providers.all_previous as all
from providers.aliyun import AliyunRQ
from providers.digital import DigitalRQ
from providers.softlayer import SoftlayerRQ
from providers.tencent import TencentRQ
from providers.tb100 import Tb100RQ
import functions
from providers.upcloud import UpcloudRQ
from providers.vultr import VultrRQ
import random

provider_lst = [
    SoftlayerRQ(),
    TencentRQ(),
    UpcloudRQ(),
    VultrRQ(),
    DigitalRQ(),
    Tb100RQ(),
    AliyunRQ()
]
monthly_index = "yearly_invoice_test"
hourly_index = "provider_billing"


def connect_to_elastic():
    logger = functions.setup_logger(logger_name="connect_to_elastic")
    try:
        es = Elasticsearch(
            "xx-xx.xxx.xx",
            http_auth=("script_job", "XXxXxxX"),
            verify_certs=False,
            scheme="https",
            port=9200,
        )
    except Exception as e:
        logger.error({
            "message": "Error while connecting to elastic",
            "error": e
        })
        sys.exit(1)
    return es


def billing2elastic(invoice_type, provider_name=None):
    logger = functions.setup_logger(logger_name="billing2elastic")
    if invoice_type not in ["hourly", "monthly"]:
        raise ValueError("Invoice type must be 'hourly' or 'monthly'")

    index = hourly_index if invoice_type == "hourly" else monthly_index

    for provider in provider_lst:
        if provider_name and provider.name != provider_name:
            continue

        method = getattr(provider, invoice_type)
        for env in method():
            es = connect_to_elastic()
            try:
                es.index(index, document=env)
            except Exception as e:
                logger.error({
                    "message": "Error while working on " + provider.name + " Provider , on function billing2elastic",
                    "error": e
                })

def invoices(provider, invoice_type):
    if invoice_type == "monthly":
        return provider.monthly()
    elif invoice_type == "hourly":
        return provider.hourly()


def main(invoice_type, provider_name=None):
    logger = functions.setup_logger(logger_name="main")
    start_time = time.time()
    if provider_name:
        provider = next((p for p in provider_lst if provider_name.lower() in p.name.lower()), None)
        print("Run Time =", datetime.datetime.now().strftime("%H:%M:%S") + "\n")
        print(f"{invoice_type.capitalize()} script #" + f" {provider.name}")
        for env in invoices(provider, invoice_type):
            try:
                print(json.dumps(env, indent=4))
            except Exception as e:
                logger.error({
                    "message": "Error while working on " + provider.name + " Provider , on function main",
                    "error": e
                })
    else:
        if invoice_type == "monthly":
            billing2elastic("monthly")
        elif invoice_type == "hourly":
            billing2elastic("hourly")
        elif invoice_type in 'upcloud-key':
            functions.upcloud_encoded_cred_convertor()
        else:
            logger.error({
                "message": "Error while working on function main",
                "error": "Invalid invoice type. Must be 'monthly', 'hourly', or 'upcloud-key'."
            })
            print("Invalid invoice type. Must be 'monthly', 'hourly', or 'upcloud-key'.")
    end_time = time.time()
    total_time = end_time - start_time
    logger.info("-"*50 + "Script execution completed in " + str(total_time) + " seconds" + "-"*50)
    return



if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please specify 'monthly', 'hourly', or 'all' as an argument.")
        exit(-1)

    command = sys.argv[1].lower()
    provider_name = None

    if len(sys.argv) == 3:
        provider_name = sys.argv[2].capitalize()

    main(command, provider_name)

