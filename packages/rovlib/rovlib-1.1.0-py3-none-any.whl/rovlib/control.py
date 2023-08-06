from enum import IntEnum
from pymavlink import mavutil


class Violation(Exception):
    def __init__(self, message):
        super().__init__(message)



class JoyStickControl:
    def __init__(self, x_throttle = 0.0, y_throttle = 0.0, z_throttle = 0.0, rotation_throttle = 0.0):
        if (x_throttle or y_throttle or z_throttle or rotation_throttle) > 1:
            raise Violation("Throttle value should not exceed 1.0, it should be a value in the boundry of ( -1.0 to 1.0 )")
        if (x_throttle or y_throttle or z_throttle or rotation_throttle) < -1:
            raise Violation("Throttle value should not be lower than -1.0, it should be a value in the boundry of ( -1.0 to 1.0 )")

        self.x_throttle = int(x_throttle * 1000.0)
        self.y_throttle = int(y_throttle * 1000.0)
        self.z_throttle = int(500 + z_throttle * 500.0)
        self.rotation_throttle = int(rotation_throttle * 1000.0)



class RovMavlink:
    def __init__(self, connection_type = 'udpin', connection_ip = '0.0.0.0', connection_port = '14550', silent_mode = True):        
        self.connection_type = connection_type
        self.connection_ip = connection_ip
        self.connection_port = connection_port
        self.__CONNECTION_ESTABLISHED = False
        self.silent_mode = silent_mode
        self.__master = None


    class Mode(IntEnum):
        '''this modes are based on how pymavlink numbered them 🤷‍♀️'''
        STABILIZE = 0
        ACRO = 1
        ALT_HOLD = 2
        AUTO = 3
        GUIDED = 4
        CIRCLE = 7
        SURFACE = 9
        POSHOLD = 16
        MANUAL = 19


    def __print(self, msg):
        if not self.silent_mode:
            print(msg)

    def establish_connection(self):
        # Create the connection
        self.__master = mavutil.mavlink_connection(self.connection_type + ':' + self.connection_ip + ':' + self.connection_port)
        # Wait a heartbeat before sending commands
        self.__master.wait_heartbeat()
        self.__print("connection established")
        self.__CONNECTION_ESTABLISHED = True
        return self

    def arm_vehicle(self):
        if not self.__CONNECTION_ESTABLISHED:
            raise Violation("Connection is not established. Establish it first")

        self.__master.mav.command_long_send(
        self.__master.target_system,
        self.__master.target_component,
        mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
        0,
        1, 0, 0, 0, 0, 0, 0)  
        self.__print("Waiting for the vehicle to arm")
        self.__master.motors_armed_wait()
        self.__print('vehicle Armed successfully')

    def disarm_vehicle(self):
        if not self.__CONNECTION_ESTABLISHED:
            raise Violation("Connection is not established. Establish it first")

        self.__master.mav.command_long_send(
        self.__master.target_system,
        self.__master.target_component,
        mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
        0,
        0, 0, 0, 0, 0, 0, 0)
        # wait until disarming confirmed
        self.__print("Waiting for the vehicle to arm")
        self.__master.motors_disarmed_wait()
        self.__print("DisArmed")
        

    def send_control(self, joy_stick_control):
        if not self.__CONNECTION_ESTABLISHED:
            raise Violation("Connection is not established. Establish it first")
        
        self.__master.mav.manual_control_send(
            self.__master.target_system,
            joy_stick_control.x_throttle,
            joy_stick_control.y_throttle,
            joy_stick_control.z_throttle,
            joy_stick_control.rotation_throttle,
            0)


    def set_vehicle_mode(self, mode):
        if not self.__CONNECTION_ESTABLISHED:
            raise Violation("Connection is not established. Establish it first")
        if not isinstance(mode, self.Mode):
            raise ValueError('given mode must be an instance of Mode Enum')
        
        self.__master.mav.set_mode_send(
        self.__master.target_system,
        mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED, mode) # 0 is the mode id for stabilization
        self.__master.wait_heartbeat()
        self.__print('mode is set')
    
    
    def wait_heartbeat(self):
        self.__master.wait_heartbeat()

if __name__ == '__main__':
    rov = RovMavlink(connection_type = 'udpin', connection_ip = '0.0.0.0', connection_port = '14555', silent_mode = True)
    # Binds to the port in the given address
    rov.establish_connection()
    rov.arm_vehicle()
    rov.set_vehicle_mode(rov.Mode.STABILIZE)
    my_lovely_fake_joy_stick = JoyStickControl(y_throttle=1)
    rov.send_control(my_lovely_fake_joy_stick)
    rov.disarm_vehicle()