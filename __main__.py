# Script to send tabular email of redash data
# This will send only top 10 data points 

import requests
from json2html import *
import json
import bs4
from utils import parse_argument, get_config

config = get_config()

def get_html_table(jsonData):
	jsonData = jsonData['query_result']['data']['rows']
	jsonData = jsonData[:10]
	template = "<html><body><table cellpadding=10 border=1></table></body></html>"
	soup = bs4.BeautifulSoup(template)
	header_data = jsonData[1].keys()
	table_header_row = bs4.BeautifulSoup('<thead><tr></tr></thead>')
	for header_col in header_data:
		table_header_data = bs4.BeautifulSoup('<th bgcolor=#dddddd>' + header_col + '</th>')
		table_header_row.tr.append(table_header_data)
	soup.body.table.append(table_header_row)
	template = str(soup)
	return template

def get_query_details(query_id):
  query_url = redash_query_url + query_id
  query_details = requests.get(query_url, 
        params={'api_key': query_key}).json()
	return query_details
	
def get_query_results():
  query_url = redash_query_url + query_id + "/results.json"
  query_results = requests.get(query_url, 
        params={'api_key': query_key}).json()
  return query_results

# function to put the refresh query logic
def put_query_refresh():
  pass

def send_email_alert(query_details, query_result, recepient_emails):
    message = get_html_table(query_result)
    request_url = 'https://api.mailgun.net/v3/<staging>/messages'
    response = requests.post(request_url, auth=('api', 'key'), data={
        'from': 'noreply@redash.practo.com',
        'to': recepient_emails,
        'subject': query_details.name,
        'html': message
    })
    # print response

options = parse_argument()
query_details = get_query_details(options.query_id)
query_result = get_query_results(options.query_id)
send_email_alert(query_details, query_result, options.recepient_emails)








