# Success

from dronekit import connect
from time import sleep

connection_string = f'/dev/ttyACM0'


print(f'connecting to device on {connection_string}')
drone = connect(connection_string, wait_ready=True)
print('connected successfully.')
print(f'GPS: %s' % drone.gps_0)
print(f'Battery: %s' % drone.battery)
print(f'Is Aemable?: % s' % drone.is_armable)
print(f'Mode: %s' % drone.mode.name)