#!/usr/bin/python

import json
import time
from FanController import FanController
from Mail import Mail
from RequestClient import RequestClient

def read_temp():
    with open("/sys/class/thermal/thermal_zone0/temp", "r") as file:
        temp_raw = file.read()
        file.close()
    temp = int(temp_raw) / 1000
    return round(temp, 1)


def main():
    with open("/etc/fan-controller/config.json", "r") as file:
        config = json.load(file)
        pwm_pin = config["PWM_PIN"]
        pwm_freq = config["PWM_FREQ"]
        read_pin = config["READ_PIN"]
        ppr = config["PPR"]
        fan_max_temp = config["FAN_MAX_TEMP"]
        fan_off_temp = config["FAN_OFF_TEMP"]
        update_interval = config["UPDATE_INTERVAL"]
        device = config["NAME"]
        smtphost = config["SMTPHOST"]
        smtpport = config["SMTPPORT"]
        smtpuser = config["SMTPUSER"]
        smtpcode = config["SMTPCODE"]
        mailsender = config["MAILSENDER"]
        mailreceiver = config["MAILRECEIVER"]
        webserver = config["WebServer"]
        pwm_fan = config["PWM_FAN"]
        url = config["URL"]
        file.close()

    fan_controller = 0
    request_client = 0
    mail = Mail(smtphost, smtpport, smtpuser, smtpcode, mailsender, mailreceiver)
    mail.send("TIME: " + str(time.asctime(time.localtime(time.time()))) + "\n" + "Device: " + device,"[STARTED] on " + device)
    last_warning = 0
    while True:
        message, cpu_temp, fan_speed = "", read_temp(), 0
        if pwm_fan:
            if fan_controller == 0:
                fan_controller = FanController(pwm_pin, pwm_freq, fan_max_temp, fan_off_temp)
            message, fan_speed = fan_controller.handler(cpu_temp)
            message = message + device
        if webserver:
            if request_client == 0:
                request_client = RequestClient(url, device)
            x = request_client.send(cpu_temp)
            if message == "":
                message = "CPUTEMP: " + str(cpu_temp) + "°C" + "\n" + "LAST REPONSE: " + str(x.status_code) + "\n" + "TIME: " + str(time.asctime(time.localtime(time.time()))) + "\n" + "Device: "+ device
        if (cpu_temp > fan_max_temp and fan_speed > 250) and time.perf_counter() - last_warning < 1200:
            last_warning = time.perf_counter()
            mail.send(message, "[WARN] CPUTEMP: " + str(cpu_temp) + " // TIME: " + str(time.asctime(time.localtime(time.time()))))
        time.sleep(update_interval)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e.args)
