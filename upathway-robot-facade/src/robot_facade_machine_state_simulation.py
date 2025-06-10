from enum import Enum
import sys
import os
import time
sys.path.append(os.path.abspath('./logger'))
from logging_config import Logger
logger=Logger.get_logger()

from robot_facade_machine_state import StateMachine
from robot_facade_machine_state import msStatus
from robot_facade_machine_state import robotStatus
from robot_facade_machine_state import missionStatus

class SimulationStateMachine(StateMachine):
    def __init__(self):
        super().__init__()
        self.q_values_name = {
            "Inicialización q0": False,  
            "Comunicación SWE Robot q1": False,  
            "Modo autónomo q2": False,  
            "Robot localizado q3": False,  
            "Batería > Umbral q4": False,  
            "Robot Cargando q5": False,  
            "Nueva misión q6": False,  
            "Misión válida q7": False,  
            "Misión aceptada por SWE Robot q8": False,  
            "Misión pausada por usuario q9": False,  
            "Misión reanudada por usuario q10": False,  
            "Misión cancelada por usuario q11": False,  
            "Misión cancelada por robot q12": False,  
            "Misión finalizada q13": False,  
            "Misión finalizada sin éxito q14": False,  
            "Misión finalizada con éxito q15": False,  
            "Emergency q16": False  
        }
        self.q_values = {"q0": False, "q1": False, "q2": False, "q3": False, "q4": False, "q5": False, "q6": False, "q7": False, "q8": False, "q9": False, "q10": False, "q11": False, "q12": False, "q13": False, "q14": False, "q15": False, "q16": False}

    def update_variable(self):
        try:
            print("\nEstado actual de las variables:")
            for key, value in self.q_values.items():
                print(f"{key}: {value}")

            q_in= input("\nIngrese el número de la variable que desea cambiar: ")
            if q_in == "q":
                return
            q_index = int(q_in)
            q_name = f"q{q_index}"
    
            if q_name not in self.q_values:
                logger.error("Variable no válida. Intente de nuevo.")
                return
            
            new_value = bool(int(input(f"Ingrese el nuevo valor para {q_name} (0 o 1): ")))
            self.q_values[q_name] = new_value
            self.q0 = self.q_values["q0"]
            self.q1 = self.q_values["q1"]
            self.q2 = self.q_values["q2"]
            self.q3 = self.q_values["q3"]
            self.q4 = self.q_values["q4"]
            self.q5 = self.q_values["q5"]
            self.q6 = self.q_values["q6"]
            self.q7 = self.q_values["q7"]
            self.q8 = self.q_values["q8"]
            self.q9 = self.q_values["q9"]
            self.q10 = self.q_values["q10"]
            self.q11 = self.q_values["q11"]
            self.q12 = self.q_values["q12"]
            self.q13 = self.q_values["q13"]
            self.q14 = self.q_values["q14"]
            self.q15 = self.q_values["q15"]
            self.q16 = self.q_values["q16"]

        except ValueError:
            logger.error("Entrada no válida. Por favor, ingrese números válidos (0 o 1).")

 # ----- MAQUINA DE ESTADOS -----
    def ms_sim_start(self):
        logger.info("MS START")
        logger.info("INITIALIZING")
        while(True):
            self.update_variable()
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
            logger.info(self.ms_status)
            time.sleep(self.ms_loop_delay)
   


    

if __name__ == "__main__":
    ms=SimulationStateMachine()
    ms.ms_sim_start()