import os
import urllib2
import requests
import json
from bs4 import BeautifulSoup
from os import path

# Blank arrays and dictionary setup
company_link_array = []
all_company_info = {}
json_list = []

# Method to get all the links to the companies on a single page based on page number
def getHTML(page_number):

    # URL that links will be pulled from.
    webpage = 'http://data-interview.enigmalabs.org/companies/?page=' + str(page_number)

    page = requests.get(webpage)

    soup = BeautifulSoup(page.content, 'html.parser')

    # Goes into table class 'table table-hover' where the links are stored
    table = soup.find('table','table table-hover')
    links = table.find_all('a')

    # puts the company links into the 'company_link_array'. To be used in other methods
    for link in links:
        company_link_array.append(link.attrs.get('href'))


# Method to go through all the pages and run the 'getHTLM(page_number)' method
def get_all_company_links(number_of_pages):
    i = 1
    while i < (number_of_pages + 1):
        getHTML(i)
        i = i +1
    #  Returns the 'company_link_array' full of the links to all the companies pages.
    return company_link_array


# Pull a single company's webpage details and put into a dictionary
def on_company_page(webpage):
    # Resets the storing_dictionary to blank every time this method is used.
    storing_dictionary = {}

    page = requests.get(webpage)

    soup = BeautifulSoup(page.content, 'html.parser')

    # goes into the 'table table-hover'.
    table = soup.find('table','table table-hover')
    t_rows = table.find_all('td')
    for script in t_rows:
        if script.has_attr('id'):
            # IMPORTANT: uses the 'id' as the key instead of the headers visable on the webpage on the leftside
            # for example: instead of the key being 'Phone' it is the id which is 'phone_number'
            storing_dictionary[script.get('id')] = script.get_text()

    return storing_dictionary

# Loop through all the companies to get all their details.
def get_all_companies_details(number_of_pages):
    webpage = 'http://data-interview.enigmalabs.org'

    # Get all the companies links stored into an 'array' variable
    array = get_all_company_links(number_of_pages)

    # The loop to get put all the new company dictionaries into an array.
    for company in array:
        new_webpage =  webpage + str(company)
        json_list.append(on_company_page(new_webpage))

    return json_list

# Turns the 'json_list' into a usable json file.
def make_report(number_of_pages, filename):
    try:
        jsondata = json.dumps(get_all_companies_details(number_of_pages), indent=4, skipkeys=True, sort_keys=True)
    	fd = open(filename, 'w')
    	fd.write(jsondata)
    	fd.close()
    except:
		print 'ERROR writing', filename
		pass

# Only need to call 'make_report' to get all the data into a "solution.json"
make_report(10, 'solution.json')
