from dronekit import connect
from time import sleep
import datetime
from control_dxl import DXLControl


class RCControl:
    def __init__(self, *args, **kwargs):
        """init"""
        self.drone = None
        self.servo_controller = DXLControl()
        self.is_connected = False
        self.fc_port = '/dev/ttyACM0'
        self.drop_ball_channel_num = 7
        self.min_channel_value = 1600
        self.last_drop = 0

    def connect(self):
        """connect to drone"""
        connection_string = self.fc_port
        self.drone = connect(connection_string, wait_ready=True)
        self.is_connected = True
        return self.drone

    def info(self):
        """show drone summary info"""
        if not self.is_connected:
            return

        print('vehicle information:')
        print(" GPS: %s" % self.drone.gps_0)
        print(" Battery: %s" % self.drone.battery)
        print(" Last Heartbeat: %s" % self.drone.last_heartbeat)
        print(" Is Armable?: %s" % self.drone.is_armable)
        print(" System status: %s" % self.drone.system_status.state)
        print(" Mode: %s" % self.drone.mode.name)  # settable

    def listen_to_rc(self):
        """start listening to rc channels for dropping ball"""
        if not self.is_connected:
            return
        while True:
            sleep(0.5)
            @self.drone.on_message('RC_CHANNELS')
            def channel_listener(drone, name, message):
                """if channel self.drop_ball_channel_num is pressed drop ball"""
#                 print(message.to_dict())
                if getattr(message, f'chan{self.drop_ball_channel_num}_raw') > self.min_channel_value :
                    # self.servo_controller.drop_ball()
                    if datetime.datetime.now().timestamp() - self.last_drop > 5:
                        print(f' ------- ball number {self.servo_controller.drop_count + 1} dropped ------- ')
                        self.servo_controller.drop_ball()
                        self.last_drop = datetime.datetime.now().timestamp()
                self.drone.notify_attribute_listeners('channels', self.drone.channels)


if __name__ == '__main__':
    rc_control = RCControl()
    rc_control.connect()
    print('connected to drone')
    rc_control.listen_to_rc()
