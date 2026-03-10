# Version passend zu Vigor 5.0 (19.08.2025)

import sys
from time import sleep, time
import MotorAPI
import RedisAPI
import CM4API
import Statemachine


def init():
    RedisAPI.set_value("hmi_vend_soll", MotorAPI.get_vend()[0])
    Statemachine.soll_vend = MotorAPI.get_vend()[0]
    RedisAPI.set_value("hmi_state", "INIT")

def update():
    MotorAPI.send_heartbeat()
    p = MotorAPI.get_pos()
    a = MotorAPI.get_vend()
    status = MotorAPI.get_status()
    state = MotorAPI.get_state(status=status)
    endstops = MotorAPI.get_endstops(status=status)
    watchdogs = MotorAPI.get_watchdogs(status=status)
    inversion = MotorAPI.get_inversion(status=status)
    e = MotorAPI.get_eeprom_state()
    
    if state == "Fehler":
        Statemachine.set_error()
        fehler_text = "Allgemeiner Fehler"
        if watchdogs[0]:
            fehler_text = "Fehler Motor links einfahren"
        elif watchdogs[1]:
            fehler_text = "Fehler Motor links ausfahren"
        elif watchdogs[2]:
            fehler_text = "Fehler Motor rechts einfahren"
        elif watchdogs[3]:
            fehler_text = "Fehler Motor rechts ausfahren"
        if status & 0b100000000000000:
            fehler_text = "Timeout CM4"
        elif status & 0b1000000000000000:
            fehler_text = "Timeout Motor"
        RedisAPI.set_value("hmi_fehler", fehler_text)

    Statemachine.set_inverted(inversion[0])
    RedisAPI.set_value("hmi_pos_l", get_str(get_pos_prozent(p[0], a[0], inversion[0])) + "%")
    RedisAPI.set_value("hmi_pos_r", get_str(get_pos_prozent(p[1], a[1], inversion[1])) + "%")
    Statemachine.set_vend_curr(a[0])
    
    statemachine_state, paused = Statemachine.get_state()
    CM4API.send_hb_state(statemachine_state, paused)
    RedisAPI.set_value("hmi_state", statemachine_state)
    RedisAPI.set_value("hmi_vend_soll", Statemachine.get_vend_soll())

    if statemachine_state == "EDGE_L" or statemachine_state == "EDGE_R" or statemachine_state == "AUTO":
        RedisAPI.set_value("hmi_soll_l", get_str(Statemachine.get_geo()[0]) + "%")
        RedisAPI.set_value("hmi_soll_r", get_str(Statemachine.get_geo()[1]) + "%")
        RedisAPI.set_value("hmi_gps", CM4API.get_gps())
        RedisAPI.set_value("hmi_speed", CM4API.get_speed())
        RedisAPI.set_value("hmi_feldname", CM4API.get_fieldname())


def get_str(num):
    if num < 10:
        return "  " + str(num)
    elif num < 100:
        return " " + str(num)
    else:
        return str(num)

def get_pos_prozent(pos, vend, inversion):
    if vend <= 100:
        vend = 101
    if vend >= 910:
        vend = 909
    if inversion:
        pos_prozent = (910 - pos) / (910 - vend) * 100
    else: 
        pos_prozent = (pos - 100) / (vend - 100) * 100
    if pos_prozent < 0:
        pos_prozent = 0
    elif pos_prozent > 100:
        pos_prozent = 100
    return round(pos_prozent / 5) * 5  # 5% Steps

def reset_errors():
    MotorAPI.reset_errors()

def reset_state():
    MotorAPI.reset_state()

if __name__ == '__main__':
    init()
    
    interval = 0.1
    next_time = time.time()

    while True:
        try:
            update()
        except Exception as e:
            print("Fehler in main.py:", e)
        
        next_time += interval
        sleep_time = next_time - time.time()
        if sleep_time > 0:
            time.sleep(sleep_time)
        else:
            next_time = time.time()
