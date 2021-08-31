from dynamixel_sdk import *

class DXLControl:
    def __init__(self):
        self.init_position = 28 # degree
        self.each_degree_pos = 10.8333
        self.drop_count = 0

        self.drop_ball_plan = {
            1: 47,
            2: 140,
            3: 235,
            4: 331
        }  # values in degree

        self.ADDR_MX_TORQUE_ENABLE = 24               # Control table address is different in Dynamixel model
        self.ADDR_MX_GOAL_POSITION = 30
        self.ADDR_MX_PRESENT_POSITION = 36
        self.PROTOCOL_VERSION = 1.0
        self.DXL_ID = 9
        self.BAUDRATE = 1000000
        self.DEVICENAME = '/dev/ttyUSB0'    
        self.TORQUE_ENABLE = 1
        self.TORQUE_DISABLE = 0
        self.DXL_MINIMUM_POSITION_VALUE = 10
        self.DXL_MAXIMUM_POSITION_VALUE = 4000
        self.DXL_MOVING_STATUS_THRESHOLD = 20

        self.portHandler = PortHandler(self.DEVICENAME)
        self.packetHandler = PacketHandler(self.PROTOCOL_VERSION)

        # Open port
        if self.portHandler.openPort():
            print("Succeeded to open the port")
        else:
            print("Failed to open the port")
            quit()


        # Set port baudrate
        if self.portHandler.setBaudRate(self.BAUDRATE):
            print("Succeeded to change the baudrate")
        else:
            print("Failed to change the baudrate")
            quit()

        # Enable Dynamixel Torque
        dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(self.portHandler, self.DXL_ID, self.ADDR_MX_TORQUE_ENABLE, self.TORQUE_ENABLE)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        else:
            print("Dynamixel has been successfully connected")
        
        self.set_angle(self.init_position, on_init=True)
    
    def _convert_angle_to_dxl_position(self, angle: float):
        """convert angle in degree to position"""
        return int(angle * self.each_degree_pos)
    
    def _convert_dxl_position_to_degree(self, position):
        """convert position to angle"""
        return position / self.each_degree_pos

    def set_angle(self, angle, on_init: bool = False):
        """set dxl position"""
        if not on_init:
            position = self._convert_angle_to_dxl_position(angle) + self._convert_angle_to_dxl_position(self.init_position)
        else:
            position = self._convert_angle_to_dxl_position(angle)
        dxl_comm_result, dxl_error = self.packetHandler.write2ByteTxRx(
            self.portHandler,
            self.DXL_ID, 
            self.ADDR_MX_GOAL_POSITION, 
            position
        )
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % self.packetHandler.getRxPacketError(dxl_error))
    
    def get_angle(self):
        """get present position"""
        dxl_present_position, dxl_comm_result, dxl_error = self.packetHandler.read2ByteTxRx(
            self.portHandler,
            self.DXL_ID,
            self.ADDR_MX_PRESENT_POSITION
        )
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % self.packetHandler.getRxPacketError(dxl_error))

        return self._convert_dxl_position_to_degree(dxl_present_position)
    
    def close_dxl(self):
        """disable dxl"""
        # Disable Dynamixel Torque
        dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(
            self.portHandler, 
            self.DXL_ID, 
            self.ADDR_MX_TORQUE_ENABLE, 
            self.TORQUE_DISABLE
        )
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))

        # Close port
        self.portHandler.closePort()
    
    def drop_ball(self):
        """drop one ball"""
        planned_angle = self.drop_ball_plan.get(self.drop_count + 1)
        self.set_angle(planned_angle)
        self.drop_count += 1

if __name__ == '__main__':
    controller = DXLControl()