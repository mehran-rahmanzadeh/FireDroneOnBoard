from dronekit import connect


class RCControl:
    def __init__(self, *args, **kwargs):
        """init"""
        self.drone = None
        # self.servo_controller = ServoControl()
        self.is_connected = False
        self.fc_port = 'localhost:14550' #'/dev/ttyACM0'
        self.drop_ball_channel_num = 16
        self.drop_count = 0

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

        @self.drone.on_message('RC_CHANNELS')
        def channel_listener(drone, name, message):
            """if channel self.drop_ball_channel_num is pressed drop ball"""
            if message == self.drop_ball_channel_num:
                # self.servo_controller.drop_ball()
                print('drop ball')
                self.drop_count += 1
                # TODO: check if it is the first drop turn 45, if second/third turn 90, forth turn 90 sleep 1 second
                #  turn 45
            self.drone.notify_attribute_listeners('channels', self.drone.channels)


if __name__ == '__main__':
    rc_control = RCControl()
    rc_control.connect()
    print('connected')
    rc_control.listen_to_rc()
