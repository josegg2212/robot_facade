import sys
import os
import threading
import time
import shutil
import json
import asyncio
from enum import Enum
from fastapi import Request, File, UploadFile, Form,HTTPException , Body
from typing import Literal
import datetime

sys.path.append(os.path.abspath('./apirest-fastapi-wrapper'))
sys.path.append(os.path.abspath('./logger'))
sys.path.append(os.path.abspath('./mqtt-wrapper'))


from logging_config import Logger
from apirest_fastapi_wrapper import ApiRestWrapper
from mqtt_wrapper import MQTTClient
from fastapi.responses import FileResponse
from robot_facade_machine_state import StateMachine
from robot import Robot
logger=Logger.get_logger()


class robotStatus(Enum):
    AVAILABLE="AVAILABLE"
    DISCONNECTED="DISCONNECTED"
    MISSION_IN_PROGRESS="MISSION_IN_PROGRESS"
    CHARGING="CHARGING"
    STILL="STILL"
    ROAMING="ROAMING"
    EMERGENCY="EMERGENCY"

class missionStatus(Enum):
    EXECUTING = "EXECUTING"
    PAUSED = "PAUSED"
    CANCELED = "CANCELED"
    DROPPED = "DROPPED"
    FINISHED = "FINISHED"
    NOT_EXECUTED = "NOT_EXECUTED"


class RobotFacade(StateMachine):
    def __init__(self,ip,port,endpoint,title,description,version,robot_id,facility_id,mqtt_broker_ip,mqtt_broker_port,robot_api_ip,robot_api_port,robot_uuid) -> None:
        StateMachine.__init__(self)
        self.host=ip
        self.port=port
        self.endpoint=endpoint
        self.title=title
        self.description=description
        self.version=version

        self.robot_id = robot_id
        self.facility_id = facility_id
        self.robot_uuid=robot_uuid
        self.mqtt_broker_ip = str(mqtt_broker_ip)
        self.mqtt_broker_port = int(mqtt_broker_port)

        self.mqtt_robot_status_feedback = f"facilities/{self.facility_id}/robots/{self.robot_id}/status"
        self.mqtt_mission_status = f"facilities/{self.facility_id}/robots/{self.robot_id}/missions"

        self.dashboard_indicators_topic = f"upathway/{self.robot_uuid}/telemetry"


        self.robot=Robot(robot_api_ip,robot_api_port)


        ## PARAMETERS #########################################
        self.robot_battery_threshold=20
        self.rf_loop_delay=0.5
        self.dashboard_div=5
        self.div=0
        #######################################################

        ## ROBOT STATUS #######################################
        self.robot_status=robotStatus.DISCONNECTED
        #######################################################

        ## MISSION STATUS #######################################
        self.mission_status = missionStatus.NOT_EXECUTED
        self.publish_times = 5
        #######################################################

        

        self.apirest_wrapper = ApiRestWrapper(self.host, self.port,self.endpoint,self.title,self.description,self.version)
        self.apirest_wrapper.setup_routes([(f"/api/robots/{self.robot_id}/missions/stop", ['POST'], self.stop_mission,"General"),
                                           (f"/api/robots/{self.robot_id}/missions/resume", ['POST'], self.resume_mission,"General"),
                                           (f"/api/robots/{self.robot_id}/missions/cancel", ['POST'], self.cancel_mission,"General"),
                                           (f"/api/robots/{self.robot_id}/missions/start", ['POST'], self.start_mission,"General")])


        self.mqtt_client = MQTTClient("RobotFacade",  self.mqtt_broker_ip, self.mqtt_broker_port, 60, qos=2,
                                      subscriptions=[])
        self.mqtt_client.connect()
        self.mqtt_client.spin_start()
        self.api_rest_th = threading.Thread(target=self.apirest_wrapper.run_app)
        self.mqtt_th = threading.Thread(target=self.robot_feedback)
        self.ms_th = threading.Thread(target=self.ms_start)
        self.received_mission={}
        self.thread_start()

        """
        If the initialization is performed correctly
        """
        self.q0=True
 

    def stop_mission(self):
        if(self.q9): 
            logger.info("Stop mission again") 
        else: 
            logger.info("Stop mission")
            self.q9 = True
        return 200
        
    def resume_mission(self):
        if(self.q10): 
            logger.info("Resume mission again") 
        else: 
            logger.info("Resume mission")
            self.q10 = True
        return 200

    def cancel_mission(self):
        if(self.q11): 
            logger.info("Cancel mission again") 
        else: 
            logger.info("Cancel mission")
            self.q11 = True
        return 200

    def start_mission(self,data: dict = Body(...)):
        if(self.q6): 
            logger.info(f"Mission received again: {data}") 
        else: 
            logger.info(f"Mission received: {data}")
            self.received_mission=data
            self.q6 = True
        return 200
 
    def robot_feedback(self):
        logger.info("Robot feedback thread started")
        while (True):
            data=self.robot.getRobotStatus()
            if(data["code"]==200):
                self.q1=True
                robot_battery_level=data["response"]["battery_level"]
                robot_autonomous_mode = data["response"]["autonomous_mode"]
                # robot_charging = data["response"]["robot_charging"]
                # robot_localized = data["response"]["robot_localized"]
                # robot_emergency = data["response"]["robot_emergency"]
                robot_autonomy = 10
                robot_pose_latlon=[40.33593631508078, -3.8858622087623353]
                
                statusData=json.dumps({
                    "autonomy":robot_autonomy,
                    "battery":robot_battery_level,
                    "identifier":self.robot_id,
                    "position":{
                        "lat":robot_pose_latlon[0],
                        "lng":robot_pose_latlon[1]
                    },
                    "status": self.robot_status.value
                })
                self.mqtt_client.publish(statusData, self.mqtt_robot_status_feedback)

                if(self.div==self.dashboard_div):
                    data={
                        "robot_id": self.robot_uuid,
                        "timestamp": datetime.datetime.utcnow().isoformat(),
                        "location": {
                            "latitude": float(robot_pose_latlon[0]),
                            "longitude": float(robot_pose_latlon[1]),
                        },
                        "battery": robot_battery_level,
                        "speed": 0,
                        "yaw": 0,
                        "pitch": 0,
                        "roll": 0,
                        "additional": {
                            "additional-telemetry1": "",
                            "additional-telemetry2": "",
                        }
                    }
                    self.mqtt_client.publish(json.dumps(data), self.dashboard_indicators_topic)
                    self.div=0
                self.div=self.div+1
                # q Update
                self.q2 = robot_autonomous_mode
                #self.q3 = robot_localized
                self.q4 = robot_battery_level > self.robot_battery_threshold
                #self.q5 = robot_charging
                #self.q16 = robot_emergency

            else:
                logger.error("Unable to connect with robot")
                self.q1=False

            
            # res = self.robot.getMissionStatus()
            # if res["code"] == 200:
            #     st = res["response"]["status"]

            #     self.q12 = (st == "CANCELED")
            #     self.q13 = (st == "FINISHED")
            #     # self.q15 = (st == "FINISHED") and res["response"].get("success", False)
            #     # self.q14 = (st == "FINISHED") and not res["response"].get("success", False)
            # else:
            #     self.q12 = False
            #     self.q13 = False
            #     # self.q14 = False
            #     # self.q15 = False                       


            # if hasattr(self, "_last_mission_status"):
            #     if self.mission_status != self._last_mission_status:
            #         mission_id = self.received_mission.get("mission_id")
            #         for _ in range(self.publish_times):
            #             self.send_mission_status(mission_id, self.mission_status.value)
            # self._last_mission_status = self.mission_status
        
            time.sleep(self.rf_loop_delay)

    def send_mission_status(self,mission_id,statusData):
        jsondata=json.dumps({
            "id":mission_id,
            "status":statusData
            })
        self.mqtt_client.publish(jsondata, self .mqtt_mission_status+"/"+str(mission_id)+"/transitions")


    def thread_start(self):
        self.mqtt_th.start()
        self.api_rest_th.start()
        self.ms_th.start()


    def thread_join(self):
        self.mqtt_th.join()
        self.api_rest_th.join()
        self.ms_th.join()




if __name__ == "__main__":
    robot_facade_ip=os.getenv("ROBOT_FACADE_IP")
    robot_facade_port=os.getenv("ROBOT_FACADE_PORT")

    robot_facade_endpoint=os.getenv("ROBOT_FACADE_ENDPOINT")
    robot_facade_api_title=os.getenv("ROBOT_FACADE_API_TITLE")
    robot_facade_api_description=os.getenv("ROBOT_FACADE_API_DESCRIPTION")
    robot_facade_api_version=os.getenv("ROBOT_FACADE_API_VERSION")

    robot_id=os.getenv("ROBOT_ID")
    facility_id=os.getenv("FACILITY_ID")
    robot_uuid = os.getenv("ROBOT_UUID")
    mqtt_broker_ip=os.getenv("MQTT_BROKER_IP")
    mqtt_broker_port=os.getenv("MQTT_BROKER_PORT")

    robot_api_ip = os.getenv("ROBOT_API_IP")
    robot_api_port = os.getenv("ROBOT_API_PORT")



    robotFacade=RobotFacade(robot_facade_ip,
                    robot_facade_port,
                    robot_facade_endpoint,
                    robot_facade_api_title,
                    robot_facade_api_description,
                    robot_facade_api_version,
                    robot_id,
                    facility_id,
                    mqtt_broker_ip,
                    mqtt_broker_port,
                    robot_api_ip,
                    robot_api_port,
                    robot_uuid)
    

    robotFacade.thread_join()






