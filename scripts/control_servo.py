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
        duty = angle / 36 + 2
        GPIO.output(3, True)
        if angle == 45:
            self.pwm.ChangeDutyCycle(10)
            sleep(0.445)
        self.pwm.ChangeDutyCycle(0)        
        self.position = angle
        GPIO.output(3, False)

    def get_angle(self):
        """get angle of servo motor"""
        return self.position

    def drop_ball(self):
        """drop one ball"""
        self.set_angle(45)
        return True




if __name__ == '__main__':
    """for test"""
    controller = ServoControl()
    controller.drop_ball()
    print('Ball Dropped Successfully!')

    controller.pwm.stop()
    GPIO.cleanup()
