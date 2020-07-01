############################################################################
#
#   Test 2 - API Automation with 'reqests'library and Session
#
############################################################################
import time
import unittest
import configparser
from   selenium import webdriver
from   getpass import getpass

import locators
import element
import page

import requests
import json
from   requests.auth import HTTPBasicAuth


#
# Read in config options for URL, Username, Password
#
config = configparser.RawConfigParser()
config.read('myTest1.conf')

config_url       = config.get('options', 'url')
config_username  = config.get('options', 'username')
config_password  = config.get('options', 'password')
config_post_url  = config.get('options', 'post_url')

print(config.sections())
print("Config option URL: ",config_url)
print("Config option Username: ",config_username)
print("Config option Password: ",config_password)
print("Config option POST_URL: ",config_post_url)










class DexcomApiAutomation(unittest.TestCase):
    """Use the Sessions object class and unittest framework to test Dexcom API endpoint."""

    def setUp(self):
        print("setUp here.")
        #self.driver = webdriver.Chrome()
        #self.driver.get(config_url)

    def test_search_in_python_org(self):
        """
        Tests the ability to POST to https://clarity.dexcom.com/api/subject/1594950620847472640/analysis_session
        """

        # Create new session object
        newSession = requests.Session()

        #
        #  Login to Dexcom URL
        #
        #  Expect status code 200, successful login
        #
        data = {"login":config_username, "password":config_password}
        auth = HTTPBasicAuth(config_username, config_password)
        r = newSession.post(url=config_url, data=data, auth=auth)


        print("Headers:::::::: ", newSession.headers)
        print("Auth::::::::::: ", newSession.auth)
        print("Response::::::::::::::::::: ",r)
        print("Response.text:::::::::::::: ",r.text)
        print("Response.Status_Code::::::: ",r.status_code)
        assert r.status_code == 200,  "Expected status code should be 200"
        print("--------------------------------------")
        print(" ")


        
        #
        #   Now use the POST request to test API endpoint
        #
        #   Expect response status_code 401 for invalid authentication
        #
        data = {'sender': 'Alice', 'receiver': 'Bob', 'message': 'We did it!'}
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = newSession.post(config_post_url, data=json.dumps(data), headers=headers, auth=auth)
        print("Response::::::::::::::::::: ",r)
        print("Response.text:::::::::::::: ",r.text)
        print("Response.Status_Code::::::: ",r.status_code)
        assert r.status_code == 401,  "Expected status code should be 401"
        print("--------------------------------------")
        print(" ")


        #
        #  Now use the GET request to test API endpoint
        #
        #  Expect response: {'errors': [{'id': 31, 'name': 'Endpoint has been removed', 'message': 'Analysis sessions are deprecated and will be removed.'}]}
        #
        r = newSession.get(url = config_post_url, auth=auth)  
        data = r.json()
        print("data:::::::::::::::::::::: ",data)
        analysisSessionId = data['errors'][0]['id']
        print("analysisSessionID::::::::: ",analysisSessionId)
        assert analysisSessionId != 'None', "The value of analysisSessionId should not be None"

        

    def tearDown(self):
        print("tearDown here.")
        #self.driver.close()

if __name__ == "__main__":
    unittest.main()


