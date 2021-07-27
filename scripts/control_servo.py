import RPi.GPIO as GPIO
from time import sleep

class ServoControl:

    def __init__(self, *args, **kwargs):
        """init"""
        super(ServoControl, self).__init__(*args, **kwargs)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(3, GPIO.OUT)
        self.pwm = GPIO.PWM(3, 50)
        
        self.position = 0
        self.pwm.start(self.position)

    def set_angle(self, angle):
        """get angle in degree & set servo angle"""
        duty = angle / 18 + 2
        GPIO.output(3, True)
        pwm.ChangeDutyCycle(duty)
        self.position = angle
        sleep(1)
        GPIO.output(3, False)
        pwm.ChangeDutyCycle(0)

    def get_angle(self):
        """get angle of servo motor"""
        return self.position

    def drop_ball(self):
        """drop one ball"""
        position = self.get_angle()
        # TODO




if __name__ == '__main__':
    """for test"""
    controller = ServoControl()
    controller.set_angle(0)
    sleep(2)
    controller.set_angle(45)
    sleep(2)
    controller.set_angle(90)
    sleep(2)
    controller.set_angle(135)
    sleep(2)
    controller.set_angle(180)
    sleep(2)

    controller.pwm.stop()
    GPIO.cleanup()