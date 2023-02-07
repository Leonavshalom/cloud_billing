# Billing Provider Data Script
A script that retrieves billing data from various cloud providers and indexes it in Elasticsearch.

## Requirements
- Python3.6
- Elasticsearch
- pip install -r requirements.txt

## Usage
To run the script, use the following command:
```
python run.py monthly <args>
```
Replace 'monthly' with 
- 'hourly' to run the script to retrive current hourly momment 
- 'monthly' to run the script to retrieve last month invoice
- 'upcloud/key' to run the token generator for upcloud token
<br />

(Optional)
For the args arguments, add any of the cloud providers names or parts of names:
```
python run.py <monthly/hourly> ten/up/ali/vult/digit/soft/100
```
- It will only print the json results retrived by the script without pushing to Elastic

## Features
Retrieves billing data from the following cloud providers:
- Softlayer
- Tencent
- Upcloud
- Vultr
- DigitalOcean
- Tb100
- Aliyun

- Indexes the billing data in Elasticsearch
- Allows for testing the monthly and hourly scripts
- Retrieves all previous invoices from January 2021 Configuration

The credentials for each provider are stored in a credentials.json file.

## Output
The script outputs the billing data for each provider in the form of a JSON object. The data is indexed in Elasticsearch in the hourly_index and monthly_index indices.
- The logs of the script are saved to /tmp/billing.log file
