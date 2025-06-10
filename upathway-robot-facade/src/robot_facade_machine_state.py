from enum import Enum
import sys
import os
import time
sys.path.append(os.path.abspath('./logger'))
from logging_config import Logger
logger=Logger.get_logger()



class msStatus(Enum):
    E0_INITIALIZING = 0
    E1_INIT = 1
    E2_NOT_COMUNICATED = 2
    E3_NOT_AUTONOMOUS_MODE = 3
    E4_NOT_LOCALIZED = 4
    E5_NOT_BATTERY = 5
    E6_NOT_CHARGING = 6
    E7_CHARGING = 7
    E8_WAITTING_MISSION = 8
    E9_PROCESSING_MISSION = 9
    E10_NOT_VALID_MISSION = 10
    E11_SENDING_MISSION = 11
    E12_REJECTED_MISSION = 12
    E13_EXECUTING_MISSION = 13
    E14_PAUSED_MISSION = 14
    E15_CANCELED_MISSION_BY_USR = 15
    E16_CANCELED_MISSION_BY_ROBOT = 16
    E17_FINISHED_MISSION = 17
    E18_SUCCESSFULLY_MISSION_COMPLETED = 18
    E19_UNSUCCESSFULLY_MISSION_COMPLETED = 19
    E20_DATA_PROCESSING = 20
    E21_EMERGENCY = 21
    

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


class StateMachine():
    def __init__(self):

        self.ms_loop_delay = 0.1

        ## STATE MACHINE ######################################
        self.ms_status=msStatus.E0_INITIALIZING
        self.q0 = False #Inicialización inicial ( Carga de archivos, bases de datos, configuraciones etc etc)
        self.q1 = False #Comunicación con software de control del robot. 
        self.q2 = False #Modo autónomo.
        self.q3 = True #Robot localizado.
        self.q4 = False #Batería > Umbral.
        self.q5 = True #Robot Cargando.
        self.q6 = False #Nueva misión.
        self.q7 = False #Misión válida.
        self.q8 = False #Misión aceptada por swe robot.
        self.q9 = False #Misión pausada por usuario.
        self.q10 = False #Misión reanudada por usuario.
        self.q11 = False #Misión cancelada por usuario.
        self.q12 = False #Misión cacelada por robot.
        self.q13 = False #Misión finalizada.
        self.q14 = False #Misión finalizada sin éxito.
        self.q15 = False #Misión finalizada con éxito.
        self.q16 = False #Emergency
        #######################################################

     
    # ----- MAQUINA DE ESTADOS -----
    def ms_start(self):
        logger.info("MS START")
        logger.info("INITIALIZING")
        while(True):
            if self.ms_status == msStatus.E0_INITIALIZING:
                self.E0_initializing()
            elif self.ms_status == msStatus.E1_INIT:
                self.E1_init()
            elif self.ms_status == msStatus.E2_NOT_COMUNICATED:              
                self.E2_not_communicated()
            elif self.ms_status == msStatus.E3_NOT_AUTONOMOUS_MODE:
                self.E3_not_autonomous_mode()
            elif self.ms_status == msStatus.E4_NOT_LOCALIZED:
                self.E4_not_localized()
            elif self.ms_status == msStatus.E5_NOT_BATTERY:
                self.E5_not_battery()
            elif self.ms_status == msStatus.E6_NOT_CHARGING:
                self.E6_not_charging()
            elif self.ms_status == msStatus.E7_CHARGING:
                self.E7_charging()
            elif self.ms_status == msStatus.E8_WAITTING_MISSION:
                self.E8_waiting_mission()
            elif self.ms_status == msStatus.E9_PROCESSING_MISSION:
                self.E9_processsing_mission()
            elif self.ms_status == msStatus.E10_NOT_VALID_MISSION:
                self.E10_not_valid_mission()
            elif self.ms_status == msStatus.E11_SENDING_MISSION:
                self.E11_sending_mission()
            elif self.ms_status == msStatus.E12_REJECTED_MISSION:
                self.E12_rejected_mission()
            elif self.ms_status == msStatus.E13_EXECUTING_MISSION:
                self.E13_executing_mission()
            elif self.ms_status == msStatus.E14_PAUSED_MISSION:
                self.E14_paused_mission()  
            elif self.ms_status == msStatus.E15_CANCELED_MISSION_BY_USR:
                self.E15_canceled_mission_by_usr()      
            elif self.ms_status == msStatus.E16_CANCELED_MISSION_BY_ROBOT:
                self.E16_canceled_mission_by_robot()      
            elif self.ms_status == msStatus.E17_FINISHED_MISSION:
                self.E17_finished_mission()
            elif self.ms_status == msStatus.E18_SUCCESSFULLY_MISSION_COMPLETED:
                self.E18_successfully_finished_mission()
            elif self.ms_status == msStatus.E19_UNSUCCESSFULLY_MISSION_COMPLETED:
                self.E19_unsuccessfully_finished_mission()
            elif self.ms_status == msStatus.E20_DATA_PROCESSING:
                self.E20_processing_data()
            elif self.ms_status == msStatus.E21_EMERGENCY:
                self.E21_emergency()
            time.sleep(self.ms_loop_delay)
    
    def E0_initializing(self):
        self.robot_status=robotStatus.DISCONNECTED
        if(self.q0==True):
            self.ms_status=msStatus.E1_INIT
            logger.info("E1_INIT")

    def E1_init(self):
        self.robot_status=robotStatus.DISCONNECTED
        if(not self.q1):
            self.ms_status=msStatus.E2_NOT_COMUNICATED
            logger.info("E2_NOT_COMUNICATED")
        elif(self.q1 and not self.q2):
            self.ms_status=msStatus.E3_NOT_AUTONOMOUS_MODE
            logger.info("E3_NOT_AUTONOMOUS_MODE")
        # elif(self.q1 and self.q2 and not self.q3):
        #     self.ms_status=msStatus.E4_NOT_LOCALIZED
        #     logger.info("E4_NOT_LOCALIZED")
        elif(self.q1 and self.q2 and self.q3 and not self.q4):
            self.ms_status=msStatus.E5_NOT_BATTERY
            logger.info("E5_NOT_BATTERY")
        elif(self.q1 and self.q2 and self.q3 and self.q4):
            self.ms_status=msStatus.E8_WAITTING_MISSION
            logger.info("E8_WAITTING_MISSION")

    def E2_not_communicated(self):
        self.robot_status=robotStatus.DISCONNECTED
        if(self.q1):
            self.ms_status=msStatus.E1_INIT
            logger.info("E1_INIT")
    
    def E3_not_autonomous_mode(self):
        self.robot_status=robotStatus.DISCONNECTED
        if(not self.q1 or self.q2):
            self.ms_status=msStatus.E1_INIT
            logger.info("E1_INIT")

    def E4_not_localized(self):
        self.robot_status=robotStatus.DISCONNECTED
        if(not self.q1 or not self.q2 or self.q3):
            self.ms_status=msStatus.E1_INIT
            logger.info("E1_INIT")

    def E5_not_battery(self):
        self.robot_status=robotStatus.DISCONNECTED
        if(self.q5):
            self.ms_status=msStatus.E7_CHARGING
            logger.info("E7_CHARGING")
        elif(not self.q5):
            self.ms_status=msStatus.E6_NOT_CHARGING
            logger.info("E6_NOT_CHARGING")

    def E6_not_charging(self):
        self.robot_status=robotStatus.EMERGENCY
        if(self.q5):
            self.ms_status=msStatus.E7_CHARGING
            logger.info("E7_CHARGING")
        elif(not self.q1 or self.q4):
            self.ms_status=msStatus.E1_INIT
            logger.info("E1_INIT")

    def E7_charging(self):
        self.robot_status=robotStatus.CHARGING
        if(not self.q5):
            self.ms_status=msStatus.E6_NOT_CHARGING
            logger.info("E6_NOT_CHARGING")
        elif(not self.q1 or self.q4):
            self.ms_status=msStatus.E1_INIT
            logger.info("E1_INIT")

    def E8_waiting_mission(self):
        self.robot_status=robotStatus.AVAILABLE
        if(not self.q1 or not self.q2 or not self.q3 or not self.q4):
            self.ms_status=msStatus.E1_INIT
            logger.info("E1_INIT")
        elif(self.q6):
            self.q6 = False
            self.ms_status=msStatus.E9_PROCESSING_MISSION
            logger.info("E9_PROCESSING_MISSION")


    def E9_processsing_mission(self):
        self.robot_status=robotStatus.MISSION_IN_PROGRESS
        self.mission_status=missionStatus.EXECUTING
        self.q7 = True
        if(not self.q1 or not self.q2 or not self.q3 or not self.q4):
            self.ms_status=msStatus.E1_INIT
            logger.info("E1_INIT")
        elif(not self.q7):
            self.ms_status=msStatus.E10_NOT_VALID_MISSION
            logger.info("E10_NOT_VALID_MISSION")
        elif(self.q7):            
            self.ms_status=msStatus.E11_SENDING_MISSION
            self.q7 = True
            logger.info("E11_SENDING_MISSION")

    def E10_not_valid_mission(self):
        self.robot_status=robotStatus.MISSION_IN_PROGRESS
        self.mission_status=missionStatus.DROPPED
        self.ms_status=msStatus.E1_INIT
        logger.info("E1_INIT")
    
    def E11_sending_mission(self):
        self.robot_status=robotStatus.MISSION_IN_PROGRESS
        data = self.robot.sendMission(self.received_mission)
        self.q8 = (data["code"]==200) 
        if(not self.q8):
            self.ms_status=msStatus.E12_REJECTED_MISSION
            logger.info("E12_REJECTED_MISSION")
        elif(self.q8):
            self.ms_status=msStatus.E13_EXECUTING_MISSION
            logger.info("E13_EXECUTING_MISSION")

    def E12_rejected_mission(self):
        self.robot_status=robotStatus.DISCONNECTED
        self.mission_status=missionStatus.DROPPED
        self.ms_status=msStatus.E1_INIT
        logger.info("E1_INIT")

    def E13_executing_mission(self):  
        self.robot_status=robotStatus.MISSION_IN_PROGRESS
        if(self.q16):
            self.ms_status=msStatus.E21_EMERGENCY
            logger.info("E21_EMERGENCY")
        elif(self.q9 and not self.q10):
            data = self.robot.stopMission()
            self.q9 = False
            if (data["code"]==200):
                self.ms_status=msStatus.E14_PAUSED_MISSION
                logger.info("E14_PAUSED_MISSION")
            else :
                self.ms_status=msStatus.E13_EXECUTING_MISSION
        elif(self.q11):
            data = self.robot.cancelMission()
            self.q11 = False
            if (data["code"]==200):
                self.ms_status=msStatus.E15_CANCELED_MISSION_BY_USR
                logger.info("E15_CANCELED_MISSION_BY_USR")
            else :
                self.ms_status=msStatus.E13_EXECUTING_MISSION
        elif(self.q12):
            self.ms_status=msStatus.E16_CANCELED_MISSION_BY_ROBOT
            logger.info("E16_CANCELED_MISSION_BY_ROBOT")
        elif(self.q13):
            self.ms_status=msStatus.E17_FINISHED_MISSION
            logger.info("E17_FINISHED_MISSION")


    def E14_paused_mission(self):
        self.robot_status=robotStatus.MISSION_IN_PROGRESS
        if(self.q11):
            data = self.robot.cancelMission()
            self.q11 = False
            if (data["code"]==200):
                self.ms_status=msStatus.E15_CANCELED_MISSION_BY_USR
                logger.info("E15_CANCELED_MISSION_BY_USR")
            else :
                self.ms_status=msStatus.E14_PAUSED_MISSION
                logger.info("E14_PAUSED_MISSION")
        elif(self.q10 and not self.q9):
            data = self.robot.resumeMission()
            self.q10 = False
            if (data["code"]==200):
                self.ms_status=msStatus.E13_EXECUTING_MISSION
                logger.info("E13_EXECUTING_MISSION")
            else :
                self.ms_status=msStatus.E14_PAUSED_MISSION
                logger.info("E14_PAUSED_MISSION")
            self.ms_status=msStatus.E13_EXECUTING_MISSION
            logger.info("E13_EXECUTING_MISSION")

    def E15_canceled_mission_by_usr(self):
        self.robot_status=robotStatus.MISSION_IN_PROGRESS
        self.mission_status=missionStatus.NOT_EXECUTED
        self.ms_status=msStatus.E20_DATA_PROCESSING
        logger.info("E20_DATA_PROCESSING")
         
    def E16_canceled_mission_by_robot(self):
        self.robot_status=robotStatus.MISSION_IN_PROGRESS
        self.mission_status=missionStatus.NOT_EXECUTED
        self.ms_status=msStatus.E20_DATA_PROCESSING
        logger.info("E20_DATA_PROCESSING")

    def E17_finished_mission(self):
        self.robot_status=robotStatus.MISSION_IN_PROGRESS
        if(self.q15 and not self.q14):
            self.ms_status=msStatus.E18_SUCCESSFULLY_MISSION_COMPLETED
            logger.info("E18_SUCCESSFULLY_MISSION_COMPLETED")
        elif(self.q14 and not self.q15):
            self.ms_status=msStatus.E19_UNSUCCESSFULLY_MISSION_COMPLETED
            logger.info("E19_UNSUCCESSFULLY_MISSION_COMPLETED")
      
    def E18_successfully_finished_mission(self):
        self.robot_status=robotStatus.MISSION_IN_PROGRESS
        self.mission_status=missionStatus.FINISHED
        self.ms_status=msStatus.E20_DATA_PROCESSING
        logger.info("E20_DATA_PROCESSING")

    def E19_unsuccessfully_finished_mission(self):
        self.robot_status=robotStatus.MISSION_IN_PROGRESS
        self.mission_status=missionStatus.FINISHED
        self.ms_status=msStatus.E20_DATA_PROCESSING
        logger.info("E20_DATA_PROCESSING")

    def E20_processing_data(self):
        self.robot_status=robotStatus.MISSION_IN_PROGRESS
        self.ms_status=msStatus.E1_INIT
        logger.info("E1_INIT")

    def E21_emergency(self):
        self.robot_status=robotStatus.DISCONNECTED
        self.mission_status=missionStatus.NOT_EXECUTED
        if(not self.q16):
            self.ms_status=msStatus.E1_INIT
            logger.info("E1_INIT")



    

if __name__ == "__main__":
    ms=StateMachine()
    ms.ms_start()