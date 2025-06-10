
import sys
import os
import json


sys.path.append(os.path.abspath('./logger'))
from logging_config import Logger
logger=Logger.get_logger()

from http_requests_generic_functions import HttpGenericFunctions


class Robot(HttpGenericFunctions):
    def __init__(self,robot_api_ip,robot_api_port) -> None:
        HttpGenericFunctions.__init__(self)
        self.ip=robot_api_ip
        self.port=robot_api_port
        self.base_url=f"http://{self.ip}:{self.port}"
        self.robot_name="Generic"

    def getRobotStatus(self):
        """
        Call the robot API and return the generic status of the robot.
        If there's no communication with robot api return:
        {
            "code":400,
            "response":"Description of the problem"
        }
        If there's communication with robot api return:
        {
            "code": 200,
            "response":{
                        "autonomous_mode": bool,
                        "localized": bool,
                        "battery": float,
                        "charging": bool,
                        "emergency": bool
                        }
        }
        """

        headers = {
        'Accept': 'application/json'
        }
        endpoint='/get_state'
        url=f"{self.base_url}{endpoint}"
        data=self.http_GET(url,headers)
        # if(data["response"]["robot_swe_communication"]==False): data["code"]=400
        return(data)
  
    def sendMission(self, mission):
        headers = {
            'Accept': 'application/json'
        }
        endpoint='/send_mission'
        url=f"{self.base_url}{endpoint}"
        data=self.http_POST(url,headers,mission)
        return(data)
    
    def stopMission(self):
        headers = {
            'Accept': 'application/json'
        }
        endpoint='/stop_mission'
        url=f"{self.base_url}{endpoint}"
        data=self.http_POST(url,headers,{})
        return(data)
    
    def resumeMission(self):
        headers = {
            'Accept': 'application/json'
        }
        endpoint='/resume_mission'
        url=f"{self.base_url}{endpoint}"
        data=self.http_POST(url,headers,{})
        return(data)
    
    def cancelMission(self):
        headers = {
            'Accept': 'application/json'
        }
        endpoint='/cancel_mission'
        url=f"{self.base_url}{endpoint}"
        data=self.http_POST(url,headers,{})
        return(data)

    def getMissionStatus(self):
        headers = {
            'Accept': 'application/json'
        }
        endpoint=f'/get_mission_status'
        url=f"{self.base_url}{endpoint}"
        data=self.http_GET(url,headers)
        return(data)
    
if __name__ == "__main__":
    robot_api_ip="192.168.100.222"
    robot_api_port=8090
    robot=Robot(robot_api_ip,robot_api_port)
    print(robot.getRobotStatus())
