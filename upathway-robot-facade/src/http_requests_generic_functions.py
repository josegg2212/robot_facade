from requests.auth import HTTPBasicAuth
import requests
import base64
import json
from enum import Enum
import zipfile
import os
import sys

sys.path.append(os.path.abspath('./logger'))
from logging_config import Logger
logger=Logger.get_logger()





class HttpGenericFunctions():

    def http_GET(self,url,headers):
        try:
            response = requests.get(url, headers=headers,verify=False,timeout=5)
            return(self.response_handler(response))
        except requests.exceptions.RequestException as e:
            logger.error(f"Server request error: {e}")
            return {'code':600,'response':f"Server request error: {e}"}

    def http_POST(self,url,headers,payload):
        try:
            response = requests.post(url, headers=headers, data=payload,verify=False,timeout=5)
            return(self.response_handler(response))
        except requests.exceptions.RequestException as e:
            logger.error(f"Server request error: {e}")
            return {'code':600,'response':f"Server request error: {e}"}

    def http_PUT(self,url,headers,payload):
        try:
            response = requests.put(url, headers=headers, data=payload,verify=False,timeout=5)
            return(self.response_handler(response))
        except requests.exceptions.RequestException as e:
            logger.error(f"Server request error: {e}")
            return {'code':600,'response':f"Server request error: {e}"}

    def http_DELETE(self,url,headers):
        try:
            response = requests.delete(url, headers=headers,verify=False,timeout=5)
            if response.status_code == 200:
                logger.debug(f"Server response: {response.status_code}")
                return {'code':response.status_code,'response':{}}
            else:
                try:
                    logger.error(f"Error response code:{response.status_code} - {(response.json()).get('title')}")
                    return {'code':response.status_code,'response':(response.json()).get('title')}
                except json.JSONDecodeError:
                    logger.error(f"Error response code:{response.status_code}")
                    if(response.status_code==401): return {'code':response.status_code,'response':'Unauthorized'}
                    return {'code':response.status_code,'response':{}}
        except requests.exceptions.RequestException as e:
            logger.error(f"Server request error: {e}")
            return {'code':600,'response':f"Server request error: {e}"}

    def response_handler(self,response):
        if response.status_code in [200,201]:
            logger.debug(f"Server response: {response.status_code}")
            try:
                json_data = response.json()
                json_pretty = json.dumps(json_data, indent=4, ensure_ascii=False)
                # print(json_pretty)
                return {'code':response.status_code,'response':json_data}
            except json.JSONDecodeError:
                return {'code':response.status_code,'response':{}}
        else:
            try:
                logger.debug(f"Error response code:{response.status_code} - {(response.json()).get('title')}")
                return {'code':response.status_code,'response':(response.json()).get('title')}
            except json.JSONDecodeError:
                logger.error(f"Error response code:{response.status_code}")
                if(response.status_code==401): return {'code':response.status_code,'response':'Unauthorized'}
                return {'code':response.status_code,'response':{}}
