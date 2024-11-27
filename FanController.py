#!/usr/bin/python
import time
import pigpio


class FanController:
    __FAN_OFF_TEMP: int
    __FAN_MAX_TEMP: int
    __PWM_FREQ: int
    __PWM_PIN: int
    __GPIO = 0
    __PWM_SPD = 0

    def __init__(self, pwm_pin: int, pwm_freq: int, fan_max_temp: int, fan_off_temp: int) -> None:
        self.__PWM_PIN = pwm_pin
        self.__PWM_FREQ = pwm_freq
        self.__FAN_OFF_TEMP = fan_off_temp
        self.__FAN_MAX_TEMP = fan_max_temp
        self.__GPIO = pigpio.pi()
        self.GPIO_init()

    def map(self, x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    def fan_curve(self, cpu_temp: int):
        spd = 255 * (float(cpu_temp) - float(self.__FAN_OFF_TEMP)) / (float(self.__FAN_MAX_TEMP) - float(self.__FAN_OFF_TEMP))
        return int(min(max(0, spd), 255))

    def set_speed(self, spd):
        self.__PWM_SPD = spd
        self.__GPIO.set_PWM_dutycycle(self.__PWM_PIN, spd)

    def GPIO_init(self):
        self.__GPIO.set_mode(self.__PWM_PIN, pigpio.OUTPUT)
        self.__GPIO.set_PWM_frequency(self.__PWM_PIN, self.__PWM_FREQ)
        self.__GPIO.set_PWM_dutycycle(self.__PWM_PIN, 254)

    def handler(self,temp:float):
            spd = self.fan_curve(temp)
            if spd != self.__PWM_SPD:
                self.set_speed(spd)
                print("PWM: " + str(spd))
                print("TEMP: " + str(temp))
            message = "CPUTEMP: " + str(temp) + "°C" + "\n" + "FANSPEED: " + str(self.map(spd, 0, 255, 0, 100)) + "%" + "\n" + "TIME: " + str(time.asctime(time.localtime(time.time()))) + "\n" + "Device: "
            return message, self.map(spd, 0, 255, 0, 100)
